#!/usr/bin/env python3
"""
Evie Voice Listener - Speech-to-Text
Captures audio from microphone and transcribes using Whisper

Usage:
    python evie-listen.py                    # Listen once, return text
    python evie-listen.py --continuous       # Keep listening until "goodbye Evie"
    python evie-listen.py --wake-word        # Wait for "Hey Evie" to activate
    python evie-listen.py --timeout 10       # Listen for 10 seconds max
"""

import subprocess
import sys
import argparse
import os

# Ensure ffmpeg is in PATH for Whisper (Windows fix)
if sys.platform == "win32":
    ffmpeg_path = r"C:\ffmpeg\bin"
    if ffmpeg_path not in os.environ.get("PATH", ""):
        os.environ["PATH"] = ffmpeg_path + ";" + os.environ.get("PATH", "")

# Install dependencies if needed
def ensure_deps():
    deps = [
        ("speech_recognition", "SpeechRecognition"),
        ("pyaudio", "pyaudio"),
        ("whisper", "openai-whisper"),
    ]
    for module, package in deps:
        try:
            __import__(module)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

ensure_deps()

import speech_recognition as sr
import whisper
import tempfile
import warnings
import wave
import numpy as np
import io

# Suppress whisper FP16 warning on CPU
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")


def normalize_audio(wav_data, gain=10.0):
    """
    Normalize audio: remove DC offset and amplify for better transcription.

    The Logitech C525 mic (index 18) captures speech at very low levels,
    so we amplify by default gain of 10x to reach usable levels for Whisper.

    Args:
        wav_data: Raw WAV bytes from audio.get_wav_data()
        gain: Amplification factor (default 10.0 for low-level mic)

    Returns:
        Corrected WAV bytes with DC offset removed and audio amplified
    """
    # Read the WAV data
    with io.BytesIO(wav_data) as wav_io:
        with wave.open(wav_io, 'rb') as wav:
            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            framerate = wav.getframerate()
            n_frames = wav.getnframes()
            raw_data = wav.readframes(n_frames)

    # Convert to numpy array
    samples = np.frombuffer(raw_data, dtype=np.int16).copy().astype(np.float64)

    # Remove DC offset (center around zero)
    samples = samples - samples.mean()

    # Amplify the audio (C525 mic has very low output levels)
    samples = samples * gain

    # Clip to valid range and convert back to int16
    samples = np.clip(samples, -32768, 32767).astype(np.int16)

    # Write back to WAV format
    output = io.BytesIO()
    with wave.open(output, 'wb') as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(sample_width)
        wav.setframerate(framerate)
        wav.writeframes(samples.tobytes())

    return output.getvalue()


# Alias for backwards compatibility
def remove_dc_offset(wav_data):
    """Backwards compatible alias for normalize_audio."""
    return normalize_audio(wav_data, gain=10.0)

# Global whisper models (loaded once)
_whisper_models = {}
_ambient_calibrated = False
_recognizer = None

def get_whisper_model(model_size="base"):
    """Load whisper model (cached). Supports multiple model sizes."""
    global _whisper_models
    if model_size not in _whisper_models:
        print(f"[Evie] Loading speech recognition model ({model_size})...")
        _whisper_models[model_size] = whisper.load_model(model_size)
        print(f"[Evie] Model '{model_size}' ready.")
    return _whisper_models[model_size]

def get_recognizer():
    """Get cached recognizer instance with optimized settings."""
    global _recognizer
    if _recognizer is None:
        _recognizer = sr.Recognizer()
        # Increase pause threshold to avoid cutting off mid-sentence
        _recognizer.pause_threshold = 1.5  # Wait 1.5 sec silence before stopping (default 0.8)
        _recognizer.non_speaking_duration = 0.8  # Minimum silence before stop
        _recognizer.dynamic_energy_threshold = True  # Auto-adjust to ambient
        _recognizer.energy_threshold = 400  # Starting threshold, higher = less sensitive
    return _recognizer

