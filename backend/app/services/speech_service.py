import asyncio
import tempfile
import os
import subprocess
import json
import wave
from vosk import Model, KaldiRecognizer
from gtts import gTTS
import logging
from pathlib import Path
from pydantic import BaseModel

class SpeechService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.models = {}
        self.model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../models/audioModel"))

        self.LANG_TO_MODEL = {
            "en": "vosk-model-en-us-0.22-lgraph",
            "hi": "vosk-model-small-hi-0.22",
            "gu": "vosk-model-small-gu-0.42",
            "te": "vosk-model-small-te-0.42"
        }

        # Preload all available models
        for lang_code, folder in self.LANG_TO_MODEL.items():
            model_path = os.path.join(self.model_dir, folder)
            if os.path.exists(model_path):
                self.models[lang_code] = Model(model_path)
            else:
                self.logger.warning(f"Model for '{lang_code}' not found at {model_path}")

    async def speech_to_text(self, audio_content: bytes, lang_code: str = "en") -> str:
        """Convert speech to text using Vosk for a specific language."""
        if lang_code not in self.models:
            raise ValueError(f"Unsupported language code '{lang_code}'")

        model = self.models[lang_code]

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_mp3:
            temp_mp3.write(audio_content)
            mp3_path = temp_mp3.name

        wav_path = mp3_path.rsplit(".", 1)[0] + ".wav"
        try:
            command = [
                "ffmpeg", "-y", "-i", mp3_path,
                "-ar", "16000", "-ac", "1", "-f", "wav", wav_path
            ]
            await asyncio.to_thread(subprocess.run, command, check=True)

            transcription = await asyncio.to_thread(self._transcribe, wav_path, model)

            if transcription:
                print("Transcription:", transcription)

            return transcription

        except Exception as e:
            self.logger.error(f"Error in speech to text conversion: {str(e)}")
            raise
        finally:
            if os.path.exists(mp3_path):
                os.unlink(mp3_path)
            if os.path.exists(wav_path):
                os.unlink(wav_path)

    def _transcribe(self, wav_path: str, model: Model) -> str:
        results = []
        with wave.open(wav_path, "rb") as wf:
            rec = KaldiRecognizer(model, wf.getframerate())
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    results.append(res.get("text", ""))
            final_result = json.loads(rec.FinalResult())
            results.append(final_result.get("text", ""))
        transcription = " ".join(results).strip()
        return transcription

    async def text_to_speech(self, text: str, lang_code: str) -> bytes:
        """Convert text to speech using gTTS and return an mp3 file in bytes."""
        return await asyncio.to_thread(self._generate_tts, text, lang_code)

    def _generate_tts(self, text: str, lang_code: str) -> bytes:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_filename = temp_file.name
        try:
            tts = gTTS(text=text, lang=lang_code)
            tts.save(temp_filename)
            with open(temp_filename, 'rb') as f:
                audio_content = f.read()
            return audio_content
        except Exception as e:
            self.logger.error(f"Error in text to speech generation: {str(e)}")
            raise
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

class TextResponse(BaseModel):
    response: str
    detected_language: str
