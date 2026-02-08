#!/usr/bin/env python3
"""
Evie Proactive Intelligence - Life Events & Relationship Management
Tracks birthdays, anniversaries, and important dates with smart suggestions

Usage:
    python evie-proactive.py                    # Check for upcoming events
    python evie-proactive.py --days 30          # Look ahead 30 days
    python evie-proactive.py --research "Jacob Bailes"  # Research a person
    python evie-proactive.py --add-birthday "Mom" "03-15"  # Add birthday
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import argparse

# Contacts file location
SCRIPT_DIR = Path(__file__).parent
CONTACTS_FILE = SCRIPT_DIR / "evie-contacts.json"

def load_contacts() -> dict:
    """Load contacts from JSON file."""
    if CONTACTS_FILE.exists():
        with open(CONTACTS_FILE, 'r') as f:
            return json.load(f)
    return {
        "owner": {},
        "family": [],
        "associates": [],
        "events": [],
        "preferences": {
            "default_reminder_days": [14, 7, 1],
            "auto_research": True,
            "suggest_gifts": True,
            "suggest_restaurants": True,
            "suggest_ecards": True,
            "suggest_social_posts": True
        }
    }

def save_contacts(data: dict):
    """Save contacts to JSON file."""
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_upcoming_events(days_ahead: int = 30) -> List[Dict]:
    """Get events occurring in the next N days."""
    contacts = load_contacts()
    today = datetime.now()
    upcoming = []

    for event in contacts.get("events", []):
        if event.get("recurring"):
            # Parse MM-DD format
            try:
                month, day = map(int, event["date"].split("-"))
                # Create date for this year
                event_date = datetime(today.year, month, day)
                # If already passed this year, use next year
                if event_date < today:
                    event_date = datetime(today.year + 1, month, day)

                days_until = (event_date - today).days
                if 0 <= days_until <= days_ahead:
                    upcoming.append({
                        **event,
                        "date_obj": event_date,
                        "days_until": days_until
                    })
            except ValueError:
                continue
        else:
            # One-time event with full date
            try:
                event_date = datetime.strptime(event["date"], "%Y-%m-%d")
                days_until = (event_date - today).days
                if 0 <= days_until <= days_ahead:
                    upcoming.append({
                        **event,
                        "date_obj": event_date,
                        "days_until": days_until
                    })
            except ValueError:
                continue

    # Sort by days until
    upcoming.sort(key=lambda x: x["days_until"])
    return upcoming

def get_person_info(name: str) -> Optional[Dict]:
    """Get info about a family member or associate."""
    contacts = load_contacts()
    name_lower = name.lower()

    # Check family
    for person in contacts.get("family", []):
        if name_lower in person.get("name", "").lower():
            return {**person, "category": "family"}

    # Check associates
    for person in contacts.get("associates", []):
        if name_lower in person.get("name", "").lower():
            return {**person, "category": "associate"}

    return None

def generate_gift_research_queries(person: Dict) -> List[str]:
    """Generate web search queries for gift research."""
    name = person.get("name", "Unknown")
    full_name = person.get("full_name", name)
    relationship = person.get("relationship", "person")
    interests = person.get("interests", [])

    queries = [
        f"gift ideas for {relationship} 2026",
        f"best birthday gifts for {relationship}",
        f"unique {relationship} birthday gift ideas",
        f"personalized gifts for {relationship}",
    ]

    # Add interest-based queries
    for interest in interests:
        queries.append(f"{interest} gift ideas")
        queries.append(f"best {interest} gifts 2026")

    return queries

def generate_suggestions(event: Dict, person: Optional[Dict] = None) -> Dict:
    """Generate proactive suggestions for an event."""
    suggestions = {
        "overview": "",
        "gifts": [],
        "restaurants": [],
        "ecards": [],
        "social_posts": [],
        "research_queries": []
    }

    event_type = event.get("type", "event")
    person_name = event.get("person", person.get("name") if person else "them")
    days_until = event.get("days_until", 0)

    # Overview
    if days_until == 0:
        suggestions["overview"] = f"🎉 Today is {person_name}'s {event_type}!"
    elif days_until == 1:
        suggestions["overview"] = f"⏰ {person_name}'s {event_type} is tomorrow!"
    else:
        suggestions["overview"] = f"📅 {person_name}'s {event_type} is in {days_until} days"

    # Gift suggestions
    if event.get("suggestions", {}).get("gifts", True):
        suggestions["gifts"] = [
            f"Research {person_name}'s interests and recent activities",
            "Check their Amazon wishlist if they have one",
            "Consider experience gifts (concert tickets, spa day, etc.)",
            "Personalized items (engraved, custom photo, etc.)",
            "Gift cards to their favorite stores",
        ]
        if person:
            suggestions["research_queries"] = generate_gift_research_queries(person)

    # Restaurant suggestions
    if event.get("suggestions", {}).get("dinner", True):
        suggestions["restaurants"] = [
            f"Book a table at {person_name}'s favorite restaurant",
            "Try a new highly-rated restaurant they'd enjoy",
            "Consider a private dining experience",
            "Check OpenTable for availability",
        ]

    # E-card suggestions
    if event.get("suggestions", {}).get("ecards", True):
        suggestions["ecards"] = [
            "Send a heartfelt e-card via JibJab or Hallmark",
            "Create a custom video message",
            "Send a digital gift card with personalized note",
            "Create a photo collage or video montage",
        ]

    # Social post suggestions
    if event.get("suggestions", {}).get("social_post", True):
        suggestions["social_posts"] = [
            f"Draft a heartfelt birthday post for {person_name}",
            "Gather photos for a tribute post",
            "Consider a throwback photo with meaningful caption",
            "Tag them in a celebration story",
        ]

    return suggestions

def format_event_briefing(event: Dict, suggestions: Dict) -> str:
    """Format event into a briefing message."""
    lines = [
        f"\n{'='*50}",
        suggestions["overview"],
        f"{'='*50}\n"
    ]

    if suggestions.get("gifts"):
        lines.append("🎁 **Gift Ideas:**")
        for gift in suggestions["gifts"][:3]:
            lines.append(f"  • {gift}")
        lines.append("")

    if suggestions.get("restaurants"):
        lines.append("🍽️ **Dinner Options:**")
        for restaurant in suggestions["restaurants"][:2]:
            lines.append(f"  • {restaurant}")
        lines.append("")

    if suggestions.get("ecards"):
        lines.append("💌 **Digital Gestures:**")
        for ecard in suggestions["ecards"][:2]:
            lines.append(f"  • {ecard}")
        lines.append("")

    if suggestions.get("social_posts"):
        lines.append("📱 **Social Media:**")
        for post in suggestions["social_posts"][:2]:
            lines.append(f"  • {post}")
        lines.append("")

    if suggestions.get("research_queries"):
        lines.append("🔍 **Research Queries:**")
        for query in suggestions["research_queries"][:3]:
            lines.append(f"  • WebSearch: \"{query}\"")
        lines.append("")

    return "\n".join(lines)

def add_family_member(name: str, relationship: str, birthday: str = None) -> bool:
    """Add a new family member."""
    contacts = load_contacts()

    new_member = {
        "name": name,
        "full_name": name,
        "relationship": relationship,
        "birthday": birthday,
        "interests": [],
        "notes": ""
    }

    contacts["family"].append(new_member)

    # Add birthday event if provided
    if birthday:
        contacts["events"].append({
            "name": f"{name}'s Birthday",
            "date": birthday,
            "recurring": True,
            "type": "birthday",
            "person": name,
            "reminder_days": [30, 14, 7, 3, 1],
            "suggestions": {
                "gifts": True,
                "dinner": True,
                "ecards": True,
                "social_post": True
            }
        })

    save_contacts(contacts)
    return True

def add_event(name: str, date: str, event_type: str, person: str = None, recurring: bool = True) -> bool:
    """Add a new event."""
    contacts = load_contacts()

    new_event = {
        "name": name,
        "date": date,
        "recurring": recurring,
        "type": event_type,
        "person": person,
        "reminder_days": [14, 7, 1],
        "suggestions": {
            "gifts": event_type == "birthday",
            "dinner": True,
            "ecards": True,
            "social_post": True
        }
    }

    contacts["events"].append(new_event)
    save_contacts(contacts)
    return True

def check_upcoming(days: int = 30, speak: bool = False) -> str:
    """Check for upcoming events and return briefing."""
    upcoming = get_upcoming_events(days)

    if not upcoming:
        return f"No events in the next {days} days. All clear, love."

    briefings = []
    for event in upcoming:
        person = get_person_info(event.get("person", ""))
        suggestions = generate_suggestions(event, person)
        briefings.append(format_event_briefing(event, suggestions))

    header = f"📅 **Upcoming Events ({len(upcoming)} in next {days} days)**\n"
    return header + "\n".join(briefings)

def main():
    parser = argparse.ArgumentParser(description="Evie Proactive Intelligence")
    parser.add_argument("--days", "-d", type=int, default=30,
                       help="Days to look ahead (default: 30)")
    parser.add_argument("--research", "-r", type=str,
                       help="Research a person for gift ideas")
    parser.add_argument("--add-family", nargs=3, metavar=("NAME", "RELATIONSHIP", "BIRTHDAY"),
                       help="Add family member (birthday as MM-DD)")
    parser.add_argument("--add-event", nargs=4, metavar=("NAME", "DATE", "TYPE", "PERSON"),
                       help="Add event (date as MM-DD for recurring)")
    parser.add_argument("--list-contacts", action="store_true",
                       help="List all contacts")

    args = parser.parse_args()

    if args.list_contacts:
        contacts = load_contacts()
        print("\n👨‍👩‍👧‍👦 **Family:**")
        for person in contacts.get("family", []):
            print(f"  • {person['name']} ({person.get('relationship', 'family')}) - Birthday: {person.get('birthday', 'not set')}")
        print("\n👥 **Associates:**")
        for person in contacts.get("associates", []):
            print(f"  • {person['name']} - Birthday: {person.get('birthday', 'not set')}")
        print("\n📅 **Events:**")
        for event in contacts.get("events", []):
            print(f"  • {event['name']} - {event['date']} ({'recurring' if event.get('recurring') else 'one-time'})")
        return

    if args.add_family:
        name, relationship, birthday = args.add_family
        add_family_member(name, relationship, birthday)
        print(f"Added {name} ({relationship}) with birthday {birthday}")
        return

    if args.add_event:
        name, date, event_type, person = args.add_event
        add_event(name, date, event_type, person)
        print(f"Added event: {name} on {date} for {person}")
        return

    if args.research:
        person = get_person_info(args.research)
        if person:
            queries = generate_gift_research_queries(person)
            print(f"\n🔍 **Research Queries for {person['name']}:**\n")
            for q in queries:
                print(f"  • {q}")
        else:
            # Search for this person online
            print(f"\n🔍 **Research {args.research}:**")
            print(f"  • WebSearch: \"{args.research} interests hobbies\"")
            print(f"  • WebSearch: \"{args.research} birthday gift ideas\"")
            print(f"  • WebSearch: \"{args.research} favorite things\"")
        return

    # Default: check upcoming events
    briefing = check_upcoming(args.days)
    print(briefing)

if __name__ == "__main__":
    main()
