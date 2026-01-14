import json
import logging
import re
import sys
from enum import Enum
from typing import Annotated, BinaryIO, Iterator, Optional

import grpc
import numpy as np
import soundfile
import typer
import ubjson
from google.protobuf.duration_pb2 import Duration
from google.protobuf.json_format import MessageToDict
from phonexia.grpc.common.core_pb2 import (
    Audio,
    RawAudioConfig,
    TimeRange,
    Voiceprint,
)
from phonexia.grpc.technologies.age_estimation.v1.age_estimation_pb2 import (
    EstimateConfig,
    EstimateRequest,
)
from phonexia.grpc.technologies.age_estimation.v1.age_estimation_pb2_grpc import (
    AgeEstimationStub,
)

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


def time_to_duration(time: float) -> Optional[Duration]:
    if time is None:
        return None
    duration = Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def is_ubjson_file(f: BinaryIO):
    try:
        ubjson.load(f)
        return True  # noqa: TRY300
    except Exception:  # noqa: S110
        pass
    finally:
        f.seek(0)

    try:
        if f.read(4) == b"VPT ":
            return True
    except Exception:  # noqa: S110
        pass
    finally:
        f.seek(0)

    return False


def make_vp_batch_request(vp_file: BinaryIO) -> Iterator[EstimateRequest]:
    yield EstimateRequest(voiceprints=[Voiceprint(content=vp_file.read())])


def make_audio_batch_request(
    file: BinaryIO,
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    use_raw_audio: bool,
) -> Iterator[EstimateRequest]:
    time_range = TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    config = EstimateConfig(speech_length=time_to_duration(speech_length))
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
                yield EstimateRequest(
                    audio=Audio(
                        content=data_scaled.flatten().tobytes(),
                        raw_audio_config=raw_audio_config,
                        time_range=time_range,
                    ),
                    config=config,
                )
                time_range = None
                raw_audio_config = None

    else:
        while chunk := file.read(chunk_size):
            yield EstimateRequest(audio=Audio(content=chunk, time_range=time_range), config=config)
            time_range = None


def estimate_age(
    file: BinaryIO,
    input_format: InputFormat,
    channel: grpc.Channel,
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    metadata: Optional[list],
    use_raw_audio: bool,
    output: typer.FileTextWrite,
) -> None:
    if input_format == InputFormat.UBJSON:
        batch_request = make_vp_batch_request(file)
    else:
        batch_request = make_audio_batch_request(
            file=file,
            start=start,
            end=end,
            speech_length=speech_length,
            use_raw_audio=use_raw_audio,
        )

    stub = AgeEstimationStub(channel)
    for result in stub.Estimate(batch_request, metadata=metadata):
        output.write(
            json.dumps(
                MessageToDict(
                    result,
                    always_print_fields_with_no_presence=True,
                    preserving_proto_field_name=True,
                ),
                indent=2,
                ensure_ascii=False,
            )
            + "\n"
        )


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


def determine_format(input_file: BinaryIO, input_format: Optional[InputFormat]) -> InputFormat:
    determined_format = input_format

    if input_file is not sys.stdin.buffer:
        determined_format = InputFormat.UBJSON if is_ubjson_file(input_file) else InputFormat.WAV
    elif not determined_format:
        raise typer.BadParameter(
            "Parameter '--in-format' must be specified when using <stdin> as an input."
        )

    return determined_format


@app.command()
def cli(
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
    speech_length: Annotated[
        Optional[float],
        typer.Option("--speech-length", help="Maximum amount of speech in seconds.", min=1e-6),
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
        logging.info(f"Connecting to {host}")
        with (
            grpc.insecure_channel(target=host)
            if plaintext
            else grpc.secure_channel(target=host, credentials=grpc.ssl_channel_credentials())
        ) as channel:
            start = time_range[0] if time_range is not None else None
            end = time_range[1] if time_range is not None else None

            input_format = determine_format(file, input_format)

            estimate_age(
                file=file,
                input_format=input_format,
                channel=channel,
                metadata=metadata,
                start=start,
                end=end,
                speech_length=speech_length,
                use_raw_audio=use_raw_audio,
                output=output,
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
