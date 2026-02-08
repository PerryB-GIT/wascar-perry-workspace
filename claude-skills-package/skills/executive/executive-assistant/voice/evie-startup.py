#!/usr/bin/env python3
"""
Evie Startup Service - Always-Listening Voice Assistant

This script runs Evie in the background, listening for wake words:
- "Hey Evie"
- "Good morning Evie"
- "Good afternoon Evie"
- "Good evening Evie"

When activated, Evie captures your command and can respond via the Claude Code session.
"""

import subprocess
import sys
import os
import json
import datetime
import signal
import atexit
from pathlib import Path

# Paths
EVIE_DIR = Path(__file__).parent
SKILLS_DIR = EVIE_DIR.parent
CLAUDE_DIR = Path.home() / ".claude"
PID_FILE = CLAUDE_DIR / "evie.pid"
LOG_FILE = CLAUDE_DIR / "evie.log"
COMMAND_FILE = CLAUDE_DIR / "evie-command.json"

# Wake word variants
WAKE_WORDS = [
    "hey evie",
    "good morning evie",
    "good afternoon evie",
    "good evening evie",
    "evie",
    "yo evie",
    "hi evie",
    "hello evie",
]

# Microphone settings
# Index 18 = Logitech C525 HD WebCam (correct endpoint with actual speech, not noise)
# Note: Index 8 captures high levels but it's noise/interference, not speech
DEFAULT_MIC_INDEX = 18

# Model settings for speed optimization
# "tiny" is 3x faster than "base" - good for wake word detection
# "base" is more accurate - use for command transcription
WAKE_WORD_MODEL = "tiny"
COMMAND_MODEL = "base"

# Greeting response when activated
def get_greeting():
    return "Yes dear, I am here to serve."

