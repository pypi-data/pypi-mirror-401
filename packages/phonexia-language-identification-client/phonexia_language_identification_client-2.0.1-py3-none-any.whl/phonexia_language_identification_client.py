import csv
import json
import logging
import re
from enum import Enum
from pathlib import Path
from typing import Annotated, Any, BinaryIO, Iterator, Optional, TextIO

import grpc
import numpy as np
import phonexia.grpc.common.core_pb2 as phx_common
import soundfile
import typer
import ubjson
from google.protobuf.duration_pb2 import Duration
from google.protobuf.json_format import MessageToDict
from phonexia.grpc.common.core_pb2 import RawAudioConfig
from phonexia.grpc.technologies.language_identification.v1.language_identification_pb2 import (
    AdaptationProfile,
    AdaptationUnit,
    AdaptRequest,
    AdaptResponse,
    ExtractConfig,
    ExtractRequest,
    ExtractResponse,
    IdentifyConfig,
    IdentifyRequest,
    Language,
    LanguageGroup,
    Languageprint,
    ListSupportedLanguagesConfig,
    ListSupportedLanguagesRequest,
    ListSupportedLanguagesResponse,
)
from phonexia.grpc.technologies.language_identification.v1.language_identification_pb2_grpc import (
    LanguageIdentificationStub,
)


