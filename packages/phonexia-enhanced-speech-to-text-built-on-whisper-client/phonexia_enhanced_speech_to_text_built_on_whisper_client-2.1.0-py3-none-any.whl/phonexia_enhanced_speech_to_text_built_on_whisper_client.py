import json
import logging
import re
from collections.abc import Iterator
from datetime import datetime
from enum import Enum
from typing import Annotated, BinaryIO, Optional, TextIO

import grpc
import numpy as np
import phonexia.grpc.technologies.enhanced_speech_to_text_built_on_whisper.v1.enhanced_speech_to_text_built_on_whisper_pb2_grpc as stt_grpc
import soundfile
import typer
from google.protobuf.duration_pb2 import Duration
from google.protobuf.json_format import MessageToDict
from phonexia.grpc.common.core_pb2 import Audio, RawAudioConfig, TimeRange
from phonexia.grpc.technologies.enhanced_speech_to_text_built_on_whisper.v1.enhanced_speech_to_text_built_on_whisper_pb2 import (
    TranscribeConfig,
    TranscribeRequest,
    TranslateConfig,
    TranslateRequest,
)

CHUNK_SIZE = 32000


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


def transcribe_request_iterator(
    file: BinaryIO,
    specified_language: Optional[str],
    start: Optional[float],
    end: Optional[float],
    enable_language_switching: bool = False,
    enable_word_segmentation: bool = False,
    use_raw_audio: bool = False,
) -> Iterator[TranscribeRequest]:
    time_range = TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    config = TranscribeConfig(
        language=specified_language,
        enable_language_switching=enable_language_switching,
        enable_word_segmentation=enable_word_segmentation,
    )

    if use_raw_audio:
        with soundfile.SoundFile(file) as r:
            raw_audio_config = RawAudioConfig(
                channels=r.channels,
                sample_rate_hertz=r.samplerate,
                encoding=RawAudioConfig.AudioEncoding.PCM16,
            )

            for data in r.blocks(blocksize=r.samplerate, dtype="float32"):
                logging.debug("Sending chunk of size %d samples", len(data))
                int16_info = np.iinfo(np.int16)
                data_scaled = np.clip(
                    data * (int16_info.max + 1), int16_info.min, int16_info.max
                ).astype("int16")
                yield TranscribeRequest(
                    audio=Audio(
                        content=data_scaled.flatten().tobytes(),
                        time_range=time_range,
                        raw_audio_config=raw_audio_config,
                    ),
                    config=config,
                )
                time_range = None
                raw_audio_config = None
                config = None
    else:
        while chunk := file.read(CHUNK_SIZE):
            yield TranscribeRequest(
                audio=Audio(content=chunk, time_range=time_range), config=config
            )
            time_range = None
            config = None


def translate_request_iterator(
    file: BinaryIO,
    specified_language: Optional[str],
    start: Optional[float],
    end: Optional[float],
    enable_language_switching: bool = False,
    enable_word_segmentation: bool = False,
    use_raw_audio: bool = False,
) -> Iterator[TranslateRequest]:
    time_range = TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    config = TranslateConfig(
        source_language=specified_language,
        enable_language_switching=enable_language_switching,
        enable_word_segmentation=enable_word_segmentation,
    )

    if use_raw_audio:
        with soundfile.SoundFile(file) as r:
            raw_audio_config = RawAudioConfig(
                channels=r.channels,
                sample_rate_hertz=r.samplerate,
                encoding=RawAudioConfig.AudioEncoding.PCM16,
            )

            for data in r.blocks(blocksize=r.samplerate, dtype="float32"):
                logging.debug("Sending chunk of size %d samples", len(data))
                int16_info = np.iinfo(np.int16)
                data_scaled = np.clip(
                    data * (int16_info.max + 1), int16_info.min, int16_info.max
                ).astype("int16")
                yield TranslateRequest(
                    audio=Audio(
                        content=data_scaled.flatten().tobytes(),
                        time_range=time_range,
                        raw_audio_config=raw_audio_config,
                    ),
                    config=config,
                )
                time_range = None
                raw_audio_config = None
                config = None
    else:
        while chunk := file.read(CHUNK_SIZE):
            yield TranslateRequest(audio=Audio(content=chunk, time_range=time_range), config=config)
            time_range = None
            config = None


def write_result(
    audio_path: str,
    responses: list,
    output: TextIO,
    language: Optional[str],
):
    logging.info(f"{audio_path!s} -> {output.name}")

    # Aggregate all responses
    response_dict = None

    for _response in responses:
        if not response_dict:
            response_dict = MessageToDict(
                message=_response,
                always_print_fields_with_no_presence=True,
                preserving_proto_field_name=True,
            )
        else:
            response_dict["result"]["one_best"]["segments"] += \
                MessageToDict(
                    message=_response,
                    always_print_fields_with_no_presence=True,
                    preserving_proto_field_name=True,
                )["result"]["one_best"]["segments"]  # fmt: skip

    json.dump(response_dict, output, indent=2, ensure_ascii=False)


