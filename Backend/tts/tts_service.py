"""
=====================================================
Ramayana AI
Piper Text-to-Speech Service
Supports:
    - English (en_US-lessac-medium)
    - Hindi (hi_IN-pratham-medium)
=====================================================
"""

from pathlib import Path
from datetime import datetime
import wave

from piper import PiperVoice


class PiperTTS:

    def __init__(self):

        # Project Root
        self.project_root = Path(__file__).resolve().parent.parent.parent

        # Piper Models Folder
        self.model_dir = self.project_root / "Models" / "Piper"

        # Audio Output Folder
        self.output_dir = self.project_root / "Backend" / "audio"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        print("\n========== Loading Piper Voices ==========")

        # -------------------------------
        # English Voice
        # -------------------------------
        print("Loading English Voice...")

        self.en_voice = PiperVoice.load(
            str(self.model_dir / "en_IN-medium.onnx"),
            config_path=str(
                self.model_dir / "en_IN-medium.onnx.json"
                )
            )

        print("English Voice Loaded")

        # -------------------------------
        # Hindi Voice
        # -------------------------------
        print("Loading Hindi Voice...")

        self.hi_voice = PiperVoice.load(
            str(self.model_dir / "hi_IN-pratham-medium.onnx"),
            config_path=str(
                self.model_dir / "hi_IN-pratham-medium.onnx.json"
            )
        )

        print("Hindi Voice Loaded")

        print("==========================================\n")

    def generate(
        self,
        text: str,
        language: str = "en"
    ) -> str:

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        language = language.lower()

        # Select voice
        if language == "hi":
            voice = self.hi_voice
        else:
            voice = self.en_voice
            language = "en"

        filename = (
            f"answer_{language}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        )

        output_file = self.output_dir / filename

        print(f"\nGenerating {language.upper()} Audio...")
        print(f"Saving : {output_file}")

        with wave.open(str(output_file), "wb") as wav_file:

            voice.synthesize_wav(
                text=text,
                wav_file=wav_file
            )

        print("Audio Generated Successfully!\n")

        return filename