class LogLevel(str, Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


class AdaptationOutputFormat(str, Enum):
    BINARY = "binary"
    JSON = "json"


class ExtractOutputFormat(str, Enum):
    LP = "languageprint"
    JSON = "json"


class InputFormat(str, Enum):
    LP = "languageprint"
    AUDIO = "audio"

    @staticmethod
    def from_file(file: BinaryIO):
        try:
            ubjson.load(file)
            return InputFormat.LP  # noqa: TRY300
        except Exception:  # noqa: S110
            pass
        finally:
            file.seek(0)

        try:
            if file.read(4) == b"VPT ":
                return InputFormat.LP
        except Exception:  # noqa: S110
            pass
        finally:
            file.seek(0)

        return InputFormat.AUDIO


# Utility functions
def time_to_duration(time: Optional[float]) -> Optional[Duration]:
    if time is None:
        return None
    duration = Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def audio_request_iterator(
    file: BinaryIO,
    use_raw_audio: bool,
    request_type: Any,
    time_range: phx_common.TimeRange,
    config: Any,
) -> Iterator:
    if use_raw_audio:
        with soundfile.SoundFile(file) as r:
            raw_audio_config = RawAudioConfig(
                channels=r.channels,
                sample_rate_hertz=r.samplerate,
                encoding=RawAudioConfig.AudioEncoding.PCM16,
            )

            for data in r.blocks(blocksize=r.samplerate, dtype="float32"):
                logging.debug(f"{data.shape[0]} samples read")
                int16_info = np.iinfo(np.int16)
                data_scaled = np.clip(
                    data * (int16_info.max + 1), int16_info.min, int16_info.max
                ).astype("int16")
                yield request_type(
                    audio=phx_common.Audio(
                        content=data_scaled.flatten().tobytes(),
                        raw_audio_config=raw_audio_config,
                        time_range=time_range,
                    ),
                    config=config,
                )
                config = None
                time_range = None
                raw_audio_config = None
    else:
        while chunk := file.read(1024 * 100):  # read by 100kB
            yield request_type(
                audio=phx_common.Audio(content=chunk, time_range=time_range), config=config
            )
            config = None
            time_range = None


def read_adaptation_profile(path: Path) -> AdaptationProfile:
    with open(path, mode="rb") as file:
        return AdaptationProfile(content=file.read())


def write_bin(path: Path, content: bytes) -> None:
    with open(path, "wb") as f:
        f.write(content)


# Language Identification
def languageprint_request_iterator(file, config) -> Iterator[IdentifyRequest]:
    yield IdentifyRequest(config=config, languageprint=Languageprint(content=file.read()))


def make_identify_request(
    file: BinaryIO,
    in_format: InputFormat,
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    languages: Optional[list[Language]],
    groups: Optional[list[LanguageGroup]],
    use_raw_audio: bool,
    adaptation_profile: Optional[BinaryIO],
) -> Iterator[IdentifyRequest]:
    time_range = phx_common.TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    adaptation_profile = (
        AdaptationProfile(content=adaptation_profile.read()) if adaptation_profile else None
    )
    config = IdentifyConfig(
        speech_length=time_to_duration(speech_length),
        languages=languages,
        groups=groups,
        adaptation_profile=adaptation_profile,
    )
    if in_format == InputFormat.LP:
        return languageprint_request_iterator(file, config)
    else:
        return audio_request_iterator(file, use_raw_audio, IdentifyRequest, time_range, config)


def write_response_json(
    output: BinaryIO,
    response: Any,
) -> None:
    payload = json.dumps(
        MessageToDict(
            response, always_print_fields_with_no_presence=True, preserving_proto_field_name=True
        ),
        indent=2,
        ensure_ascii=False,
    ).encode("utf-8")
    output.write(payload)


def identify_impl(
    channel: grpc.Channel,
    input_file: BinaryIO,
    in_format: InputFormat,
    output: BinaryIO,
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    input_languages: Optional[TextIO],
    input_groups: Optional[TextIO],
    metadata: Optional[list],
    use_raw_audio: bool,
    adaptation_profile: Optional[BinaryIO],
) -> None:
    logging.info(f"{input_file.name} -> {output.name}")

    logging.debug(f"Parsing input languages {input_languages}")
    languages: Optional[list[Language]] = (
        None
        if input_languages is None
        else [Language(language_code=code) for code in json.loads(input_languages.read())]
    )

    logging.debug(f"Parsing input groups {input_groups}")
    groups: Optional[list[LanguageGroup]] = (
        None
        if input_groups is None
        else [
            LanguageGroup(identifier=identifier, language_codes=langs)
            for identifier, langs in json.loads(input_groups.read()).items()
        ]
    )

    logging.info(f"Estimating language probabilities from file '{input_file}'")
    stub = LanguageIdentificationStub(channel)
    response = stub.Identify(
        make_identify_request(
            file=input_file,
            in_format=in_format,
            start=start,
            end=end,
            speech_length=speech_length,
            languages=languages,
            groups=groups,
            use_raw_audio=use_raw_audio,
            adaptation_profile=adaptation_profile,
        ),
        metadata=metadata,
    )

    logging.info("Writing results")
    write_response_json(output, response)


# List Supported Languages
def list_supported_languages_impl(
    channel: grpc.Channel,
    output: BinaryIO,
    metadata: Optional[list],
    adaptation_profile: Optional[Path],
) -> None:
    logging.info("Getting supported languages")
    adaptation_profile = read_adaptation_profile(adaptation_profile) if adaptation_profile else None
    stub = LanguageIdentificationStub(channel)
    response: ListSupportedLanguagesResponse = stub.ListSupportedLanguages(
        ListSupportedLanguagesRequest(
            config=ListSupportedLanguagesConfig(adaptation_profile=adaptation_profile)
        ),
        metadata=metadata,
    )

    logging.info(f"Writing result to {output.name}")

    payload = json.dumps(
        MessageToDict(response, always_print_fields_with_no_presence=True),
        indent=2,
        ensure_ascii=False,
    ).encode("utf-8")
    output.write(payload)


# Languageprint Extraction
def make_extract_request(
    file: BinaryIO,
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    use_raw_audio: bool,
) -> Iterator[ExtractRequest]:
    time_range = phx_common.TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    config = ExtractConfig(speech_length=time_to_duration(speech_length))
    return audio_request_iterator(file, use_raw_audio, ExtractRequest, time_range, config)


def write_extraction_result(
    response: ExtractResponse,
    output: BinaryIO,
    out_format: ExtractOutputFormat,
) -> None:
    if out_format == ExtractOutputFormat.JSON:
        write_response_json(output, response)
    else:
        output.write(response.result.languageprint.content)


def extract_impl(
    channel: grpc.Channel,
    input_file: BinaryIO,
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    metadata: Optional[list],
    use_raw_audio: bool,
    output: BinaryIO,
    out_format: ExtractOutputFormat,
) -> None:
    logging.info(f"{input_file} -> {output.name}")

    logging.info("Extracting languageprint")
    stub = LanguageIdentificationStub(channel)

    response = stub.Extract(
        make_extract_request(input_file, start, end, speech_length, use_raw_audio),
        metadata=metadata,
    )

    logging.info("Writing results")
    write_extraction_result(response, output, out_format)


# Adaptation profile creation
def make_adapt_request(
    input_list: list[str],
    languages: list[str],
) -> Iterator[AdaptRequest]:
    max_batch_size = 1024
    batch_size = 0
    request = AdaptRequest()
    for [lp_file, language] in zip(input_list, languages, strict=True):
        logging.debug(f"Appending file '{lp_file}' -> '{language}'.")
        if batch_size >= max_batch_size:
            yield request
            batch_size = 0
            request = AdaptRequest()
        if lp_file:
            with open(lp_file, "rb") as lp_open_file:
                unit = AdaptationUnit(
                    languageprint=Languageprint(content=lp_open_file.read()),
                    language=Language(language_code=language),
                )
                request.adaptation_units.append(unit)
            batch_size += 1

    if len(request.adaptation_units):
        yield request


def write_adapt_result(
    response: AdaptResponse,
    output: BinaryIO,
    out_format: AdaptationOutputFormat,
) -> None:
    logging.info(f"Writing adaptation profile to {output.name}")
    if out_format == AdaptationOutputFormat.JSON:
        write_response_json(output, response)
    else:
        output.write(response.result.adaptation_profile.content)


def adapt_languages_impl(
    channel: grpc.Channel,
    input_list: list[str],
    languages: list[str],
    metadata: Optional[list],
    output: BinaryIO,
    output_format: AdaptationOutputFormat,
) -> None:
    logging.info(
        f"Adapting languages using {len(input_list)} languageprints with {len(set(languages))} unique languages."
    )
    logging.info(f"Unique languages are: {set(languages)}.")
    stub = LanguageIdentificationStub(channel)

    response = stub.Adapt(
        make_adapt_request(input_list, languages),
        metadata=metadata,
    )

    logging.info("Writing results")
    write_adapt_result(response, output, output_format)


# Helper functions
app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True)


