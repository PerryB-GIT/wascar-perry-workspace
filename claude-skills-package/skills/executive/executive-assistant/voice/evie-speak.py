#!/usr/bin/env python3
"""
Evie Voice Generator - Azure Speech SDK
Warm British EA voice inspired by Evie Hammond

Usage:
    python evie-speak.py "Hello, love. How are you today?"
    python evie-speak.py --style alert "This needs your attention!"
    python evie-speak.py --save output.wav "Your meeting starts in 15 minutes."
"""

import subprocess
import sys
import json
import argparse
from pathlib import Path

# Check for Azure SDK
try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("Installing Azure Speech SDK...")
    subprocess.run([sys.executable, "-m", "pip", "install", "azure-cognitiveservices-speech"], check=True)
    import azure.cognitiveservices.speech as speechsdk

import os

# Configuration
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "evie-voice-config.json"

# Load voice config
with open(CONFIG_FILE) as f:
    CONFIG = json.load(f)

def get_speech_config():
    """Get Azure Speech configuration from environment."""
    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION", "eastus")

    if not key:
        # Try loading from credentials file
        cred_file = Path.home() / ".credentials" / "azure-speech.json"
        if cred_file.exists():
            with open(cred_file) as f:
                creds = json.load(f)
                key = creds.get("key")
                region = creds.get("region", region)

    if not key:
        print("ERROR: Azure Speech key not found!")
        print("\nSet up credentials:")
        print("  1. Go to https://portal.azure.com")
        print("  2. Create a Speech resource (free tier available)")
        print("  3. Copy Key 1 and Region")
        print("  4. Set environment variables:")
        print("     export AZURE_SPEECH_KEY='your-key'")
        print("     export AZURE_SPEECH_REGION='eastus'")
        print("\n  Or create ~/.credentials/azure-speech.json:")
        print('     {"key": "your-key", "region": "eastus"}')
        sys.exit(1)

    return speechsdk.SpeechConfig(subscription=key, region=region)

def build_ssml(text: str, style: str = "default") -> str:
    """Build SSML with Evie's voice characteristics."""

    voice = CONFIG["voice_id"]
    base_config = CONFIG["ssml_config"]

    # Get style-specific overrides
    style_config = CONFIG["ssml_templates"].get(style, {})

    rate = style_config.get("rate", base_config["rate"])
    pitch = style_config.get("pitch", base_config["pitch"])
    voice_style = style_config.get("style", base_config["style"])
    style_degree = base_config.get("style_degree", "1.0")

    ssml = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-GB">
    <voice name="{voice}">
        <mstts:express-as style="{voice_style}" styledegree="{style_degree}">
            <prosody rate="{rate}" pitch="{pitch}">
                {text}
            </prosody>
        </mstts:express-as>
    </voice>
</speak>'''

    return ssml

def speak(text: str, style: str = "default", output_file: str = None):
    """Speak text with Evie's voice."""

    speech_config = get_speech_config()
    speech_config.speech_synthesis_voice_name = CONFIG["voice_id"]

    # Configure output
    if output_file:
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
    else:
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    # Build SSML
    ssml = build_ssml(text, style)

    # Synthesize
    print(f"[Evie speaking{'...' if not output_file else f' → {output_file}'}]")
    result = synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("✓ Done")
        return True
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print(f"✗ Error: {cancellation.reason}")
        if cancellation.error_details:
            print(f"  Details: {cancellation.error_details}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Evie Voice Generator")
    parser.add_argument("text", nargs="?", help="Text for Evie to speak")
    parser.add_argument("--style", "-s", default="default",
                       choices=["default", "greeting", "alert", "encouragement", "urgent"],
                       help="Speaking style")
    parser.add_argument("--save", "-o", help="Save to WAV file instead of speaking")
    parser.add_argument("--demo", action="store_true", help="Run demo with sample phrases")
    parser.add_argument("--list-samples", action="store_true", help="List sample phrases")

    args = parser.parse_args()

    if args.list_samples:
        print("\nEvie's Sample Phrases:")
        print("-" * 40)
        for name, phrase in CONFIG["sample_phrases"].items():
            print(f"  {name}: \"{phrase}\"")
        return

    if args.demo:
        print("\n🎭 Evie Voice Demo")
        print("=" * 40)
        samples = [
            ("greeting", CONFIG["sample_phrases"]["morning_greeting"]),
            ("default", CONFIG["sample_phrases"]["meeting_reminder"]),
            ("encouragement", CONFIG["sample_phrases"]["encouragement"]),
            ("alert", CONFIG["sample_phrases"]["critical_alert"]),
        ]
        for style, text in samples:
            print(f"\nStyle: {style}")
            print(f"Text: \"{text}\"")
            speak(text, style)
            input("Press Enter for next...")
        return

    if not args.text:
        # Default intro
        text = "Good morning, love. I'm Evie, your executive assistant. I'll be keeping you organised, on track, and well looked after. Shall we get started?"
    else:
        text = args.text

    speak(text, args.style, args.save)

if __name__ == "__main__":
    main()
