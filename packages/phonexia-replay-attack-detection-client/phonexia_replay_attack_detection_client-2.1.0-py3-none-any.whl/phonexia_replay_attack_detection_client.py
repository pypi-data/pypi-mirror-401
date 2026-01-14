import json
import logging
import re
from collections.abc import Iterator
from enum import Enum
from typing import Annotated, Any, BinaryIO, Optional, TextIO

import grpc
import numpy as np
import soundfile
import typer
from google.protobuf.duration_pb2 import Duration
from google.protobuf.json_format import MessageToDict
from phonexia.grpc.common.core_pb2 import Audio, RawAudioConfig, TimeRange
from phonexia.grpc.technologies.replay_attack_detection.experimental.replay_attack_detection_pb2 import (
    DetectRequest,
    DetectResponse,
)
from phonexia.grpc.technologies.replay_attack_detection.experimental.replay_attack_detection_pb2_grpc import (
    ReplayAttackDetectionStub,
)


class LogLevel(str, Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


def time_to_duration(time: Optional[float]) -> Optional[Duration]:
    if time is None:
        return None
    duration = Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def make_request(
    file: BinaryIO,
    start: Optional[float],
    end: Optional[float],
    use_raw_audio: bool,
) -> Iterator[DetectRequest]:
    time_range: Optional[TimeRange] = TimeRange(
        start=time_to_duration(start), end=time_to_duration(end)
    )
    chunk_size = 1024 * 100
    if use_raw_audio:
        with soundfile.SoundFile(file) as r:
            raw_audio_config: Optional[RawAudioConfig] = RawAudioConfig(
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
                    )
                )
                time_range = None
                raw_audio_config = None

    else:
        while chunk := file.read(chunk_size):
            yield DetectRequest(audio=Audio(content=chunk, time_range=time_range))
            time_range = None


def write_result(audio_path: str, response: DetectResponse, output: TextIO):
    logging.info(f"{audio_path!s} -> {output.name}")
    json.dump(
        MessageToDict(
            message=response,
            always_print_fields_with_no_presence=True,
            preserving_proto_field_name=True,
        ),
        output,
        indent=2,
        ensure_ascii=False,
    )


def detect(
    channel: grpc.Channel,
    file: BinaryIO,
    output: TextIO,
    start: Optional[float],
    end: Optional[float],
    metadata: Optional[list[Any]],
    use_raw_audio: bool,
):
    logging.info(f"Detecting replay attacks in {file}")
    stub = ReplayAttackDetectionStub(channel)
    response = stub.Detect(make_request(file, start, end, use_raw_audio), metadata=metadata)
    write_result(file, response, output)


# Helper functions
app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True)


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

    raise typer.BadParameter(err_msg)


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


@app.command()
def cli(
    input_file: Annotated[
        typer.FileBinaryRead,
        typer.Argument(
            help="Input audio file path.",
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
    """Run replay attack detection on input audio files."""

    logging.basicConfig(
        level=log_level.value.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        logging.info(f"Connecting to {host}")
        with (
            grpc.insecure_channel(target=host)
            if plaintext
            else grpc.secure_channel(target=host, credentials=grpc.ssl_channel_credentials())
        ) as channel:
            detect(
                channel,
                input_file,
                output,
                time_range[0],
                time_range[1],
                metadata,
                use_raw_audio,
            )
    except grpc.RpcError as e:
        handle_grpc_error(e)
    except (typer.Exit, typer.BadParameter):
        raise
    except Exception:
        logging.exception("Unknown error")
        raise typer.Exit(code=2) from None


if __name__ == "__main__":
    app()