def translate_impl(
    channel: grpc.Channel,
    file: BinaryIO,
    output: TextIO,
    language: Optional[str],
    start: Optional[float],
    end: Optional[float],
    metadata: Optional[list],
    enable_language_switching: bool = False,
    enable_word_segmentation: bool = False,
    use_raw_audio: bool = False,
):
    logging.info("Processing audio file with translate")
    stub = stt_grpc.SpeechToTextStub(channel)
    response = stub.Translate(
        translate_request_iterator(
            file=file,
            specified_language=language,
            start=start,
            end=end,
            enable_language_switching=enable_language_switching,
            enable_word_segmentation=enable_word_segmentation,
            use_raw_audio=use_raw_audio,
        ),
        metadata=metadata,
    )
    # Collect all responses
    responses = list(response)
    write_result(file.name, responses, output, language)


def transcribe_impl(
    channel: grpc.Channel,
    file: BinaryIO,
    output: TextIO,
    language: Optional[str],
    start: Optional[float],
    end: Optional[float],
    metadata: Optional[list],
    enable_language_switching: bool = False,
    enable_word_segmentation: bool = False,
    use_raw_audio: bool = False,
):
    logging.info("Processing audio file with transcribe")
    stub = stt_grpc.SpeechToTextStub(channel)
    response = stub.Transcribe(
        transcribe_request_iterator(
            file=file,
            specified_language=language,
            start=start,
            end=end,
            enable_language_switching=enable_language_switching,
            enable_word_segmentation=enable_word_segmentation,
            use_raw_audio=use_raw_audio,
        ),
        metadata=metadata,
    )

    # Collect all responses
    responses = list(response)
    write_result(file.name, responses, output, language)


# Helper functions
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


@app.command()
def translate(
    ctx: typer.Context,
    input_file: Annotated[
        typer.FileBinaryRead,
        typer.Argument(
            help="Input audio file path.",
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
    language: Annotated[
        Optional[str],
        typer.Option(
            "--language",
            help=(
                "Force transcription to specified language, if not set, language is detected "
                "automatically."
            ),
        ),
    ] = None,
    enable_language_switching: Annotated[
        bool,
        typer.Option(
            "--enable-language-switching",
            help="Enable dynamic language switching during transcription, with the language being detected approximately every 30 seconds.",
        ),
    ] = False,
    enable_word_segmentation: Annotated[
        bool,
        typer.Option(
            "--enable-word-segmentation",
            help="Enable word-level transcription. Note: Enabling this option may increase processing time.",
        ),
    ] = False,
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
    """Translates input audio into segments with timestamps."""

    try:
        logging.info(f"Connecting to {ctx.obj['host']}")
        with (
            grpc.insecure_channel(target=ctx.obj["host"])
            if ctx.obj["plaintext"]
            else grpc.secure_channel(
                target=ctx.obj["host"], credentials=grpc.ssl_channel_credentials()
            )
        ) as channel:
            start_time = datetime.now()

            translate_impl(
                channel=channel,
                file=input_file,
                output=output,
                language=language,
                start=time_range[0],
                end=time_range[1],
                metadata=ctx.obj["metadata"],
                enable_language_switching=enable_language_switching,
                enable_word_segmentation=enable_word_segmentation,
                use_raw_audio=use_raw_audio,
            )

            logging.debug(f"Elapsed time {(datetime.now() - start_time)}")

    except grpc.RpcError as e:
        handle_grpc_error(e)
    except (typer.Exit, typer.BadParameter):
        raise
    except Exception:
        logging.exception("Unknown error")
        raise typer.Exit(code=2) from None


@app.command()
def transcribe(
    ctx: typer.Context,
    input_file: Annotated[
        typer.FileBinaryRead,
        typer.Argument(
            help="Input audio file path.",
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
    language: Annotated[
        Optional[str],
        typer.Option(
            "--language",
            help=(
                "Force transcription to specified language, if not set, language is detected "
                "automatically."
            ),
        ),
    ] = None,
    enable_language_switching: Annotated[
        bool,
        typer.Option(
            "--enable-language-switching",
            help="Enable dynamic language switching during transcription, with the language being detected approximately every 30 seconds.",
        ),
    ] = False,
    enable_word_segmentation: Annotated[
        bool,
        typer.Option(
            "--enable-word-segmentation",
            help="Enable word-level transcription. Note: Enabling this option may increase processing time.",
        ),
    ] = False,
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
    """Transcribes input audio into segments with timestamps."""

    try:
        logging.info(f"Connecting to {ctx.obj['host']}")
        with (
            grpc.insecure_channel(target=ctx.obj["host"])
            if ctx.obj["plaintext"]
            else grpc.secure_channel(
                target=ctx.obj["host"], credentials=grpc.ssl_channel_credentials()
            )
        ) as channel:
            start_time = datetime.now()

            transcribe_impl(
                channel=channel,
                file=input_file,
                output=output,
                language=language,
                start=time_range[0],
                end=time_range[1],
                metadata=ctx.obj["metadata"],
                enable_language_switching=enable_language_switching,
                enable_word_segmentation=enable_word_segmentation,
                use_raw_audio=use_raw_audio,
            )

            logging.debug(f"Elapsed time {(datetime.now() - start_time)}")

    except grpc.RpcError as e:
        handle_grpc_error(e)
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
    """Enhanced Speech to Text Built on Whisper gRPC client."""

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
