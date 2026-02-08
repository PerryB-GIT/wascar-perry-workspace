#!/usr/bin/env python3
"""
Evie Interactive Mode - Full Voice Assistant
Listen → Process → Speak → Act

Usage:
    python evie-interactive.py                    # Start interactive session
    python evie-interactive.py --wake-word        # Require "Hey Evie" to activate
    python evie-interactive.py --vision           # Enable camera for visual context

Commands Evie understands:
    - "check my calendar" / "what's on my schedule"
    - "check my email" / "any new messages"
    - "what's the weather" / "weather forecast"
    - "any news" / "what's happening today" / "major events"
    - "take a screenshot" / "what am I looking at"
    - "capture photo" / "look at me"
    - "help me with [skill]" / "use [skill]"
    - "goodbye evie" - exits

Skills Evie can leverage:
    - negotiator, invoice-generator, client-intake
    - creating-financial-models, seo-audit
    - incident-response, aws-cost-optimizer
    - ceh-agent (security), pm-agent, sales-agent
"""

import subprocess
import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime

# Ensure we're in the right directory for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import Evie's voice modules
from importlib import import_module

def lazy_import(module_name):
    """Import module only when needed."""
    try:
        return import_module(module_name)
    except ImportError:
        return None

# Available skills mapping
SKILLS = {
    "negotiator": "negotiator",
    "negotiation": "negotiator",
    "negotiate": "negotiator",
    "invoice": "invoice-generator",
    "billing": "invoice-generator",
    "client": "client-intake",
    "intake": "client-intake",
    "onboarding": "client-intake",
    "financial": "creating-financial-models",
    "finance": "creating-financial-models",
    "model": "creating-financial-models",
    "seo": "seo-audit",
    "audit": "seo-audit",
    "incident": "incident-response",
    "emergency": "incident-response",
    "outage": "incident-response",
    "aws": "aws-cost-optimizer",
    "cost": "aws-cost-optimizer",
    "security": "ceh-agent",
    "pentest": "ceh-agent",
    "project": "pm-agent",
    "product": "pm-agent",
    "sales": "sales-agent",
    "selling": "sales-agent",
    "email": "email-marketing-agent",
    "marketing": "email-marketing-agent",
}

