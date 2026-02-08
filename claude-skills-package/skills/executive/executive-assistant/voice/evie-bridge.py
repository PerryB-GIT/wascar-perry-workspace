#!/usr/bin/env python3
"""
Evie Bridge - Direct Voice to Claude Code Interface

Listens continuously → Sends to Claude Code → Speaks response
Perfect for hands-free interaction with Claude.

Usage:
    python evie-bridge.py                    # Start voice bridge
    python evie-bridge.py --wake-word        # Require "Hey Claude" to activate
    python evie-bridge.py --no-confirm       # Skip confirmation sounds
"""

import subprocess
import sys
import os
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
CLAUDE_CLI = "claude"  # Assumes claude is in PATH

# Wake word for activation
DEFAULT_WAKE_WORD = "hey claude"

# Microphone settings (from working tests)
DEFAULT_MIC_INDEX = 18  # Logitech C525 HD WebCam

# Import Evie's voice modules
sys.path.insert(0, str(SCRIPT_DIR))

def load_module(module_file):
    """Load a Python module from a file with dashes in the name."""
    import importlib.util
    module_name = module_file.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, module_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load Evie's listen and speak modules
listen_module = load_module(SCRIPT_DIR / "evie-listen.py")
speak_module = load_module(SCRIPT_DIR / "evie-speak-edge.py")

def speak(text, style="default"):
    """Have Evie speak text."""
    print(f"\n[Evie] {text}\n")
    try:
        speak_module.speak(text, style=style, play=True)
    except Exception as e:
        print(f"[Voice Error] {e}")

def listen(duration=8, mic_index=DEFAULT_MIC_INDEX, model="base"):
    """Listen for user speech."""
    try:
        return listen_module.listen_fixed(
            duration=duration,
            mic_index=mic_index,
            model_size=model,
            verbose=False
        )
    except Exception as e:
        print(f"[Listen Error] {e}")
        return None

def send_to_claude(text):
    """
    Send text to Claude Code and get response.

    Uses a temporary file approach since direct piping can be tricky.
    """
    try:
        # Create temp file with the query
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(text)
            temp_file = f.name

        # Call Claude with the query
        # Using --quiet flag to minimize noise
        result = subprocess.run(
            ["claude", "code", text],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60
        )

        # Clean up temp file
        try:
            os.unlink(temp_file)
        except:
            pass

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"

    except subprocess.TimeoutExpired:
        return "I'm sorry, that took too long. Let's try something simpler."
    except Exception as e:
        return f"I encountered an error: {str(e)}"

def run_bridge(wake_word=None, confirm_sounds=True):
    """
    Run the voice bridge.

    Args:
        wake_word: Optional wake word to require before processing (e.g., "hey claude")
        confirm_sounds: Play confirmation sounds for actions
    """
    print("=" * 60)
    print("Evie Bridge - Direct Voice to Claude Code")
    print("=" * 60)
    print(f"Wake word: {wake_word or 'None (always listening)'}")
    print(f"Microphone: Index {DEFAULT_MIC_INDEX}")
    print("Say 'goodbye' or 'stop listening' to exit")
    print("=" * 60)

    speak("Hello love. I'm connected directly to Claude. What would you like to know?", style="greeting")

    waiting_for_wake = bool(wake_word)

    while True:
        try:
            # Listen for speech
            if waiting_for_wake:
                print(f"\n[Listening for '{wake_word}'...]")
                duration = 4  # Shorter for wake word detection
            else:
                print("\n[Listening...]")
                duration = 8  # Longer for full queries

            text = listen(duration=duration, mic_index=DEFAULT_MIC_INDEX)

            if not text:
                continue

            text_lower = text.lower().strip()
            print(f"[You said] {text}")

            # Check for exit commands
            if any(word in text_lower for word in ["goodbye", "stop listening", "exit", "quit"]):
                speak("Alright love, signing off. Take care.", style="encouragement")
                break

            # If waiting for wake word
            if waiting_for_wake:
                if wake_word.lower() in text_lower:
                    if confirm_sounds:
                        speak("Yes?", style="greeting")
                    waiting_for_wake = False
                continue

            # Process the command
            if confirm_sounds:
                speak("Let me think about that.", style="default")

            # Send to Claude
            print("[Sending to Claude...]")
            response = send_to_claude(text)
            print(f"[Claude's response]\n{response}\n")

            # Speak the response
            # Limit to first 500 chars for reasonable speech length
            if len(response) > 500:
                spoken_response = response[:500] + "... I've sent the full response to your screen."
            else:
                spoken_response = response

            speak(spoken_response, style="default")

            # If using wake word, go back to waiting
            if wake_word:
                waiting_for_wake = True

        except KeyboardInterrupt:
            print("\n[Interrupted]")
            speak("Interrupted. Goodbye love.", style="default")
            break
        except Exception as e:
            print(f"[Error] {e}")
            speak("Sorry, I had a hiccup. Let's try that again.", style="alert")
            continue

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Evie Bridge - Voice to Claude Code")
    parser.add_argument("--wake-word", "-w", type=str, default=None,
                       help="Require wake word before processing (e.g., 'hey claude')")
    parser.add_argument("--no-confirm", action="store_true",
                       help="Skip confirmation sounds")
    parser.add_argument("--mic-index", "-m", type=int, default=DEFAULT_MIC_INDEX,
                       help="Microphone device index")

    args = parser.parse_args()

    run_bridge(
        wake_word=args.wake_word,
        confirm_sounds=not args.no_confirm
    )

if __name__ == "__main__":
    main()