def list_microphones():
    """List available microphones."""
    print("\nAvailable Microphones:")
    print("-" * 40)
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  [{i}] {name}")
    print()

def listen_fixed(duration=3, mic_index=None, model_size="base", verbose=True, warmup=0.3):
    """
    Record audio for a fixed duration and transcribe with Whisper.

    This is more reliable than listen() which can have speech detection issues.
    Use this for wake word detection (short duration) and commands (longer duration).

    Args:
        duration: Seconds to record (default: 3 for wake words, use 8-10 for commands)
        mic_index: Specific microphone index (None = default)
        model_size: Whisper model size ("tiny", "base", "small")
        verbose: Print status messages
        warmup: Seconds to let mic stabilize before recording (default: 0.3)

    Returns:
        Transcribed text or empty string if nothing detected
    """
    recognizer = get_recognizer()
    mic_kwargs = {"device_index": mic_index} if mic_index is not None else {}

    try:
        with sr.Microphone(**mic_kwargs) as source:
            # Brief warmup to let mic stabilize (helps with DC offset issues)
            if warmup > 0:
                recognizer.adjust_for_ambient_noise(source, duration=warmup)

            if verbose:
                print(f"[Evie] Recording for {duration}s...")

            # Use record() with fixed duration - this is reliable
            audio = recognizer.record(source, duration=duration)

            # Transcribe with Whisper
            model = get_whisper_model(model_size)

            # Remove DC offset from audio (fixes mic bias issues that confuse Whisper)
            wav_data = remove_dc_offset(audio.get_wav_data())

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(wav_data)
                temp_path = f.name

            try:
                # Force English language to avoid DC offset causing wrong language detection
                result = model.transcribe(temp_path, fp16=False, language='en')
                text = result["text"].strip()
                # Filter out Whisper hallucinations on silence
                if text and not is_whisper_hallucination(text):
                    return text
                return ""
            finally:
                os.unlink(temp_path)

    except Exception as e:
        if verbose:
            print(f"[Evie] Error: {e}")
        return ""


def is_whisper_hallucination(text):
    """
    Check if Whisper output is a hallucination (common on silence/noise).
    Whisper sometimes generates these phrases when given silence.
    """
    hallucinations = [
        "thank you",
        "thanks for watching",
        "subscribe",
        "like and subscribe",
        "see you next time",
        "bye",
        "goodbye",
        "thank you for watching",
        "please subscribe",
        "...",
        "you",
        "the",
        # Additional patterns discovered during testing
        "?!?!",
        "a&m",
        "techn bi",
        "...",
        "。",
        "!",
        "?",
    ]
    text_lower = text.lower().strip()
    # Check exact matches or very short outputs
    if len(text_lower) < 3:
        return True
    # Check if text is mostly punctuation
    if len(text_lower.replace(".", "").replace("?", "").replace("!", "").strip()) < 2:
        return True
    for h in hallucinations:
        if text_lower == h or text_lower == h + ".":
            return True
    return False