def _parse_time_range(time_range: str) -> tuple[Optional[float], Optional[float]]:
    if time_range is None:
        return None, None

    if len(time_range) == 0:
        raise typer.BadParameter("Parameter 'time_range' must be of the form '[START]:[END]'.")

    # Regex pattern to match [START]:[END] format where START and END are positive floats
    pattern = r"^(\d+(?:\.\d+)?)?:(\d+(?:\.\d+)?)?$"
    match = re.match(pattern, time_range.strip())

    if not match:
        raise typer.BadParameter(
            "Parameter 'time_range' must be of the form '[START]:[END]' where START and END are positive float numbers."
        )

    # Parse START and END from regex groups
    start_str = match.group(1)
    end_str = match.group(2)

    start = float(start_str) if start_str is not None else None
    end = float(end_str) if end_str is not None else None

    if start is not None and end is not None and start >= end:
        raise typer.BadParameter("Parameter 'end' must be larger than 'start'.")

    return (None if start == 0.0 else start, end)


def _parse_metadata_callback(
    ctx: typer.Context, metadata_list: Optional[list[str]]
) -> list[tuple[str, str]]:
    if ctx.resilient_parsing or metadata_list is None:
        return []

    params = []
    for item in metadata_list:
        t = tuple(item.split("=", 1))
        if len(t) != 2:
            raise typer.BadParameter(f"Metadata must be in format 'KEY=VALUE': {item}")
        params.append(t)
    return params


def parse_list_adapt(csvfile: TextIO) -> list:
    reader = csv.reader(csvfile, delimiter=" ", skipinitialspace=True)
    rows = list(reader)

    num_cols = max(len(row) for row in rows)
    if num_cols != min(len(row) for row in rows):
        raise ValueError(f"Two or more rows in '{csvfile.name}' have different number of columns.")

    if num_cols != 2:
        raise ValueError(
            f"File '{csvfile.name}' must contain one column with file paths and "
            "one with associated language codes."
        )

    return rows


