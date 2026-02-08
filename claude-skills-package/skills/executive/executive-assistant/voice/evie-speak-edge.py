#!/usr/bin/env python3
"""
Evie Voice Generator - Edge TTS (Free, no API key needed)
Natural conversational British voice with SSML prosody

Usage:
    python evie-speak-edge.py "Hello, love."
    python evie-speak-edge.py --play "Your meeting is in 15 minutes."
    python evie-speak-edge.py --save greeting.mp3 "Good morning, darling."
    python evie-speak-edge.py --natural "I will check that for you"  # Auto-converts to natural speech
"""

import subprocess
import sys
import asyncio
import argparse
import re
import random
from pathlib import Path
import tempfile

# Install edge-tts if needed
try:
    import edge_tts
except ImportError:
    print("Installing edge-tts...")
    subprocess.run([sys.executable, "-m", "pip", "install", "edge-tts"], check=True)
    import edge_tts

# Evie's voices - British English
EVIE_VOICE = "en-GB-SoniaNeural"  # Warm, professional British female
CONVERSATIONAL_VOICE = "en-GB-LibbyNeural"  # More casual, friendly

# Natural speech patterns - contractions and casual forms
NATURAL_CONTRACTIONS = {
    r"\bI am\b": "I'm",
    r"\bI will\b": "I'll",
    r"\bI would\b": "I'd",
    r"\bI have\b": "I've",
    r"\byou are\b": "you're",
    r"\byou will\b": "you'll",
    r"\byou would\b": "you'd",
    r"\byou have\b": "you've",
    r"\bwe are\b": "we're",
    r"\bwe will\b": "we'll",
    r"\bwe have\b": "we've",
    r"\bthey are\b": "they're",
    r"\bthey will\b": "they'll",
    r"\bthey have\b": "they've",
    r"\bit is\b": "it's",
    r"\bit will\b": "it'll",
    r"\bthat is\b": "that's",
    r"\bthat will\b": "that'll",
    r"\bwhat is\b": "what's",
    r"\bwho is\b": "who's",
    r"\bhere is\b": "here's",
    r"\bthere is\b": "there's",
    r"\bdo not\b": "don't",
    r"\bdoes not\b": "doesn't",
    r"\bdid not\b": "didn't",
    r"\bwill not\b": "won't",
    r"\bwould not\b": "wouldn't",
    r"\bcould not\b": "couldn't",
    r"\bshould not\b": "shouldn't",
    r"\bcannot\b": "can't",
    r"\bcan not\b": "can't",
    r"\bhave not\b": "haven't",
    r"\bhas not\b": "hasn't",
    r"\bhad not\b": "hadn't",
    r"\bis not\b": "isn't",
    r"\bare not\b": "aren't",
    r"\bwas not\b": "wasn't",
    r"\bwere not\b": "weren't",
    r"\blet us\b": "let's",
    r"\bgoing to\b": "gonna",  # Very casual - use sparingly
}

# British conversational fillers (used sparingly for naturalness)
BRITISH_FILLERS = [
    "right, ",
    "so, ",
    "well, ",
    "look, ",
    "okay, ",
]

# Voice styling - more varied and natural
VOICE_CONFIG = {
    "default": {
        "rate": "+5%",
        "pitch": "-2Hz",
        "voice": EVIE_VOICE,
    },
    "casual": {
        "rate": "+3%",
        "pitch": "+0Hz",
        "voice": CONVERSATIONAL_VOICE,
    },
    "greeting": {
        "rate": "+2%",
        "pitch": "+2Hz",
        "voice": CONVERSATIONAL_VOICE,
    },
    "warm": {
        "rate": "-2%",
        "pitch": "-3Hz",
        "voice": EVIE_VOICE,
    },
    "alert": {
        "rate": "+12%",
        "pitch": "+3Hz",
        "voice": EVIE_VOICE,
    },
    "encouragement": {
        "rate": "+0%",
        "pitch": "-2Hz",
        "voice": CONVERSATIONAL_VOICE,
    },
    "urgent": {
        "rate": "+18%",
        "pitch": "+5Hz",
        "voice": EVIE_VOICE,
    },
    "thinking": {
        "rate": "-5%",
        "pitch": "-3Hz",
        "voice": EVIE_VOICE,
    },
    "playful": {
        "rate": "+8%",
        "pitch": "+5Hz",
        "voice": CONVERSATIONAL_VOICE,
    },
}


