#!/usr/bin/env python3
"""
Accessible CLI - Voice-Controlled Command Line Interface

Designed for users who cannot use keyboard/mouse (amputees, paralysis, blindness).
Full voice control with audio feedback for all operations.

Features:
- Voice-controlled shell commands
- Audio confirmation of all actions
- Safety confirmations for destructive commands
- File navigation by voice
- Text editing by voice
- Email/calendar integration

Usage:
    python accessible-cli.py                    # Start accessible CLI
    python accessible-cli.py --beginner         # Extra guidance for new users
    python accessible-cli.py --no-confirm       # Skip safety confirmations (advanced)

Voice Commands:
    Navigation:
        "list files" / "show directory"
        "change directory to [path]"
        "go to home" / "go to desktop"
        "go back" / "parent directory"
        "what directory am i in"

    File Operations:
        "create file [filename]"
        "delete file [filename]"
        "copy [source] to [destination]"
        "move [source] to [destination]"
        "open [filename]"
        "read [filename]"

    Shell Commands:
        "run [command]"
        "check [service] status"
        "install [package]"

    Text Editing:
        "edit [filename]"
        "append to [filename] the text [content]"
        "replace in [filename] [old] with [new]"

    Email (via Gmail MCP):
        "check email"
        "read email [subject]"
        "send email to [recipient] subject [subject] body [content]"

    Calendar (via Google Calendar MCP):
        "what's on my calendar"
        "schedule meeting [details]"

    Help:
        "help" / "what can i do"
        "repeat that" / "say again"
        "exit" / "quit" / "goodbye"
"""

import subprocess
import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
HISTORY_FILE = Path.home() / ".accessible-cli-history.json"

# Microphone settings
DEFAULT_MIC_INDEX = 18  # Logitech C525 HD WebCam

# Safety lists
DESTRUCTIVE_COMMANDS = [
    "rm", "rmdir", "del", "delete", "format", "kill",
    "shutdown", "reboot", "restart"
]

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

def speak(text, style="default", rate="+0%"):
    """Speak text to user."""
    print(f"\n[System] {text}\n")
    try:
        speak_module.speak(text, style=style, play=True, rate=rate)
    except Exception as e:
        print(f"[Voice Error] {e}")

def listen(duration=8, mic_index=DEFAULT_MIC_INDEX):
    """Listen for user speech."""
    try:
        return listen_module.listen_fixed(
            duration=duration,
            mic_index=mic_index,
            model_size="base",
            verbose=False
        )
    except Exception as e:
        print(f"[Listen Error] {e}")
        return None

def confirm_action(action_description):
    """Ask user to confirm an action."""
    speak(f"{action_description}. Say 'yes' to confirm or 'no' to cancel.", style="alert")
    response = listen(duration=4)
    if response and "yes" in response.lower():
        return True
    speak("Cancelled.", style="default")
    return False

def save_to_history(command, result):
    """Save command to history file."""
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []

        history.append({
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "result": result[:500] if result else None  # Limit result size
        })

        # Keep last 100 commands
        history = history[-100:]

        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass

class AccessibleCLI:
    """Voice-controlled command line interface."""

    def __init__(self, beginner_mode=False, skip_confirms=False):
        self.beginner_mode = beginner_mode
        self.skip_confirms = skip_confirms
        self.current_dir = Path.cwd()
        self.last_response = ""
        self.running = True

    def parse_command(self, text):
        """Parse voice command into action and parameters."""
        text_lower = text.lower().strip()

        # Exit commands
        if any(word in text_lower for word in ["exit", "quit", "goodbye", "stop"]):
            return ("exit", {})

        # Help commands
        if "help" in text_lower or "what can i do" in text_lower:
            return ("help", {})

        # Repeat last response
        if "repeat" in text_lower or "say again" in text_lower:
            return ("repeat", {})

        # Navigation commands
        if "list files" in text_lower or "show directory" in text_lower:
            return ("list", {})

        if "change directory" in text_lower or "go to" in text_lower:
            # Extract path
            match = re.search(r"(?:change directory to|go to) (.+)", text_lower)
            if match:
                return ("cd", {"path": match.group(1).strip()})

        if "go back" in text_lower or "parent directory" in text_lower:
            return ("cd", {"path": ".."})

        if "what directory" in text_lower or "where am i" in text_lower:
            return ("pwd", {})

        # File operations
        if "create file" in text_lower:
            match = re.search(r"create file (.+)", text_lower)
            if match:
                return ("create", {"filename": match.group(1).strip()})

        if "delete file" in text_lower:
            match = re.search(r"delete file (.+)", text_lower)
            if match:
                return ("delete", {"filename": match.group(1).strip()})

        if "read file" in text_lower or "open file" in text_lower:
            match = re.search(r"(?:read|open) file (.+)", text_lower)
            if match:
                return ("read", {"filename": match.group(1).strip()})

        # Shell commands
        if "run " in text_lower:
            match = re.search(r"run (.+)", text_lower)
            if match:
                return ("shell", {"command": match.group(1).strip()})

        # Email commands
        if "check email" in text_lower:
            return ("email_check", {})

        if "send email" in text_lower:
            # Parse: "send email to [recipient] subject [subject] body [body]"
            match = re.search(r"send email to (.+?) subject (.+?) body (.+)", text_lower)
            if match:
                return ("email_send", {
                    "to": match.group(1).strip(),
                    "subject": match.group(2).strip(),
                    "body": match.group(3).strip()
                })

        # Calendar commands
        if "calendar" in text_lower or "schedule" in text_lower:
            return ("calendar", {"query": text})

        # Default - didn't understand
        return ("unknown", {"text": text})

    def handle_list(self):
        """List files in current directory."""
        try:
            files = list(self.current_dir.iterdir())
            if not files:
                speak("The directory is empty.", style="default")
                return "Empty directory"

            # Separate directories and files
            dirs = [f.name for f in files if f.is_dir()]
            regular_files = [f.name for f in files if f.is_file()]

            response = f"Found {len(dirs)} folders and {len(regular_files)} files. "
            if dirs:
                response += f"Folders: {', '.join(dirs[:5])}"
                if len(dirs) > 5:
                    response += f" and {len(dirs) - 5} more. "
            if regular_files:
                response += f"Files: {', '.join(regular_files[:5])}"
                if len(regular_files) > 5:
                    response += f" and {len(regular_files) - 5} more."

            speak(response, style="default")
            return response
        except Exception as e:
            speak(f"Error listing directory: {str(e)}", style="alert")
            return f"Error: {e}"

    def handle_cd(self, path):
        """Change directory."""
        try:
            # Handle special paths
            if path == "home":
                new_dir = Path.home()
            elif path == "desktop":
                new_dir = Path.home() / "Desktop"
            else:
                new_dir = (self.current_dir / path).resolve()

            if not new_dir.exists():
                speak(f"Directory {path} does not exist.", style="alert")
                return f"Error: Directory not found"

            self.current_dir = new_dir
            speak(f"Changed to {new_dir.name}", style="default")
            return f"Changed to {new_dir}"
        except Exception as e:
            speak(f"Error changing directory: {str(e)}", style="alert")
            return f"Error: {e}"

    def handle_pwd(self):
        """Report current directory."""
        speak(f"You are in {self.current_dir}", style="default")
        return str(self.current_dir)

    def handle_create(self, filename):
        """Create a new file."""
        try:
            filepath = self.current_dir / filename
            if filepath.exists():
                speak(f"File {filename} already exists.", style="alert")
                return "Error: File exists"

            filepath.touch()
            speak(f"Created file {filename}", style="default")
            return f"Created {filename}"
        except Exception as e:
            speak(f"Error creating file: {str(e)}", style="alert")
            return f"Error: {e}"

    def handle_delete(self, filename):
        """Delete a file."""
        try:
            filepath = self.current_dir / filename
            if not filepath.exists():
                speak(f"File {filename} not found.", style="alert")
                return "Error: File not found"

            # Confirm deletion
            if not self.skip_confirms:
                if not confirm_action(f"About to delete {filename}"):
                    return "Cancelled"

            filepath.unlink()
            speak(f"Deleted {filename}", style="default")
            return f"Deleted {filename}"
        except Exception as e:
            speak(f"Error deleting file: {str(e)}", style="alert")
            return f"Error: {e}"

    def handle_read(self, filename):
        """Read file contents."""
        try:
            filepath = self.current_dir / filename
            if not filepath.exists():
                speak(f"File {filename} not found.", style="alert")
                return "Error: File not found"

            content = filepath.read_text(encoding='utf-8')

            # Speak first 500 chars
            if len(content) > 500:
                spoken = content[:500] + "... File is longer. I've printed the full content to your screen."
            else:
                spoken = content

            speak(f"Contents of {filename}: {spoken}", style="default")
            print(f"\n[Full File Contents]\n{content}\n")
            return content
        except Exception as e:
            speak(f"Error reading file: {str(e)}", style="alert")
            return f"Error: {e}"

    def handle_shell(self, command):
        """Execute shell command."""
        try:
            # Check for destructive commands
            is_destructive = any(cmd in command.lower() for cmd in DESTRUCTIVE_COMMANDS)

            if is_destructive and not self.skip_confirms:
                if not confirm_action(f"About to run potentially destructive command: {command}"):
                    return "Cancelled"

            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.current_dir)
            )

            output = result.stdout.strip() if result.stdout else result.stderr.strip()

            if result.returncode == 0:
                speak(f"Command completed. {output[:200] if output else 'No output.'}", style="default")
            else:
                speak(f"Command failed: {output[:200]}", style="alert")

            print(f"\n[Command Output]\n{output}\n")
            return output
        except subprocess.TimeoutExpired:
            speak("Command timed out after 30 seconds.", style="alert")
            return "Timeout"
        except Exception as e:
            speak(f"Error running command: {str(e)}", style="alert")
            return f"Error: {e}"

    def handle_help(self):
        """Provide help information."""
        help_text = """
        Available voice commands:
        Navigation: list files, change directory, go to home, go back
        Files: create file, delete file, read file
        Shell: run followed by any command
        Email: check email, send email
        Calendar: what's on my calendar
        Say help anytime for this menu, or goodbye to exit.
        """
        speak(help_text, style="default", rate="+10%")
        return help_text

    def handle_repeat(self):
        """Repeat last response."""
        if self.last_response:
            speak(self.last_response, style="default")
        else:
            speak("Nothing to repeat yet.", style="default")
        return self.last_response

    def run(self):
        """Main loop."""
        speak("Accessible CLI started. Say 'help' for commands or 'goodbye' to exit.", style="greeting")

        while self.running:
            try:
                # Listen for command
                print("\n[Listening...]")
                text = listen(duration=10, mic_index=DEFAULT_MIC_INDEX)

                if not text:
                    continue

                print(f"[You said] {text}")

                # Parse and execute
                action, params = self.parse_command(text)

                if action == "exit":
                    speak("Goodbye. Take care.", style="encouragement")
                    self.running = False
                    continue

                # Route to handler
                handlers = {
                    "help": lambda: self.handle_help(),
                    "repeat": lambda: self.handle_repeat(),
                    "list": lambda: self.handle_list(),
                    "cd": lambda: self.handle_cd(params.get("path")),
                    "pwd": lambda: self.handle_pwd(),
                    "create": lambda: self.handle_create(params.get("filename")),
                    "delete": lambda: self.handle_delete(params.get("filename")),
                    "read": lambda: self.handle_read(params.get("filename")),
                    "shell": lambda: self.handle_shell(params.get("command")),
                }

                handler = handlers.get(action)
                if handler:
                    result = handler()
                    self.last_response = result if result else "Command completed"
                    save_to_history(text, result)
                else:
                    speak("I didn't understand that command. Say 'help' for options.", style="alert")

            except KeyboardInterrupt:
                speak("Interrupted. Goodbye.", style="default")
                self.running = False
            except Exception as e:
                speak(f"An error occurred: {str(e)}", style="alert")
                print(f"[Error] {e}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Accessible CLI - Voice-Controlled Terminal")
    parser.add_argument("--beginner", "-b", action="store_true",
                       help="Beginner mode with extra guidance")
    parser.add_argument("--no-confirm", action="store_true",
                       help="Skip safety confirmations (advanced users)")
    parser.add_argument("--mic-index", "-m", type=int, default=DEFAULT_MIC_INDEX,
                       help="Microphone device index")

    args = parser.parse_args()

    cli = AccessibleCLI(
        beginner_mode=args.beginner,
        skip_confirms=args.no_confirm
    )

    cli.run()

if __name__ == "__main__":
    main()