@app.command()
def identify(
    ctx: typer.Context,
    input_file: Annotated[
        Optional[typer.FileBinaryRead],
        typer.Argument(help="Input file path. If omitted, reads from stdin.", lazy=False),
    ] = "-",
    in_format: Annotated[
        Optional[InputFormat],
        typer.Option(
            "-F",
            "--in-format",
            help="Input file format for 'identify' operation.",
        ),
    ] = None,
    groups: Annotated[
        Optional[typer.FileText],
        typer.Option(
            "--groups",
            help="Path to a json file with definitions of groups. The groups must have unique id "
            "and should be assigned disjunct subset of languages. The file should contain a json "
            "dictionary where each key should be a group identifier and value should be a List of "
            'language codes, i.e. {"english": ["en-US", "en-GB"], "arabic": ["ar-IQ", "ar-KW"]}',
            lazy=False,
        ),
    ] = None,
    time_range: Annotated[
        Optional[str],
        typer.Option(
            "-t",
            "--time-range",
            callback=_parse_time_range,
            metavar="[START]:[END]",
            help=(
                "Time range in seconds using format [START]:[END] where START and END are positive float numbers. "
                "START can be omitted to process from beginning, END can be omitted to process to the end of the recording. "
                "Examples: --time-range :10 (0 to 10), --time-range 10.1: (10.1 to end), --time-range 5:10 (5 to 10)."
            ),
        ),
    ] = None,
    speech_length: Annotated[
        Optional[float],
        typer.Option("--speech-length", help="Maximum amount of speech in seconds.", min=0),
    ] = None,
    adaptation_profile: Annotated[
        Optional[typer.FileBinaryRead],
        typer.Option(
            "--adaptation-profile",
            help="Path to a binary file with language adaptation profile used for 'identify' operation.",
            lazy=False,
        ),
    ] = None,
    use_raw_audio: Annotated[
        bool,
        typer.Option(
            "--use-raw-audio",
            help="Send raw audio in chunks. Enables continuous audio processing with less server memory usage.",
        ),
    ] = False,
    output: Annotated[
        typer.FileBinaryWrite,
        typer.Option(
            "--output", "-o", help="Output file path. If omitted, prints to stdout.", lazy=False
        ),
    ] = "-",
    languages: Annotated[
        Optional[typer.FileText],
        typer.Option(
            "--languages",
            help="Path to a json file with selected subset of languages for the identification. "
            'The file should contain a json array of language codes, i.e. ["cs-cz", "en-US"]',
            lazy=False,
        ),
    ] = None,
):
    try:
        logging.info(f"Connecting to {ctx.obj['host']}")
        with (
            grpc.insecure_channel(target=ctx.obj["host"])
            if ctx.obj["plaintext"]
            else grpc.secure_channel(
                target=ctx.obj["host"], credentials=grpc.ssl_channel_credentials()
            )
        ) as channel:
            if in_format is None:
                if input_file.name == "<stdin>":
                    raise typer.BadParameter(  # noqa: TRY301
                        "Input format must be specified when reading from stdin."
                    )
                else:
                    in_format = InputFormat.from_file(input_file)

            identify_impl(
                channel=channel,
                input_file=input_file,
                in_format=in_format,
                output=output,
                start=time_range[0],
                end=time_range[1],
                speech_length=speech_length,
                input_languages=languages,
                input_groups=groups,
                metadata=ctx.obj["metadata"],
                use_raw_audio=use_raw_audio,
                adaptation_profile=adaptation_profile,
            )
    except grpc.RpcError:
        logging.exception("RPC failed")
        raise typer.Exit(code=1) from None
    except (typer.Exit, typer.BadParameter):
        raise
    except Exception:
        logging.exception("Unknown error")
        raise typer.Exit(code=2) from None


@app.command()
def extract(
    ctx: typer.Context,
    input_file: Annotated[
        typer.FileBinaryRead,
        typer.Argument(
            help="Input file for 'extract' operation.",
            lazy=False,
        ),
    ] = "-",
    time_range: Annotated[
        Optional[str],
        typer.Option(
            "-t",
            "--time-range",
            callback=_parse_time_range,
            metavar="[START]:[END]",
            help=(
                "Time range in seconds using format [START]:[END] where START and END are positive float numbers. "
                "START can be omitted to process from beginning, END can be omitted to process to the end of the recording. "
                "Examples: --time-range :10 (0 to 10), --time-range 10.1: (10.1 to end), --time-range 5:10 (5 to 10)."
            ),
        ),
    ] = None,
    speech_length: Annotated[
        Optional[float],
        typer.Option("--speech-length", help="Maximum amount of speech in seconds.", min=0),
    ] = None,
    use_raw_audio: Annotated[
        bool,
        typer.Option(
            "--use-raw-audio",
            help="Send raw audio in chunks. Enables continuous audio processing with less server memory usage.",
        ),
    ] = False,
    output: Annotated[
        typer.FileBinaryWrite,
        typer.Option(
            "--output", "-o", help="Output file path. If omitted, prints to stdout.", lazy=False
        ),
    ] = "-",
    out_format: Annotated[
        ExtractOutputFormat,
        typer.Option(
            "-f",
            "--out-format",
            help="Output file format for 'extract' operation.",
        ),
    ] = ExtractOutputFormat.JSON,
):
    try:
        logging.info(f"Connecting to {ctx.obj['host']}")
        with (
            grpc.insecure_channel(target=ctx.obj["host"])
            if ctx.obj["plaintext"]
            else grpc.secure_channel(
                target=ctx.obj["host"], credentials=grpc.ssl_channel_credentials()
            )
        ) as channel:
            extract_impl(
                channel=channel,
                input_file=input_file,
                start=time_range[0],
                end=time_range[1],
                speech_length=speech_length,
                metadata=ctx.obj["metadata"],
                use_raw_audio=use_raw_audio,
                output=output,
                out_format=out_format,
            )
    except grpc.RpcError:
        logging.exception("RPC failed")
        raise typer.Exit(code=1) from None
    except (typer.Exit, typer.BadParameter):
        raise
    except Exception:
        logging.exception("Unknown error")
        raise typer.Exit(code=2) from None


