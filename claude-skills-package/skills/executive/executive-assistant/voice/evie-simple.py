#!/usr/bin/env python3
"""
Evie Simple - Voice Assistant (Standalone)

A simplified voice assistant that responds to common queries without
needing Claude Code integration. Perfect for quick hands-free tasks.

Usage:
    python evie-simple.py
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Paths
SCRIPT_DIR = Path(__file__).parent
DEFAULT_MIC_INDEX = 18

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

def listen(duration=8):
    """Listen for user speech."""
    try:
        return listen_module.listen_fixed(
            duration=duration,
            mic_index=DEFAULT_MIC_INDEX,
            model_size="base",
            verbose=False
        )
    except Exception as e:
        print(f"[Listen Error] {e}")
        return None

def handle_time():
    """Get current time."""
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")
    day_str = now.strftime("%A, %B %d")
    response = f"It's {time_str} on {day_str}."
    speak(response)
    return response

def handle_list_files():
    """List files in current directory."""
    try:
        files = list(Path.cwd().iterdir())
        if not files:
            speak("The directory is empty.")
            return "Empty"

        dirs = [f.name for f in files if f.is_dir()]
        regular_files = [f.name for f in files if f.is_file()]

        response = f"Found {len(dirs)} folders and {len(regular_files)} files. "
        if dirs[:3]:
            response += f"Folders include: {', '.join(dirs[:3])}. "
        if regular_files[:3]:
            response += f"Files include: {', '.join(regular_files[:3])}."

        speak(response)
        return response
    except Exception as e:
        speak(f"Error: {str(e)}")
        return f"Error: {e}"

def handle_directory():
    """Report current directory."""
    cwd = Path.cwd()
    response = f"You are in {cwd.name}"
    speak(response)
    return str(cwd)

def handle_shell_command(command):
    """Execute a shell command."""
    try:
        speak(f"Running {command}")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout.strip() if result.stdout else result.stderr.strip()

        if result.returncode == 0:
            # Success
            if output:
                response = f"Command completed. {output[:200]}"
            else:
                response = "Command completed successfully."
        else:
            response = f"Command failed: {output[:200]}"

        speak(response)
        print(f"\n[Full Output]\n{output}\n")
        return output
    except subprocess.TimeoutExpired:
        speak("Command timed out after 30 seconds.")
        return "Timeout"
    except Exception as e:
        speak(f"Error: {str(e)}")
        return f"Error: {e}"

def handle_read_file(filename):
    """Read a file."""
    try:
        filepath = Path.cwd() / filename
        if not filepath.exists():
            speak(f"File {filename} not found.")
            return "Not found"

        content = filepath.read_text(encoding='utf-8')

        # Speak first 300 chars
        if len(content) > 300:
            spoken = content[:300] + "... File is longer, full content is on screen."
        else:
            spoken = content

        speak(f"Contents of {filename}: {spoken}")
        print(f"\n[Full File]\n{content}\n")
        return content
    except Exception as e:
        speak(f"Error reading file: {str(e)}")
        return f"Error: {e}"

def parse_command(text):
    """Parse voice command."""
    text_lower = text.lower().strip()

    # Exit
    if any(word in text_lower for word in ["goodbye", "exit", "quit", "stop"]):
        return ("exit", {})

    # Help
    if "help" in text_lower:
        return ("help", {})

    # Time
    if "time" in text_lower or "what time" in text_lower:
        return ("time", {})

    # List files
    if "list files" in text_lower or "show files" in text_lower:
        return ("list", {})

    # Current directory
    if "directory" in text_lower and "am i" in text_lower:
        return ("pwd", {})

    # Run command
    if "run " in text_lower:
        import re
        match = re.search(r"run (.+)", text_lower)
        if match:
            return ("shell", {"command": match.group(1).strip()})

    # Read file
    if "read file" in text_lower or "read " in text_lower:
        import re
        match = re.search(r"read (?:file )?(.+)", text_lower)
        if match:
            return ("read", {"filename": match.group(1).strip()})

    # Unknown
    return ("unknown", {"text": text})

def run_assistant():
    """Main loop."""
    print("=" * 60)
    print("Evie - Voice Assistant")
    print("=" * 60)
    print("Say 'help' for commands or 'goodbye' to exit")
    print("=" * 60)

    speak("Hello love. I'm Evie. What can I help you with?", style="greeting")

    while True:
        try:
            print("\n[Listening...]")
            text = listen(duration=8)

            if not text:
                continue

            print(f"[You said] {text}")

            action, params = parse_command(text)

            if action == "exit":
                speak("Goodbye love. Take care.", style="encouragement")
                break
            elif action == "help":
                help_text = "I can help with: telling time, listing files, showing current directory, running commands, or reading files. Say goodbye when you're done."
                speak(help_text)
            elif action == "time":
                handle_time()
            elif action == "list":
                handle_list_files()
            elif action == "pwd":
                handle_directory()
            elif action == "shell":
                handle_shell_command(params["command"])
            elif action == "read":
                handle_read_file(params["filename"])
            elif action == "unknown":
                speak("I didn't quite catch that. Try saying: time, list files, run command, or read file.", style="alert")

        except KeyboardInterrupt:
            speak("Interrupted. Goodbye love.", style="default")
            break
        except Exception as e:
            print(f"[Error] {e}")
            speak("Sorry, I had a hiccup. Let's try again.")

if __name__ == "__main__":
    run_assistant()
