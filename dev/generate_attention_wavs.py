"""
generate_attention_wavs.py — Pre-bake "Attention" audio files for all supported languages.

Generates one WAV per language using the HALT TTS backend (Kokoro ONNX).
For languages with native Kokoro voices (en, es, fr, hi, it, pt, zh), the pronunciation
is native-quality. For others, Kokoro romanizes and speaks through the best available voice.

Output: viewer/public/data/sounds/attention/attention_{lang}.wav

Usage:
    python dev/generate_attention_wavs.py

Requires the HALT API server to be running on localhost:7778.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

API_BASE = "http://localhost:7778"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "viewer" / "public" / "data" / "sounds" / "attention"

# "Attention" in each supported language
# For languages where Kokoro has native voices, use the native word.
# For others, use the romanized version that Kokoro can phonemize.
ATTENTION_PHRASES = {
    "en": "Attention.",
    "am": "Attention.",          # Amharic — falls back to English phonemes
    "ar": "Intibah.",            # Arabic — romanized
    "bn": "Manojogh.",           # Bengali — romanized
    "de": "Achtung.",            # German
    "es": "Atención.",           # Spanish (native Kokoro voice)
    "fa": "Tavajoh.",            # Farsi — romanized
    "fr": "Attention.",          # French (native Kokoro voice)
    "ha": "Attention.",          # Hausa — falls back to English
    "he": "Attention.",          # Hebrew — falls back to English
    "hi": "Dhyaan dijiye.",      # Hindi (native Kokoro voice)
    "id": "Perhatian.",          # Indonesian
    "ig": "Attention.",          # Igbo — falls back to English
    "it": "Attenzione.",         # Italian (native Kokoro voice)
    "ja": "Chuui.",              # Japanese — romanized
    "jw": "Perhatian.",          # Javanese — uses Indonesian phonemes
    "km": "Attention.",          # Khmer — falls back
    "ko": "Ju-ui.",              # Korean — romanized
    "ku": "Attention.",          # Kurdish — falls back
    "la": "Attendite.",          # Latin
    "mg": "Attention.",          # Malagasy — uses French phonemes
    "mr": "Laksh dya.",          # Marathi — romanized
    "my": "Attention.",          # Burmese — falls back
    "nl": "Attentie.",           # Dutch
    "pl": "Uwaga.",              # Polish
    "ps": "Pam sha.",            # Pashto — romanized
    "pt": "Atenção.",            # Portuguese (native Kokoro voice)
    "ru": "Vnimanie.",           # Russian — romanized
    "so": "Attention.",          # Somali — falls back
    "sw": "Sikiliza.",           # Swahili
    "ta": "Kavanaம.",            # Tamil — romanized
    "te": "Gamaninchandi.",      # Telugu — romanized
    "th": "Attention.",          # Thai — falls back
    "tl": "Pansin.",             # Tagalog — romanized
    "tr": "Dikkat.",             # Turkish
    "uk": "Uvaga.",              # Ukrainian — romanized
    "ur": "Tawajjuh.",           # Urdu — romanized
    "vi": "Chú ý.",              # Vietnamese
    "xh": "Attention.",          # Xhosa — falls back
    "yo": "Attention.",          # Yoruba — falls back
    "zh": "注意。",               # Chinese (native Kokoro voice)
    "zu": "Attention.",          # Zulu — falls back
}


def generate_wav(text: str, lang: str, output_path: Path) -> bool:
    """Call the HALT TTS API to generate a WAV file."""
    payload = json.dumps({
        "text": text,
        "voice": "af_heart",  # _pick_voice on server will auto-swap to native
        "rate": 1.0,
        "lang": lang,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{API_BASE}/tts/synthesize",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            wav_data = resp.read()
            output_path.write_bytes(wav_data)
            size_kb = len(wav_data) / 1024
            return True
    except urllib.error.URLError as e:
        print(f"    ✗ {lang}: API error — {e}")
        return False
    except Exception as e:
        print(f"    ✗ {lang}: {e}")
        return False


def main():
    print("=" * 60)
    print("HALT — Pre-bake Attention WAV Library")
    print("=" * 60)

    # Check API is running
    try:
        urllib.request.urlopen(f"{API_BASE}/tts/health", timeout=5)
    except Exception:
        print(f"\n  ✗ Cannot reach TTS API at {API_BASE}/tts/health")
        print("    Start the server first: python api/main.py")
        sys.exit(1)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n  Output: {OUTPUT_DIR}")
    print(f"  Languages: {len(ATTENTION_PHRASES)}\n")

    success = 0
    failed = 0

    for lang, phrase in sorted(ATTENTION_PHRASES.items()):
        output_file = OUTPUT_DIR / f"attention_{lang}.wav"
        print(f"  [{lang:>3}] {phrase:<30}", end="", flush=True)

        if generate_wav(phrase, lang, output_file):
            size_kb = output_file.stat().st_size / 1024
            print(f" ✓ {size_kb:.1f} KB")
            success += 1
        else:
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"  Done: {success} generated, {failed} failed")
    print(f"  Location: {OUTPUT_DIR}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
