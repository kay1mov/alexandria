import whisper
import torch
from ai.config import *


class Transcriber:
    def __init__(self):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(AI_FOR_AUDIO.get("model_type"), device=self.device)

    def transcribe_audio_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Path: {file_path} doesn't exist")

        result = model.transcribe(
            file_path,
            language=AI_FOR_AUDIO.get("default_language", "en"),
            fp16=(device == "cuda"),
            temperature=0,
            without_timestamps=True
        )

        return result["text"].strip()

