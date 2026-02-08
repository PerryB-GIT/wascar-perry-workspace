#!/usr/bin/env python3
"""
Voice-to-Claude - Full AI Voice Assistant

Direct voice conversation with Claude AI (Sonnet 4.5).
Uses Anthropic API for true conversational intelligence.

Usage:
    python voice-to-claude.py
    python voice-to-claude.py --model opus    # Use Claude Opus 4.6
    python voice-to-claude.py --stream        # Stream responses (faster)

Features:
- Full conversational AI via Anthropic API
- Context retention across conversation
- Evie's British voice for responses
- Smart response summarization for long answers
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json

# Check for anthropic library
try:
    import anthropic
except ImportError:
    print("Installing anthropic library...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "anthropic"], check=True)
    import anthropic

# Paths
SCRIPT_DIR = Path(__file__).parent
CONVERSATION_FILE = Path.home() / ".voice-claude-history.json"

# API Configuration
API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_API_KEY_HERE")
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"
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

class VoiceClaudeAssistant:
    """Voice assistant powered by Claude AI."""

    def __init__(self, model=DEFAULT_MODEL, stream=False):
        self.model = model
        self.stream = stream
        self.client = anthropic.Anthropic(api_key=API_KEY)
        self.conversation_history = []
        self.running = True
        self.system_prompt = """You are Evie, Perry's executive assistant with a warm British personality.

Key traits:
- Professional yet friendly, with a touch of warmth
- Direct and concise - no unnecessary pleasantries
- Use terms of endearment sparingly ("love", "darling") only when appropriate
- Focus on being helpful and efficient
- When answers are long, prioritize the most important information first

Response guidelines:
- Keep responses under 3 sentences when possible
- For complex topics, give a brief answer first, then offer to elaborate
- Use clear, conversational language
- Show personality but stay professional"""

        # Load previous conversation if exists
        self.load_history()

    def load_history(self):
        """Load conversation history from file."""
        try:
            if CONVERSATION_FILE.exists():
                with open(CONVERSATION_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Only keep last 10 exchanges (20 messages) to avoid token limits
                    self.conversation_history = data.get("messages", [])[-20:]
                    print(f"[Loaded {len(self.conversation_history)} previous messages]")
        except Exception as e:
            print(f"[Could not load history: {e}]")

    def save_history(self):
        """Save conversation history to file."""
        try:
            data = {
                "last_updated": datetime.now().isoformat(),
                "messages": self.conversation_history
            }
            with open(CONVERSATION_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[Could not save history: {e}]")

    def ask_claude(self, user_message):
        """Send message to Claude and get response."""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })

            print(f"[Thinking...]")

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=self.system_prompt,
                messages=self.conversation_history
            )

            # Extract response text
            assistant_message = response.content[0].text

            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            # Save updated history
            self.save_history()

            return assistant_message

        except anthropic.APIError as e:
            error_msg = f"API Error: {str(e)}"
            print(f"[Error] {error_msg}")
            return f"Sorry love, I encountered an API error: {str(e)}"
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"[Error] {error_msg}")
            return f"Sorry, something went wrong: {str(e)}"

    def process_response_for_speech(self, text):
        """
        Process Claude's response for optimal speech output.

        If response is very long, speak a summary and note that
        the full response is on screen.
        """
        # Remove markdown code blocks for speech (but keep in printed version)
        import re

        # Count words
        word_count = len(text.split())

        # If very long (>150 words), create a summary
        if word_count > 150:
            # Take first 2-3 sentences as summary
            sentences = re.split(r'(?<=[.!?])\s+', text)
            summary = ' '.join(sentences[:3])

            return summary + " ... I've put the full answer on your screen for reference."

        return text

    def run(self):
        """Main conversation loop."""
        print("=" * 60)
        print("Voice-to-Claude - Full AI Assistant")
        print("=" * 60)
        print(f"Model: {self.model}")
        print("Say 'goodbye' or 'stop' to exit")
        print("=" * 60)

        speak("Hello love, I'm Evie, powered by Claude. What can I help you with?", style="greeting")

        while self.running:
            try:
                # Listen for user input
                print("\n[Listening...]")
                user_text = listen(duration=10)

                if not user_text:
                    continue

                # Clean up the text
                user_text = user_text.strip()
                print(f"\n[You] {user_text}")

                # Check for exit commands
                if any(word in user_text.lower() for word in ["goodbye", "bye bye", "stop", "exit", "quit"]):
                    speak("Goodbye love. Take care.", style="encouragement")
                    self.running = False
                    break

                # Check for history reset
                if "clear history" in user_text.lower() or "reset conversation" in user_text.lower():
                    self.conversation_history = []
                    self.save_history()
                    speak("Memory cleared. Starting fresh.", style="default")
                    continue

                # Get Claude's response
                response = self.ask_claude(user_text)

                # Print full response
                print(f"\n[Claude] {response}\n")

                # Process for speech (may summarize if long)
                spoken_response = self.process_response_for_speech(response)

                # Speak the response
                speak(spoken_response, style="default")

            except KeyboardInterrupt:
                speak("Interrupted. Goodbye love.", style="default")
                self.running = False
            except Exception as e:
                print(f"[Error] {e}")
                speak("Sorry, I had a hiccup. Let's try again.", style="alert")

        # Final save
        self.save_history()
        print(f"\n[Conversation saved to {CONVERSATION_FILE}]")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Voice-to-Claude - Full AI Voice Assistant")
    parser.add_argument("--model", "-m", type=str, default=DEFAULT_MODEL,
                       choices=[
                           "claude-sonnet-4-5-20250929",
                           "claude-opus-4-6",
                           "claude-haiku-4-5-20251001"
                       ],
                       help="Claude model to use")
    parser.add_argument("--stream", "-s", action="store_true",
                       help="Stream responses (experimental)")
    parser.add_argument("--clear-history", action="store_true",
                       help="Clear conversation history and start fresh")

    args = parser.parse_args()

    # Clear history if requested
    if args.clear_history:
        if CONVERSATION_FILE.exists():
            CONVERSATION_FILE.unlink()
            print("[History cleared]")

    # Start assistant
    assistant = VoiceClaudeAssistant(
        model=args.model,
        stream=args.stream
    )

    assistant.run()


if __name__ == "__main__":
    main()