@app.command()
def adapt_languages(
    ctx: typer.Context,
    list_file: Annotated[
        Optional[typer.FileText],
        typer.Argument(
            help="List of files and their appropriate languages for 'adapt' operation.",
            lazy=False,
        ),
    ] = "-",
    output_format: Annotated[
        AdaptationOutputFormat,
        typer.Option(
            "-f",
            "--out-format",
            help="Output file format for 'adapt' operation.",
        ),
    ] = AdaptationOutputFormat.JSON,
    output: Annotated[
        typer.FileBinaryWrite,
        typer.Option(
            "--output", "-o", help="Output file path. If omitted, prints to stdout.", lazy=False
        ),
    ] = "-",
):
    try:
        logging.info(f"Connecting to {ctx.obj['host']}")
        with (
            grpc.insecure_channel(target=ctx.obj["host"])
            if ctx.obj["plaintext"]
            else grpc.secure_channel(
                target=ctx.obj["host"], credentials=grpc.ssl_channel_credentials()
            )
        ) as channel:
            input_files, languages_list = zip(*parse_list_adapt(list_file), strict=True)
            adapt_languages_impl(
                channel,
                input_files,
                languages_list,
                ctx.obj["metadata"],
                output,
                output_format,
            )
    except grpc.RpcError:
        logging.exception("RPC failed")
        raise typer.Exit(code=1) from None
    except (typer.Exit, typer.BadParameter, ValueError):
        raise
    except Exception:
        logging.exception("Unknown error")
        raise typer.Exit(code=2) from None


@app.command()
def list_languages(
    ctx: typer.Context,
    adaptation_profile: Annotated[
        Optional[typer.FileText],
        typer.Option(
            "--adaptation-profile",
            help="Path to a binary file with language adaptation profile used for 'list_languages' operation.",
            lazy=False,
        ),
    ] = None,
    output: Annotated[
        typer.FileBinaryWrite,
        typer.Option(
            "--output", "-o", help="Output file path. If omitted, prints to stdout.", lazy=False
        ),
    ] = "-",
):
    try:
        logging.info(f"Connecting to {ctx.obj['host']}")
        with (
            grpc.insecure_channel(target=ctx.obj["host"])
            if ctx.obj["plaintext"]
            else grpc.secure_channel(
                target=ctx.obj["host"], credentials=grpc.ssl_channel_credentials()
            )
        ) as channel:
            list_supported_languages_impl(
                channel,
                output,
                ctx.obj["metadata"],
                Path(adaptation_profile.name) if adaptation_profile else None,
            )
    except grpc.RpcError:
        logging.exception("RPC failed")
        raise typer.Exit(code=1) from None
    except (typer.Exit, typer.BadParameter):
        raise
    except Exception:
        logging.exception("Unknown error")
        raise typer.Exit(code=2) from None


@app.callback()
def cli(
    ctx: typer.Context,
    host: Annotated[
        str,
        typer.Option("--host", "-H", help="Server address (host:port)."),
    ] = "localhost:8080",
    log_level: Annotated[
        LogLevel, typer.Option("--log-level", "-l", help="Logging level.")
    ] = LogLevel.ERROR,
    metadata: Annotated[
        list[str],
        typer.Option(
            "--metadata",
            metavar="key=value",
            help="Custom client metadata.",
            show_default=False,
            callback=_parse_metadata_callback,
        ),
    ] = [],
    plaintext: Annotated[
        bool,
        typer.Option(
            "--plaintext", help="Use plain-text HTTP/2 when connecting to server (no TLS)."
        ),
    ] = False,
) -> None:
    """Language identification gRPC client. Identify language probabilities from input audio files."""

    ctx.obj = {
        "host": host,
        "metadata": metadata,
        "log_level": log_level,
        "plaintext": plaintext,
    }

    logging.basicConfig(
        level=log_level.value.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


if __name__ == "__main__":
    app()
