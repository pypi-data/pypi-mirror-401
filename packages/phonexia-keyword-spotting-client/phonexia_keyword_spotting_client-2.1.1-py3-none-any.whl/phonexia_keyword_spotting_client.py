import json
import logging
import re
from enum import Enum
from typing import Annotated, BinaryIO, Iterator, Optional, TextIO

import grpc
import numpy as np
import soundfile
import typer
from google.protobuf.duration_pb2 import Duration
from google.protobuf.json_format import MessageToDict, Parse, ParseError
from phonexia.grpc.common.core_pb2 import (
    Audio,
    RawAudioConfig,
    TimeRange,
)
from phonexia.grpc.technologies.keyword_spotting.v1.keyword_spotting_pb2 import (
    DetectRequest,
    DetectResponse,
    Keyword,
    ListAllowedSymbolsRequest,
    ListAllowedSymbolsResponse,
)
from phonexia.grpc.technologies.keyword_spotting.v1.keyword_spotting_pb2_grpc import (
    KeywordSpottingStub,
)


class LogLevel(str, Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


def message_to_dict(message):
    return MessageToDict(
        message,
        always_print_fields_with_no_presence=True,
        preserving_proto_field_name=True,
        use_integers_for_enums=False,
    )


def time_to_duration(time: Optional[float]) -> Optional[Duration]:
    if time is None:
        return None
    duration = Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def make_request(
    file: BinaryIO,
    keywords: list[Keyword],
    start: Optional[float],
    end: Optional[float],
    use_raw_audio: bool,
) -> Iterator[DetectRequest]:
    time_range = TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    chunk_size = 1024 * 100
    if use_raw_audio:
        with soundfile.SoundFile(file) as r:
            raw_audio_config = RawAudioConfig(
                channels=r.channels,
                sample_rate_hertz=r.samplerate,
                encoding=RawAudioConfig.AudioEncoding.PCM16,
            )
            for data in r.blocks(blocksize=r.samplerate, dtype="float32"):
                int16_info = np.iinfo(np.int16)
                data_scaled = np.clip(
                    data * (int16_info.max + 1), int16_info.min, int16_info.max
                ).astype("int16")
                yield DetectRequest(
                    audio=Audio(
                        content=data_scaled.flatten().tobytes(),
                        raw_audio_config=raw_audio_config,
                        time_range=time_range,
                    ),
                    keywords=keywords,
                )
                time_range = None
                raw_audio_config = None
                keywords = None

    else:
        while chunk := file.read(chunk_size):
            yield DetectRequest(
                audio=Audio(content=chunk, time_range=time_range),
                keywords=keywords,
            )
            time_range = None
            keywords = None


def print_json(response: DetectResponse, output: TextIO) -> None:
    print_dict(message_to_dict(response), output)


def print_dict(response: dict, output: TextIO) -> None:
    json.dump(
        response,
        output,
        indent=2,
        ensure_ascii=False,
    )


def detect_keywords(
    channel: grpc.Channel,
    keyword_list: BinaryIO,
    input_file: BinaryIO,
    output: TextIO,
    start: Optional[float],
    end: Optional[float],
    metadata: Optional[list],
    use_raw_audio: bool,
) -> None:
    logging.info("Detecting keywords from {input_file.name} -> {output.name}")
    parsed_keyword_list = Parse(text=keyword_list.read(), message=DetectRequest())
    keywords = parsed_keyword_list.keywords

    response_it = make_request(
        file=input_file,
        keywords=keywords,
        start=start,
        end=end,
        use_raw_audio=use_raw_audio,
    )

    stub = KeywordSpottingStub(channel)
    for response in stub.Detect(response_it, metadata=metadata):
        print_json(response, output)


def list_allowed_symbols(channel: grpc.Channel, output: TextIO, metadata: Optional[list]):
    logging.info("Listing allowed symbols")
    stub = KeywordSpottingStub(channel)

    response: ListAllowedSymbolsResponse = stub.ListAllowedSymbols(
        ListAllowedSymbolsRequest(), metadata=metadata
    )
    print_json(response, output)


# Main program
def handle_grpc_error(e: grpc.RpcError):
    err_msg = f"gRPC call failed with status code: {e.code()}\n\n"

    if e.code() == grpc.StatusCode.UNAVAILABLE:
        err_msg += "Service is unavailable at this address. (Hint use '--plaintext' option to connect to the service without TLS.)"
    elif e.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
        err_msg += "Service is busy. Please try again later."
    elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
        err_msg += f"Invalid arguments were provided to the RPC. Details: {e.details()}"
    elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
        err_msg += "The RPC deadline was exceeded."
    else:
        err_msg += f"An unexpected error occurred: {e.code()} - {e.details()}"

    if e.details():
        err_msg += f"Error details: {e.details()}"

    raise typer.BadParameter(err_msg)


app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True)


