import json
import logging
import re
from enum import Enum
from pathlib import Path
from typing import Annotated, BinaryIO, Iterator, Optional, TextIO

import grpc
import numpy as np
import soundfile as sf
import typer
from google.protobuf.duration_pb2 import Duration
from google.protobuf.json_format import MessageToDict
from phonexia.grpc.common.core_pb2 import (
    Audio,
    RawAudioConfig,
    TimeRange,
)
from phonexia.grpc.technologies.speaker_diarization.v1.speaker_diarization_pb2 import (
    DiarizeConfig,
    DiarizeRequest,
    DiarizeResponse,
)
from phonexia.grpc.technologies.speaker_diarization.v1.speaker_diarization_pb2_grpc import (
    SpeakerDiarizationStub,
)

CHUNK_SIZE = 1024 * 1024


class LogLevel(str, Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


class OutputFormat(str, Enum):
    JSON = "json"
    RTTM = "rttm"
    LAB = "lab"


def time_to_duration(time: Optional[float]) -> Optional[Duration]:
    if time is None:
        return None
    duration = Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def make_request(
    file: BinaryIO,
    total_speakers: Optional[int],
    max_speakers: Optional[int],
    start: Optional[float],
    end: Optional[float],
    use_raw_audio: bool,
) -> Iterator[DiarizeRequest]:
    time_range = TimeRange(start=time_to_duration(start), end=time_to_duration(end))

    config = DiarizeConfig(max_speakers=max_speakers, total_speakers=total_speakers)

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
                yield DiarizeRequest(
                    audio=Audio(
                        content=data_scaled.flatten().tobytes(),
                        raw_audio_config=raw_audio_config,
                        time_range=time_range,
                    ),
                    config=config,
                )
                time_range = None
                raw_audio_config = None
                config = None

    else:
        while chunk := file.read(chunk_size):
            yield DiarizeRequest(audio=Audio(content=chunk, time_range=time_range), config=config)
            time_range = None
            config = None


def save_response_lab(response: DiarizeResponse, output):
    def to_htk(sec: float):
        return int(round(sec * 10**7, ndigits=0))

    for segment in response.segments:
        output.write(
            "{start:d} {end:d} {speaker:d}\n".format(  # noqa: UP032
                start=to_htk(segment.start_time.ToTimedelta().total_seconds()),
                end=to_htk(segment.end_time.ToTimedelta().total_seconds()),
                speaker=int(segment.speaker_id) + 1,
            )
        )


def save_response_rttm(response: DiarizeResponse, file: TextIO, output: TextIO):
    for segment in response.segments:
        beg = segment.start_time.ToTimedelta().total_seconds()
        end = segment.end_time.ToTimedelta().total_seconds()
        size = end - beg
        output.write(
            f"SPEAKER {Path(file.name).stem} 1 {beg:.2f} {size:.2f} <NA> <NA>"
            f" {int(segment.speaker_id) + 1} <NA>\n"
        )


def diarize(
    channel: grpc.Channel,
    file: BinaryIO,
    output: TextIO,
    output_format: OutputFormat,
    max_speakers: Optional[int],
    total_speakers: Optional[int],
    start: Optional[float],
    end: Optional[float],
    use_raw_audio: bool,
    metadata: Optional[list],
):
    logging.info(f"Transcribing {file.name} -> {output.name}")
    if max_speakers is not None:
        logging.info(f"Using max_speakers={max_speakers}")
    if total_speakers is not None:
        logging.info(f"Using total_speakers={total_speakers}")

    diarize_stub = SpeakerDiarizationStub(channel)
    response = diarize_stub.Diarize(
        make_request(
            file=file,
            max_speakers=max_speakers,
            total_speakers=total_speakers,
            start=start,
            end=end,
            use_raw_audio=use_raw_audio,
        ),
        metadata=metadata,
    )

    if output_format == OutputFormat.LAB:
        save_response_lab(response, output)
    elif output_format == OutputFormat.RTTM:
        save_response_rttm(response, file, output)
    elif output_format == OutputFormat.JSON:
        json.dump(
            MessageToDict(
                response,
                always_print_fields_with_no_presence=True,
                preserving_proto_field_name=True,
            ),
            output,
            indent=2,
            ensure_ascii=False,
        )


def handle_grpc_error(e: grpc.RpcError):
    logging.error(f"gRPC call failed with status code: {e.code()}")
    logging.error(f"Error details: {e.details()}")

    if e.code() == grpc.StatusCode.UNAVAILABLE:
        logging.error("Service is unavailable. Please try again later.")
    elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
        logging.error("Invalid arguments were provided to the RPC.")
    elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
        logging.error("The RPC deadline was exceeded.")
    else:
        logging.error(f"An unexpected error occurred: {e.code()} - {e.details()}")


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


@app.command()
def cli(
    file: Annotated[
        typer.FileBinaryRead,
        typer.Argument(
            help="Input audio file. '-' to read audio bytes from standard input.", lazy=False
        ),
    ] = "-",
    output: Annotated[
        typer.FileTextWrite,
        typer.Option(
            "--output", "-o", help="Output file path. If omitted, prints to stdout.", lazy=False
        ),
    ] = "-",
    output_format: Annotated[
        OutputFormat,
        typer.Option(
            "-f",
            "--out-format",
            help="Output format.",
        ),
    ] = OutputFormat.JSON,
    total_speakers: Annotated[
        Optional[int],
        typer.Option(
            "--total-speakers",
            help="Exact number of speakers in recording.",
            min=1,
        ),
    ] = None,
    max_speakers: Annotated[
        Optional[int],
        typer.Option(
            "--max-speakers",
            help="Maximum number of speakers in recording.",
            min=1,
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
        Optional[list[str]],
        typer.Option(
            "--metadata",
            metavar="KEY=VALUE",
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
            is_flag=True,
        ),
    ] = False,
) -> None:
    """Run speaker diarization on input audio data. Identifies speakers in input audio and returns segmentation with timestamps for each speaker."""

    logging.basicConfig(
        level=log_level.value.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        if total_speakers is not None and max_speakers is not None:
            raise typer.BadParameter(  # noqa: TRY301
                "total_speakers and max_speakers cannot be specified at the same time"
            )

        logging.info(f"Connecting to {host}")
        with (
            grpc.insecure_channel(target=host)
            if plaintext
            else grpc.secure_channel(target=host, credentials=grpc.ssl_channel_credentials())
        ) as channel:
            diarize(
                channel=channel,
                file=file,
                output=output,
                output_format=output_format,
                max_speakers=max_speakers,
                total_speakers=total_speakers,
                start=time_range[0],
                end=time_range[1],
                use_raw_audio=use_raw_audio,
                metadata=metadata,
            )

    except grpc.RpcError as e:
        handle_grpc_error(e)
        raise typer.Exit(code=1) from None
    except ValueError as e:
        logging.error(f"Error while writing result: {e}")  # noqa: TRY400
        raise typer.Exit(code=1) from None
    except (typer.Exit, typer.BadParameter):
        raise
    except Exception:
        logging.exception("Unknown error")
        raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
