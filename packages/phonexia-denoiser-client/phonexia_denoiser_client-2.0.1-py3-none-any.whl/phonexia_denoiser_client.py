import json
import logging
import re
from collections.abc import Iterator
from datetime import timedelta
from enum import Enum
from typing import Annotated, BinaryIO, Optional

import grpc
import numpy as np
import soundfile as sf
import typer
from google.protobuf.duration_pb2 import Duration
from google.protobuf.json_format import MessageToDict
from phonexia.grpc.common.core_pb2 import Audio, RawAudioConfig, TimeRange
from phonexia.grpc.technologies.denoiser.v1.denoiser_pb2 import DenoiseRequest, DenoiseResponse
from phonexia.grpc.technologies.denoiser.v1.denoiser_pb2_grpc import DenoiserStub

MAX_BATCH_SIZE = 1024


class LogLevel(str, Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


class InputFormat(str, Enum):
    UBJSON = "ubjson"
    WAV = "wav"


class DenoiseFormat(str, Enum):
    BINARY = "binary"
    JSON = "json"


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
) -> Iterator[DenoiseRequest]:
    time_range = TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    chunk_size = 1024 * 100
    if use_raw_audio:
        with sf.SoundFile(file) as r:
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
                yield DenoiseRequest(
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
            yield DenoiseRequest(audio=Audio(content=chunk, time_range=time_range))
            time_range = None


def write_result(
    audio_path: str,
    output_file: BinaryIO,
    billed_time: timedelta,
    audio_data: bytearray,
    raw_audio_config: Optional[RawAudioConfig] = None,
) -> None:
    logging.info(f"Writing denoised audio to '{output_file}'")

    if raw_audio_config is None:
        output_file.write(audio_data)
    else:
        with sf.SoundFile(
            output_file,
            mode="w",
            samplerate=raw_audio_config.sample_rate_hertz,
            channels=1,
            subtype="PCM_16",
            format="wav",
        ) as file:
            file.buffer_write(audio_data, dtype="int16")


def dump_json(response: dict, output: BinaryIO):
    payload = json.dumps(
        MessageToDict(response, always_print_fields_with_no_presence=True),
        indent=2,
        ensure_ascii=False,
    ).encode("utf-8")
    output.write(payload)


def denoise(
    channel: grpc.Channel,
    file: BinaryIO,
    output_file: BinaryIO,
    start: Optional[float],
    end: Optional[float],
    metadata: Optional[list],
    use_raw_audio: bool,
    to_json: bool,
) -> None:
    logging.info(f"Denoising '{file}'")
    stub = DenoiserStub(channel)
    response_it: Iterator[DenoiseResponse] = stub.Denoise(
        make_request(file, start, end, use_raw_audio),
        metadata=metadata,
    )
    billed_time = timedelta()
    audio_data = bytearray()
    raw_audio_config = None

    for i, response in enumerate(response_it):
        if to_json:
            if i == 0:
                output_file.write(b"[\n")
            else:
                output_file.write(b",\n")

            dump_json(response, output_file)
        else:
            audio_data += response.result.audio.content

    if to_json:
        output_file.write(b"\n]")
    else:
        if response.result.audio.HasField("raw_audio_config"):
            raw_audio_config = response.result.audio.raw_audio

        write_result(file, output_file, billed_time, audio_data, raw_audio_config)


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
    output: Annotated[
        typer.FileBinaryWrite,
        typer.Option(
            "--output", "-o", help="Output file path. If omitted, prints to stdout.", lazy=False
        ),
    ],
    file: Annotated[
        typer.FileBinaryRead,
        typer.Argument(
            lazy=False,
            help="Input audio file. If omitted, the client reads audio bytes from standard input.",
        ),
    ] = "-",
    input_format: Annotated[
        Optional[InputFormat],
        typer.Option(
            "-F",
            "--in-format",
            help="Forced input format. For the case the input is <stdin>.",
        ),
    ] = None,
    fmt: Annotated[
        DenoiseFormat,
        typer.Option(
            "-f",
            "--out-format",
            help="Output file format.",
        ),
    ] = DenoiseFormat.JSON,
    host: Annotated[
        str,
        typer.Option("--host", "-H", help="Server address (host:port)."),
    ] = "localhost:8080",
    log_level: Annotated[
        LogLevel, typer.Option("--log-level", "-l", help="Logging level.")
    ] = LogLevel.ERROR,
    metadata: Annotated[
        Optional[list[str]],
        typer.Option(
            "--metadata",
            metavar="key=value",
            help="Custom client metadata.",
            show_default=False,
            callback=_parse_metadata_callback,
        ),
    ] = None,
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
) -> None:
    """Remove noises and other disturbing elements from audio recordings."""

    if metadata is None:
        metadata = []
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
            to_json = fmt == DenoiseFormat.JSON

            denoise(
                channel=channel,
                file=file,
                output_file=output,
                start=time_range[0],
                end=time_range[1],
                metadata=metadata,
                use_raw_audio=use_raw_audio,
                to_json=to_json,
            )

    except grpc.RpcError:
        logging.exception("RPC failed")
        raise typer.Exit(code=1) from None
    except (typer.Exit, typer.BadParameter):
        raise
    except Exception:
        logging.exception("Unknown error")
        raise typer.Exit(code=2) from None


if __name__ == "__main__":
    app()