def _parse_time_range(
    ctx: typer.Context, time_range: str
) -> tuple[Optional[float], Optional[float]]:
    """Parse time range in format 'start:end' where both start and end are optional."""
    if ctx.resilient_parsing or time_range is None:
        return None, None

    if len(time_range) == 0:
        raise typer.BadParameter("Parameter 'time_range' must be of the form '[START]:[END]'.")

    # Regex pattern to match [START]:[END] format where START and END are optional positive floats
    pattern = r"^(\d+(?:\.\d+)?)?:(\d+(?:\.\d+)?)?$"
    match = re.match(pattern, time_range.strip())

    if not match:
        raise typer.BadParameter(
            "Parameter 'time_range' must be of the form '[START]:[END]' where START and END are positive float numbers."
        )

    # Parse START and END from regex groups
    start_str = match.group(1)
    end_str = match.group(2)

    # Ensure at least one of START or END is provided
    if not start_str and not end_str:
        raise typer.BadParameter(
            "Parameter 'time_range' must specify at least one of START or END."
        )

    start = float(start_str) if start_str else None
    end = float(end_str) if end_str else None

    return start, end


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


@app.command()
def cli(
    file: Annotated[
        typer.FileBinaryRead,
        typer.Argument(
            lazy=False,
            help="Input audio file. If omitted, the client reads audio bytes from standard input.",
        ),
    ] = "-",
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
    keyword_list: Annotated[
        Optional[typer.FileText],
        typer.Option(
            "-k",
            "--keyword-list",
            help="Path to a file containing a list of keywords. You can generate reference list by "
            "running this client with '--example-keyword-list' argument.",
            lazy=False,
        ),
    ] = None,
    allowed_symbols: Annotated[
        bool,
        typer.Option("--list-allowed-symbols", help="List allowed graphemes and phonemes"),
    ] = False,
    example_keyword_list: Annotated[
        bool,
        typer.Option("--example-keyword-list", help="Generate example keyword list", lazy=False),
    ] = False,
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
    use_raw_audio: Annotated[
        bool,
        typer.Option(
            "--use-raw-audio",
            help="Send raw audio in chunks. Enables continuous audio processing with less server memory usage.",
        ),
    ] = False,
    output: Annotated[
        typer.FileTextWrite,
        typer.Option(
            "--output", "-o", help="Output file path. If omitted, prints to stdout.", lazy=False
        ),
    ] = "-",
) -> None:
    """Run age estimation on an input audio file or standard input."""

    logging.basicConfig(
        level=log_level.value.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        if example_keyword_list:
            keyword_list = {
                "keywords": [
                    {
                        "spelling": "frumious",
                        "pronunciations": ["f r u m i o s", "f r u m i u s"],
                    },
                    {
                        "spelling": "flibbertigibbet",
                        "pronunciations": ["f l i b r t i j i b i t", "f l i b r t i j i b e t"],
                    },
                ]
            }
            print_dict(keyword_list, output)
        else:
            logging.info(f"Connecting to {host}")
            with (
                grpc.insecure_channel(target=host)
                if plaintext
                else grpc.secure_channel(target=host, credentials=grpc.ssl_channel_credentials())
            ) as channel:
                if allowed_symbols:
                    list_allowed_symbols(
                        channel=channel,
                        output=output,
                        metadata=metadata,
                    )
                else:
                    if not keyword_list:
                        raise typer.BadParameter(  # noqa: TRY301
                            "--keyword-list must be specified for keyword spotting"
                        )

                    detect_keywords(
                        channel=channel,
                        keyword_list=keyword_list,
                        input_file=file,
                        output=output,
                        start=time_range[0],
                        end=time_range[1],
                        metadata=metadata,
                        use_raw_audio=use_raw_audio,
                    )

    except grpc.RpcError as e:
        handle_grpc_error(e)
    except ParseError:
        logging.exception("Error while parsing keyword list")
        raise typer.Exit(code=2) from None
    except (typer.Exit, typer.BadParameter):
        raise
    except Exception:
        logging.exception("Unknown error")
        raise typer.Exit(code=3) from None


if __name__ == "__main__":
    app()