def naturalize_text(text: str, add_filler: bool = False) -> str:
    """
    Convert formal text to natural conversational speech.
    Adds contractions and optionally British conversational fillers.
    """
    result = text

    # Apply contractions (case-insensitive)
    for pattern, replacement in NATURAL_CONTRACTIONS.items():
        # Handle both cases
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        # Preserve capitalization for sentence starts
        result = re.sub(
            pattern.replace(r"\b", r"\b").upper(),
            replacement.capitalize() if replacement[0].islower() else replacement,
            result
        )

    # Optionally add a conversational filler at the start (20% chance)
    if add_filler and random.random() < 0.2:
        # Only add filler if sentence doesn't already start casually
        if not any(result.lower().startswith(f) for f in BRITISH_FILLERS):
            filler = random.choice(BRITISH_FILLERS[:3])  # Use milder fillers
            result = filler.capitalize() + result[0].lower() + result[1:]

    return result


def add_natural_pauses(text: str) -> str:
    """
    Add SSML breaks for natural speech rhythm.
    Converts punctuation and phrases to include micro-pauses.
    """
    # Add slight pause after commas (natural breath)
    text = re.sub(r',\s*', ', <break time="150ms"/> ', text)

    # Add pause after colons
    text = re.sub(r':\s*', ': <break time="200ms"/> ', text)

    # Add pause after em-dashes for dramatic effect
    text = re.sub(r'\s*—\s*', ' <break time="300ms"/> ', text)
    text = re.sub(r'\s*--\s*', ' <break time="300ms"/> ', text)

    # Add slight pause before "but", "and", "or" for natural flow
    text = re.sub(r'\s+(but|and|or)\s+', r' <break time="100ms"/> \1 ', text, flags=re.IGNORECASE)

    # Add pause after introductory phrases
    intro_phrases = [
        r"^(Right),",
        r"^(So),",
        r"^(Well),",
        r"^(Look),",
        r"^(Okay),",
        r"^(Now),",
    ]
    for phrase in intro_phrases:
        text = re.sub(phrase, r'\1, <break time="200ms"/>', text, flags=re.IGNORECASE)

    return text


def add_emphasis(text: str) -> str:
    """
    Add SSML emphasis to key words for natural prosody.
    """
    # Emphasize words in caps (but not acronyms)
    def emphasize_caps(match):
        word = match.group(0)
        if len(word) > 3:  # Likely intentional emphasis, not acronym
            return f'<emphasis level="moderate">{word.capitalize()}</emphasis>'
        return word

    text = re.sub(r'\b[A-Z]{4,}\b', emphasize_caps, text)

    # Emphasize words with asterisks: *important*
    text = re.sub(r'\*(\w+)\*', r'<emphasis level="strong">\1</emphasis>', text)

    # Slight emphasis on key action words
    action_words = ['now', 'urgent', 'important', 'critical', 'please', 'need', 'must']
    for word in action_words:
        text = re.sub(
            rf'\b({word})\b',
            r'<emphasis level="moderate">\1</emphasis>',
            text,
            flags=re.IGNORECASE
        )

    return text


def build_ssml(text: str, style: str = "default", natural: bool = True) -> str:
    """
    Build full SSML markup for natural speech.
    """
    config = VOICE_CONFIG.get(style, VOICE_CONFIG["default"])

    if natural:
        # Apply naturalizations
        text = naturalize_text(text, add_filler=(style in ["casual", "greeting", "playful"]))
        text = add_natural_pauses(text)
        text = add_emphasis(text)

    # Build SSML
    ssml = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-GB">
    <voice name="{config['voice']}">
        <prosody rate="{config['rate']}" pitch="{config['pitch']}">
            {text}
        </prosody>
    </voice>