def log(msg):
    """Log message with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {msg}"
    print(log_line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    except Exception:
        pass

def cleanup():
    """Remove PID file on exit."""
    if PID_FILE.exists():
        PID_FILE.unlink()
    log("Evie shutdown complete.")

def save_command(text, wake_word_used):
    """Save captured command for Claude Code to pick up."""
    command_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "text": text,
        "wake_word": wake_word_used,
        "processed": False
    }
    with open(COMMAND_FILE, "w", encoding="utf-8") as f:
        json.dump(command_data, f, indent=2)
    log(f"Command saved: {text}")

def is_wake_word(text):
    """Check if text contains a wake word."""
    text_lower = text.lower().strip()
    for wake in WAKE_WORDS:
        if wake in text_lower:
            return wake
    return None

def run_listener():
    """Run the continuous listener with wake word detection."""
    # Import the listener module
    sys.path.insert(0, str(EVIE_DIR))

    try:
        from evie_listen import listen_fixed, get_whisper_model
    except ImportError:
        # Try alternate import
        import importlib.util
        spec = importlib.util.spec_from_file_location("evie_listen", EVIE_DIR / "evie-listen.py")
        evie_listen = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(evie_listen)
        listen_fixed = evie_listen.listen_fixed
        get_whisper_model = evie_listen.get_whisper_model

    # Preload both models for instant switching
    log("Loading speech models...")
    get_whisper_model(WAKE_WORD_MODEL)  # Fast model for wake words
    get_whisper_model(COMMAND_MODEL)    # Accurate model for commands

    log("Evie is now listening for wake words...")
    log(f"Say any of: {', '.join(WAKE_WORDS)}")

    waiting_for_command = False
    active_wake_word = None

    # Recording durations
    WAKE_WORD_DURATION = 3   # Short recordings for wake word detection
    COMMAND_DURATION = 8     # Longer recordings for commands

    while True:
        try:
            # Choose model and duration based on state
            if waiting_for_command:
                current_model = COMMAND_MODEL
                duration = COMMAND_DURATION
            else:
                current_model = WAKE_WORD_MODEL
                duration = WAKE_WORD_DURATION

            # Record fixed-duration audio (reliable method)
            text = listen_fixed(
                duration=duration,
                mic_index=DEFAULT_MIC_INDEX,
                model_size=current_model,
                verbose=False
            )

            if not text:
                continue

            text_lower = text.lower().strip()

            # Check for exit commands
            if "goodbye evie" in text_lower or "stop listening" in text_lower:
                log("Exit command received.")
                break

            if waiting_for_command:
                # We already got the wake word, this is the command
                save_command(text, active_wake_word)

                # Speak acknowledgment
                try:
                    speak_script = EVIE_DIR / "evie-speak-edge.py"
                    subprocess.run([
                        sys.executable, str(speak_script),
                        "Got it, love. Let me work on that.",
                        "--style", "casual",
                        "--play"
                    ], check=False)
                except Exception as e:
                    log(f"Speak error: {e}")

                waiting_for_command = False
                active_wake_word = None
                continue

            # Check for wake word
            wake = is_wake_word(text)
            if wake:
                log(f"Wake word detected: {wake}")
                active_wake_word = wake

                # Extract command if it came with the wake word
                command_text = text_lower.replace(wake, "").strip()

                if command_text and len(command_text) > 3:
                    # Command included with wake word
                    save_command(command_text, wake)

                    try:
                        speak_script = EVIE_DIR / "evie-speak-edge.py"
                        subprocess.run([
                            sys.executable, str(speak_script),
                            "On it, love.",
                            "--style", "casual",
                            "--play"
                        ], check=False)
                    except Exception:
                        pass
                else:
                    # Just wake word, wait for command
                    waiting_for_command = True

                    # Respond to greeting
                    try:
                        speak_script = EVIE_DIR / "evie-speak-edge.py"
                        greeting = get_greeting()
                        subprocess.run([
                            sys.executable, str(speak_script),
                            greeting,
                            "--style", "greeting",
                            "--play"
                        ], check=False)
                    except Exception as e:
                        log(f"Speak error: {e}")

        except KeyboardInterrupt:
            log("Interrupted by user.")
            break
        except Exception as e:
            log(f"Error: {e}")
            continue

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Evie Startup Service")
    parser.add_argument("--daemon", "-d", action="store_true",
                       help="Run as background daemon")
    parser.add_argument("--stop", "-s", action="store_true",
                       help="Stop running daemon")
    parser.add_argument("--status", action="store_true",
                       help="Check if Evie is running")
    args = parser.parse_args()

    if args.status:
        if PID_FILE.exists():
            pid = int(PID_FILE.read_text().strip())
            print(f"Evie is running (PID: {pid})")
        else:
            print("Evie is not running")
        return

    if args.stop:
        if PID_FILE.exists():
            pid = int(PID_FILE.read_text().strip())
            try:
                if sys.platform == "win32":
                    subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                                   capture_output=True, check=True)
                else:
                    os.kill(pid, signal.SIGTERM)
                print(f"Stopped Evie (PID: {pid})")
            except (ProcessLookupError, subprocess.CalledProcessError, OSError):
                print("Evie process not found, cleaning up...")
            PID_FILE.unlink()
        else:
            print("Evie is not running")
        return

    # Check if already running
    if PID_FILE.exists():
        pid = int(PID_FILE.read_text().strip())
        try:
            # Cross-platform process check
            if sys.platform == "win32":
                import ctypes
                kernel32 = ctypes.windll.kernel32
                handle = kernel32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
                if handle:
                    kernel32.CloseHandle(handle)
                    print(f"Evie is already running (PID: {pid})")
                    return
                # Process doesn't exist
                PID_FILE.unlink()
            else:
                os.kill(pid, 0)  # Unix: Check if process exists
                print(f"Evie is already running (PID: {pid})")
                return
        except (ProcessLookupError, OSError):
            PID_FILE.unlink()  # Stale PID file

    # Write PID file
    PID_FILE.write_text(str(os.getpid()))
    atexit.register(cleanup)

    log("=" * 50)
    log("Evie Voice Assistant Starting")
    log("=" * 50)

    if args.daemon:
        # Run in background (on Windows, use pythonw)
        log("Running in daemon mode...")

    run_listener()

if __name__ == "__main__":
    main()
