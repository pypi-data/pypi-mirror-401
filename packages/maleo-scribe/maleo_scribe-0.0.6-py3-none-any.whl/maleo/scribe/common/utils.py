import io
from pydub import AudioSegment
from nexo.types.string import OptStr


def is_wav(content: bytes) -> bool:
    if len(content) < 12:
        return False

    return content[0:4] == b"RIFF" and content[8:12] == b"WAVE"


def to_wav(content: bytes, format: OptStr = None) -> bytes:
    """
    Convert any audio format (MP3, M4A, AAC, etc.) to WAV.

    :param content: The raw audio file bytes.
    :param format: The format of the input audio (e.g., "mp3", "m4a", "aac").
    :return: The WAV file as bytes.
    """
    try:
        # Read content and convert to AudioSegment
        audio_io = io.BytesIO(content)
        audio = AudioSegment.from_file(audio_io, format=format)
        audio = audio.set_channels(1).set_frame_rate(16000)
        # Convert to WAV
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")

        return wav_io.getvalue()  # Return WAV as bytes
    except Exception as e:
        raise ValueError(f"Audio conversion failed: {str(e)}")