</speak>'''

    return ssml


async def generate_speech(text: str, output_file: str, style: str = "default", use_ssml: bool = False):
    """Generate speech with Evie's voice."""
    config = VOICE_CONFIG.get(style, VOICE_CONFIG["default"])

    if use_ssml:
        # SSML mode - text should already be SSML formatted
        communicate = edge_tts.Communicate(
            text,
            config["voice"],
        )
    else:
        # Simple mode with rate/pitch
        communicate = edge_tts.Communicate(
            text,
            config["voice"],
            rate=config["rate"],
            pitch=config["pitch"]
        )

    await communicate.save(output_file)
    return output_file


async def generate_natural_speech(text: str, output_file: str, style: str = "default"):
    """Generate natural-sounding speech with preprocessing."""
    config = VOICE_CONFIG.get(style, VOICE_CONFIG["default"])

    # Apply naturalizations
    natural_text = naturalize_text(text, add_filler=(style in ["casual", "greeting", "playful"]))

    communicate = edge_tts.Communicate(
        natural_text,
        config["voice"],
        rate=config["rate"],
        pitch=config["pitch"]
    )

    await communicate.save(output_file)
    return output_file


def play_audio(file_path: str):
    """Play audio file using system default player."""
    import platform

    system = platform.system()
    if system == "Windows":
        # Use Windows Media Player or default
        subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{file_path}').PlaySync()"], check=True)
    elif system == "Darwin":  # macOS
        subprocess.run(["afplay", file_path], check=True)
    else:  # Linux
        subprocess.run(["aplay", file_path], check=True)


def speak(text: str, style: str = "default", output_file: str = None, play: bool = True, natural: bool = True):
    """Speak text with Evie's voice."""

    # Determine output file
    if output_file:
        out_path = output_file
        should_cleanup = False
    else:
        # Use temp file
        temp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        out_path = temp.name
        temp.close()
        should_cleanup = play  # Only cleanup if we're playing

    print(f"[Evie speaking...]")

    # Generate audio with natural speech
    if natural:
        asyncio.run(generate_natural_speech(text, out_path, style))
    else:
        asyncio.run(generate_speech(text, out_path, style))

    if output_file:
        print(f"[OK] Saved to: {output_file}")

    if play:
        # Convert to wav for Windows playback
        wav_path = out_path.replace(".mp3", ".wav")
        try:
            # Try ffmpeg first
            result = subprocess.run(
                ["ffmpeg", "-y", "-i", out_path, "-ar", "22050", wav_path],
                capture_output=True
            )
            if result.returncode == 0:
                play_audio(wav_path)
                Path(wav_path).unlink(missing_ok=True)
            else:
                # Fallback: use PowerShell with Windows Media Player
                subprocess.run([
                    "powershell", "-c",
                    f"Add-Type -AssemblyName presentationCore; $player = New-Object System.Windows.Media.MediaPlayer; $player.Open('{out_path}'); Start-Sleep -Milliseconds 500; $player.Play(); while($player.Position -lt $player.NaturalDuration.TimeSpan) {{ Start-Sleep -Milliseconds 100 }}; $player.Close()"
                ], check=True)
        except FileNotFoundError:
            # No ffmpeg, try direct
            print("(Install ffmpeg for better audio playback)")
            subprocess.run([
                "powershell", "-c",
                f"Add-Type -AssemblyName presentationCore; $player = New-Object System.Windows.Media.MediaPlayer; $player.Open('{out_path}'); Start-Sleep -Milliseconds 500; $player.Play(); while($player.Position -lt $player.NaturalDuration.TimeSpan) {{ Start-Sleep -Milliseconds 100 }}; $player.Close()"
            ], check=True)

    if should_cleanup:
        Path(out_path).unlink(missing_ok=True)

    print("[OK] Done")


def main():
    parser = argparse.ArgumentParser(description="Evie Voice (Edge TTS - Natural British)")
    parser.add_argument("text", nargs="?", help="Text for Evie to speak")
    parser.add_argument("--style", "-s", default="default",
                       choices=list(VOICE_CONFIG.keys()),
                       help="Speaking style")
    parser.add_argument("--save", "-o", help="Save to MP3 file")
    parser.add_argument("--play", "-p", action="store_true", default=True,
                       help="Play audio (default: True)")
    parser.add_argument("--no-play", action="store_true", help="Don't play, just save")
    parser.add_argument("--no-natural", action="store_true",
                       help="Disable natural speech processing")
    parser.add_argument("--list-voices", action="store_true", help="List available British voices")
    parser.add_argument("--list-styles", action="store_true", help="List available speaking styles")

    args = parser.parse_args()

    if args.list_voices:
        print("\nAvailable British Female Voices:")
        print("-" * 40)
        voices = [
            ("en-GB-SoniaNeural", "Warm, professional (Evie's main voice)"),
            ("en-GB-LibbyNeural", "Friendly, conversational (casual mode)"),
            ("en-GB-MaisieNeural", "Young, energetic"),
        ]
        for voice, desc in voices:
            print(f"  {voice}: {desc}")
        return

    if args.list_styles:
        print("\nAvailable Speaking Styles:")
        print("-" * 40)
        style_descriptions = {
            "default": "Standard professional warmth",
            "casual": "Relaxed, conversational",
            "greeting": "Welcoming, friendly",
            "warm": "Slower, intimate",
            "alert": "Attention-getting",
            "encouragement": "Supportive, caring",
            "urgent": "Fast, important",
            "thinking": "Thoughtful, measured",
            "playful": "Light, teasing",
        }
        for style, desc in style_descriptions.items():
            print(f"  {style}: {desc}")
        return

    if not args.text:
        text = "Good morning, love. I'm Evie, your executive assistant. I'll be keeping you organised, on track, and well looked after. Shall we get started?"
    else:
        text = args.text

    play = not args.no_play
    natural = not args.no_natural
    speak(text, args.style, args.save, play, natural)


if __name__ == "__main__":
    main()