def listen_once(timeout=5, phrase_limit=None, mic_index=None, use_whisper=True, model_size="base", verbose=True):
    """
    Listen for a single utterance and return transcribed text.

    Args:
        timeout: Max seconds to wait for speech to start
        phrase_limit: Max seconds of speech to capture
        mic_index: Specific microphone index (None = default)
        use_whisper: Use Whisper (True) or Google Speech API (False)
        model_size: Whisper model size ("tiny", "base", "small") - tiny is fastest
        verbose: Print status messages

    Returns:
        Transcribed text or None if failed
    """
    global _ambient_calibrated

    recognizer = get_recognizer()
    mic_kwargs = {"device_index": mic_index} if mic_index is not None else {}

    try:
        with sr.Microphone(**mic_kwargs) as source:
            # Only calibrate ambient noise once per session
            if not _ambient_calibrated:
                if verbose:
                    print("[Evie] Calibrating for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                _ambient_calibrated = True

            if verbose:
                print("[Evie] Listening...")
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_limit
            )

            if use_whisper:
                # Use Whisper for transcription
                model = get_whisper_model(model_size)

                # Remove DC offset from audio (fixes mic bias issues that confuse Whisper)
                wav_data = remove_dc_offset(audio.get_wav_data())

                # Save audio to temp file
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                    f.write(wav_data)
                    temp_path = f.name

                try:
                    # Force English language to avoid DC offset causing wrong language detection
                    result = model.transcribe(temp_path, fp16=False, language='en')
                    text = result["text"].strip()
                finally:
                    os.unlink(temp_path)
            else:
                # Use Google Speech Recognition (requires internet)
                text = recognizer.recognize_google(audio)

            return text

    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        if verbose:
            print(f"[Evie] Speech service error: {e}")
        return None
    except Exception as e:
        if verbose:
            print(f"[Evie] Error: {e}")
        return None

def listen_continuous(wake_word=None, exit_phrase="goodbye evie", mic_index=None):
    """
    Continuously listen and yield transcriptions.

    Args:
        wake_word: If set, only process after hearing this phrase
        exit_phrase: Stop listening when this is heard
        mic_index: Specific microphone index

    Yields:
        Transcribed text for each utterance
    """
    print(f"[Evie] Continuous listening mode.")
    if wake_word:
        print(f"[Evie] Say '{wake_word}' to activate.")
    print(f"[Evie] Say '{exit_phrase}' to stop.\n")

    waiting_for_wake = wake_word is not None

    while True:
        if waiting_for_wake:
            print("[Evie] Waiting for wake word...")

        text = listen_once(timeout=None, phrase_limit=15, mic_index=mic_index)

        if text is None:
            continue

        text_lower = text.lower().strip()

        # Check for exit
        if exit_phrase in text_lower:
            print("[Evie] Goodbye, love. Chat soon.")
            break

        # Check for wake word
        if waiting_for_wake:
            if wake_word.lower() in text_lower:
                print("[Evie] Yes, love? I'm listening...")
                waiting_for_wake = False
                # Remove wake word from text
                text = text_lower.replace(wake_word.lower(), "").strip()
                if text:
                    yield text
            continue

        # Normal mode - yield the text
        if text:
            print(f"[You said] {text}")
            yield text

        # Reset wake word requirement after each command
        if wake_word:
            waiting_for_wake = True

def main():
    parser = argparse.ArgumentParser(description="Evie Voice Listener")
    parser.add_argument("--continuous", "-c", action="store_true",
                       help="Continuous listening mode")
    parser.add_argument("--wake-word", "-w", default=None,
                       help="Wake word to activate (e.g., 'hey evie')")
    parser.add_argument("--timeout", "-t", type=int, default=5,
                       help="Seconds to wait for speech (default: 5)")
    parser.add_argument("--phrase-limit", "-p", type=int, default=None,
                       help="Max seconds of speech to capture")
    parser.add_argument("--mic", "-m", type=int, default=None,
                       help="Microphone index (use --list-mics to see options)")
    parser.add_argument("--list-mics", action="store_true",
                       help="List available microphones")
    parser.add_argument("--google", action="store_true",
                       help="Use Google Speech API instead of Whisper")

    args = parser.parse_args()

    if args.list_mics:
        list_microphones()
        return

    use_whisper = not args.google

    if args.continuous:
        for text in listen_continuous(
            wake_word=args.wake_word,
            mic_index=args.mic
        ):
            # In standalone mode, just print
            # When imported, the caller handles the text
            pass
    else:
        text = listen_once(
            timeout=args.timeout,
            phrase_limit=args.phrase_limit,
            mic_index=args.mic,
            use_whisper=use_whisper
        )
        if text:
            print(f"\n[Transcription] {text}")
            return text
        return None

if __name__ == "__main__":
    main()
