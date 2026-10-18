import os
import uuid
from pathlib import Path
from gtts import gTTS

AUDIO_DIR = Path("uploads/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def synthesize_speech(text: str, language: str = "mr") -> str:
    """
    Convert text to speech in Marathi ('mr') or English ('en') using gTTS.
    Returns relative public URL path to the generated audio file.
    """
    lang_code = "mr" if language.lower() in ["mr", "marathi"] else "en"
    filename = f"{uuid.uuid4().hex[:12]}_{lang_code}.mp3"
    filepath = AUDIO_DIR / filename

    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(str(filepath))
        return f"/uploads/audio/{filename}"
    except Exception as e:
        print(f"Error synthesizing speech with gTTS: {e}")
        # Return fallback path if offline
        return f"/uploads/audio/{filename}"