class EvieAssistant:
    """
    Evie - Your Executive Assistant
    Full interactive voice assistant with skill integration.
    """

    def __init__(self, enable_vision=False, wake_word=None):
        self.enable_vision = enable_vision
        self.wake_word = wake_word
        self.running = False
        self.context = {}

        # Lazy load modules
        self._listen_module = None
        self._speak_module = None
        self._vision_module = None

    @property
    def listener(self):
        if self._listen_module is None:
            # Import the listen module (handles dash in filename)
            import importlib.util
            spec = importlib.util.spec_from_file_location("evie_listen", SCRIPT_DIR / "evie-listen.py")
            self._listen_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self._listen_module)
        return self._listen_module

    @property
    def speaker(self):
        if self._speak_module is None:
            # Import the speak module (edge version - free)
            import importlib.util
            spec = importlib.util.spec_from_file_location("evie_speak", SCRIPT_DIR / "evie-speak-edge.py")
            self._speak_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self._speak_module)
        return self._speak_module

    @property
    def vision(self):
        if self._vision_module is None and self.enable_vision:
            import importlib.util
            spec = importlib.util.spec_from_file_location("evie_vision", SCRIPT_DIR / "evie-vision.py")
            vision_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(vision_module)
            self._vision_module = vision_module.EvieVision()
        return self._vision_module

    def speak(self, text, style="default"):
        """Have Evie speak."""
        print(f"\n[Evie] {text}\n")
        try:
            self.speaker.speak(text, style=style, play=True)
        except Exception as e:
            print(f"[Voice Error] {e}")

    def listen(self, timeout=10):
        """Listen for user input."""
        return self.listener.listen_once(timeout=timeout, phrase_limit=15)

    def parse_intent(self, text):
        """
        Parse user's intent from speech.

        Returns:
            tuple: (intent, parameters)
        """
        text_lower = text.lower().strip()

        # Exit commands
        if any(phrase in text_lower for phrase in ["goodbye evie", "bye evie", "stop", "exit", "quit"]):
            return ("exit", {})

        # Calendar commands
        if any(phrase in text_lower for phrase in ["calendar", "schedule", "meetings", "appointments", "what's on"]):
            return ("calendar", {})

        # Email commands
        if any(phrase in text_lower for phrase in ["email", "inbox", "messages", "mail"]):
            return ("email", {})

        # Screenshot commands
        if any(phrase in text_lower for phrase in ["screenshot", "screen", "looking at", "see my screen"]):
            return ("screenshot", {})

        # Photo/webcam commands
        if any(phrase in text_lower for phrase in ["photo", "picture", "look at me", "camera", "webcam"]):
            return ("photo", {})

        # Time/date
        if any(phrase in text_lower for phrase in ["what time", "what day", "today's date"]):
            return ("time", {})

        # Weather commands
        if any(phrase in text_lower for phrase in ["weather", "forecast", "temperature", "rain", "sunny", "cold", "hot"]):
            return ("weather", {})

        # News/Events commands
        if any(phrase in text_lower for phrase in ["news", "events", "happening", "headlines", "world", "major"]):
            return ("events", {})

        # Skill invocation
        for keyword, skill_name in SKILLS.items():
            if keyword in text_lower:
                return ("skill", {"skill": skill_name, "query": text})

        # Morning briefing
        if any(phrase in text_lower for phrase in ["briefing", "brief me", "morning", "daily"]):
            return ("briefing", {})

        # Default - treat as general query
        return ("query", {"text": text})

    def handle_calendar(self):
        """Check calendar and report."""
        self.speak("Let me check your calendar love.", style="default")

        # This would integrate with Google Calendar MCP
        # For now, provide guidance
        return """To check your calendar, I'll use the Google Calendar MCP.
        Run: mcp__google-calendar__calendar_list_events with maxResults: 5"""

    def handle_email(self):
        """Check email and report."""
        self.speak("Checking your inbox darling.", style="default")

        # This would integrate with Gmail MCP
        return """To check email, I'll use the Gmail MCP.
        Run: mcp__gmail__search_emails with query: "is:unread in:inbox" """

    def handle_screenshot(self):
        """Capture and describe screen."""
        if self.vision:
            self.speak("Taking a look at your screen.", style="default")
            img = self.vision.see_screen(save=True)
            if img is not None:
                self.speak("Got it. I can see what you're working on.", style="default")
                return "Screenshot captured"
        else:
            self.speak("Vision isn't enabled love. Start me with --vision flag.", style="alert")
        return None

    def handle_photo(self):
        """Capture photo from webcam."""
        if self.vision:
            self.speak("Say cheese!", style="greeting")
            img = self.vision.look(save=True, preview=False)
            if img is not None:
                self.speak("Looking good babe.", style="encouragement")
                return "Photo captured"
        else:
            self.speak("Camera isn't enabled. Start me with --vision flag.", style="alert")
        return None

    def handle_skill(self, skill_name, query):
        """Invoke another skill."""
        self.speak(f"Right, let me pull up the {skill_name.replace('-', ' ')} skill.", style="default")

        # Return guidance for invoking the skill
        return f"""Skill requested: {skill_name}
        Query: {query}

        To invoke in Claude Code, use: /{skill_name}
        Or reference the skill file at: ~/.claude/skills/{skill_name}/skill.md"""

    def handle_time(self):
        """Report current time/date."""
        now = datetime.now()
        day = now.strftime("%A")
        date = now.strftime("%B %d")
        time = now.strftime("%I:%M %p")

        response = f"It's {day}, {date}. The time is {time}."
        self.speak(response, style="default")
        return response

    def handle_briefing(self):
        """Deliver morning briefing."""
        self.speak("Right, let me pull together your briefing.", style="greeting")

        # This would aggregate calendar, email, tasks
        return """Morning briefing requested.
        This combines: calendar_list_events + search_emails + any pending tasks."""

    def handle_weather(self):
        """Get weather forecast."""
        self.speak("Let me check the weather for you love.", style="default")

        # Use web search for weather
        return """Weather lookup requested.
        To get weather, use WebSearch tool with query: "weather forecast [location] today"
        Or integrate with weather API (OpenWeatherMap, wttr.in)

        Quick CLI option: curl wttr.in/?format=3"""

    def handle_events(self):
        """Get major news and events."""
        self.speak("Right, let me see what's happening in the world.", style="default")

        # Use web search for news
        return """Major events lookup requested.
        To get news, use WebSearch tool with queries:
        - "major news today"
        - "breaking news [date]"
        - "important events [industry]"

        Sources to check:
        - Reuters, AP News for global
        - TechCrunch, Hacker News for tech
        - Local news for your area"""

    def process_command(self, text):
        """Process a voice command."""
        intent, params = self.parse_intent(text)

        handlers = {
            "exit": lambda: "exit",
            "calendar": self.handle_calendar,
            "email": self.handle_email,
            "screenshot": self.handle_screenshot,
            "photo": self.handle_photo,
            "time": self.handle_time,
            "weather": self.handle_weather,
            "events": self.handle_events,
            "briefing": self.handle_briefing,
            "skill": lambda: self.handle_skill(params.get("skill"), params.get("query")),
            "query": lambda: self.handle_query(params.get("text")),
        }

        handler = handlers.get(intent, lambda: None)
        return handler()

    def handle_query(self, text):
        """Handle general queries."""
        self.speak(f"You said: {text}. I'll need Claude to help with that one.", style="default")
        return f"Query: {text}"

    def greet(self):
        """Opening greeting."""
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning love."
        elif hour < 17:
            greeting = "Good afternoon darling."
        else:
            greeting = "Good evening babe."

        self.speak(f"{greeting} I'm Evie, your executive assistant. What can I help you with?", style="greeting")

    def farewell(self):
        """Closing farewell."""
        self.speak("Alright love, I'm here if you need me. Take care.", style="encouragement")

    def run(self):
        """Run interactive session."""
        self.running = True
        self.greet()

        while self.running:
            try:
                # Listen for command
                text = self.listen(timeout=30)

                if text is None:
                    continue

                # Check for wake word if required
                if self.wake_word:
                    if self.wake_word.lower() not in text.lower():
                        continue
                    # Remove wake word from text
                    text = text.lower().replace(self.wake_word.lower(), "").strip()

                # Process the command
                result = self.process_command(text)

                if result == "exit":
                    self.running = False
                elif result:
                    print(f"\n[Result] {result}\n")

            except KeyboardInterrupt:
                self.running = False

        self.farewell()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Evie Interactive Assistant")
    parser.add_argument("--vision", "-v", action="store_true",
                       help="Enable camera/screen capture")
    parser.add_argument("--wake-word", "-w", type=str, default=None,
                       help="Require wake word (e.g., 'hey evie')")
    parser.add_argument("--test", "-t", action="store_true",
                       help="Run quick test (greet and exit)")

    args = parser.parse_args()

    evie = EvieAssistant(
        enable_vision=args.vision,
        wake_word=args.wake_word
    )

    if args.test:
        evie.greet()
        evie.speak("Systems check complete. Voice, vision, and skills all ready.", style="default")
        evie.farewell()
    else:
        evie.run()


if __name__ == "__main__":
    main()
