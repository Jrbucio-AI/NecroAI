# study_tools.py - Study Tools Module for Study Hub
import json
import os
import time
from datetime import datetime, timedelta

class Flashcard:
    """Flashcard for memorization"""
    
    def __init__(self, front, back, category="general"):
        self.front = front
        self.back = back
        self.category = category
        self.times_reviewed = 0
        self.times_correct = 0
        self.last_reviewed = None
        self.created_at = datetime.now().isoformat()
        
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "front": self.front,
            "back": self.back,
            "category": self.category,
            "times_reviewed": self.times_reviewed,
            "times_correct": self.times_correct,
            "last_reviewed": self.last_reviewed,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        card = cls(data["front"], data["back"], data.get("category", "general"))
        card.times_reviewed = data.get("times_reviewed", 0)
        card.times_correct = data.get("times_correct", 0)
        card.last_reviewed = data.get("last_reviewed")
        card.created_at = data.get("created_at", datetime.now().isoformat())
        return card


class FlashcardDeck:
    """Manage a deck of flashcards"""
    
    def __init__(self, name, category="general"):
        self.name = name
        self.category = category
        self.cards = []
        
    def add_card(self, front, back):
        """Add a flashcard to the deck"""
        card = Flashcard(front, back, self.category)
        self.cards.append(card)
        
    def remove_card(self, index):
        """Remove a card from the deck"""
        if 0 <= index < len(self.cards):
            self.cards.pop(index)
            
    def get_card(self, index):
        """Get a specific card"""
        if 0 <= index < len(self.cards):
            return self.cards[index]
        return None
    
    def shuffle(self):
        """Shuffle the deck"""
        import random
        random.shuffle(self.cards)
        
    def save(self, filename):
        """Save deck to file"""
        data = {
            "name": self.name,
            "category": self.category,
            "cards": [card.to_dict() for card in self.cards]
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
            
    @classmethod
    def load(cls, filename):
        """Load deck from file"""
        with open(filename, "r") as f:
            data = json.load(f)
        deck = cls(data["name"], data.get("category", "general"))
        deck.cards = [Flashcard.from_dict(card_data) for card_data in data["cards"]]
        return deck


class Note:
    """Note-taking system"""
    
    def __init__(self, title, content, subject="general"):
        self.title = title
        self.content = content
        self.subject = subject
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.tags = []
        
    def update(self, content):
        """Update note content"""
        self.content = content
        self.updated_at = datetime.now().isoformat()
        
    def add_tag(self, tag):
        """Add a tag to the note"""
        if tag not in self.tags:
            self.tags.append(tag)
            
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "title": self.title,
            "content": self.content,
            "subject": self.subject,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        note = cls(data["title"], data["content"], data.get("subject", "general"))
        note.created_at = data.get("created_at", note.created_at)
        note.updated_at = data.get("updated_at", note.updated_at)
        note.tags = data.get("tags", [])
        return note


class NoteManager:
    """Manage notes"""
    
    def __init__(self, storage_file="notes.json"):
        self.storage_file = storage_file
        self.notes = []
        self.load_notes()
        
    def add_note(self, title, content, subject="general"):
        """Add a new note"""
        note = Note(title, content, subject)
        self.notes.append(note)
        self.save_notes()
        return note
        
    def update_note(self, index, content):
        """Update an existing note"""
        if 0 <= index < len(self.notes):
            self.notes[index].update(content)
            self.save_notes()
            return True
        return False
        
    def delete_note(self, index):
        """Delete a note"""
        if 0 <= index < len(self.notes):
            self.notes.pop(index)
            self.save_notes()
            return True
        return False
        
    def search_notes(self, query):
        """Search notes by title, content, or tags"""
        query_lower = query.lower()
        results = []
        for i, note in enumerate(self.notes):
            if (query_lower in note.title.lower() or 
                query_lower in note.content.lower() or 
                any(query_lower in tag.lower() for tag in note.tags)):
                results.append((i, note))
        return results
        
    def get_notes_by_subject(self, subject):
        """Get all notes for a specific subject"""
        return [(i, note) for i, note in enumerate(self.notes) if note.subject == subject]
        
    def save_notes(self):
        """Save notes to file"""
        data = [note.to_dict() for note in self.notes]
        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=2)
            
    def load_notes(self):
        """Load notes from file"""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                data = json.load(f)
            self.notes = [Note.from_dict(note_data) for note_data in data]


class PomodoroTimer:
    """Pomodoro technique timer for studying"""
    
    def __init__(self, work_minutes=25, break_minutes=5, long_break_minutes=15):
        self.work_duration = work_minutes * 60
        self.break_duration = break_minutes * 60
        self.long_break_duration = long_break_minutes * 60
        self.sessions_completed = 0
        self.is_running = False
        self.start_time = None
        self.remaining_time = self.work_duration
        self.session_type = "work"  # "work", "break", or "long_break"
        
    def start(self):
        """Start the timer"""
        self.is_running = True
        self.start_time = time.time()
        
    def pause(self):
        """Pause the timer"""
        if self.is_running:
            elapsed = time.time() - self.start_time
            self.remaining_time -= elapsed
            self.is_running = False
            
    def reset(self):
        """Reset the timer"""
        self.is_running = False
        self.start_time = None
        if self.session_type == "work":
            self.remaining_time = self.work_duration
        elif self.session_type == "break":
            self.remaining_time = self.break_duration
        else:
            self.remaining_time = self.long_break_duration
            
    def get_remaining_time(self):
        """Get remaining time in seconds"""
        if self.is_running:
            elapsed = time.time() - self.start_time
            return max(0, self.remaining_time - elapsed)
        return self.remaining_time
        
    def is_finished(self):
        """Check if timer is finished"""
        return self.get_remaining_time() <= 0
        
    def next_session(self):
        """Move to next session"""
        if self.session_type == "work":
            self.sessions_completed += 1
            if self.sessions_completed % 4 == 0:
                self.session_type = "long_break"
                self.remaining_time = self.long_break_duration
            else:
                self.session_type = "break"
                self.remaining_time = self.break_duration
        else:
            self.session_type = "work"
            self.remaining_time = self.work_duration
        self.is_running = False
        self.start_time = None
        
    def format_time(self, seconds):
        """Format seconds as MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"


class StudyProgress:
    """Track study progress and statistics"""
    
    def __init__(self, storage_file="study_progress.json"):
        self.storage_file = storage_file
        self.sessions = []
        self.total_study_time = 0  # in seconds
        self.subjects_studied = {}
        self.load_progress()
        
    def log_session(self, subject, duration_seconds, activity="study"):
        """Log a study session"""
        session = {
            "subject": subject,
            "duration": duration_seconds,
            "activity": activity,
            "timestamp": datetime.now().isoformat()
        }
        self.sessions.append(session)
        self.total_study_time += duration_seconds
        
        if subject not in self.subjects_studied:
            self.subjects_studied[subject] = 0
        self.subjects_studied[subject] += duration_seconds
        
        self.save_progress()
        
    def get_today_study_time(self):
        """Get total study time for today"""
        today = datetime.now().date()
        total = 0
        for session in self.sessions:
            session_date = datetime.fromisoformat(session["timestamp"]).date()
            if session_date == today:
                total += session["duration"]
        return total
        
    def get_week_study_time(self):
        """Get total study time for this week"""
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        total = 0
        for session in self.sessions:
            session_date = datetime.fromisoformat(session["timestamp"]).date()
            if session_date >= week_start:
                total += session["duration"]
        return total
        
    def get_subject_stats(self):
        """Get study time by subject"""
        return self.subjects_studied.copy()
        
    def save_progress(self):
        """Save progress to file"""
        data = {
            "sessions": self.sessions,
            "total_study_time": self.total_study_time,
            "subjects_studied": self.subjects_studied
        }
        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=2)
            
    def load_progress(self):
        """Load progress from file"""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                data = json.load(f)
            self.sessions = data.get("sessions", [])
            self.total_study_time = data.get("total_study_time", 0)
            self.subjects_studied = data.get("subjects_studied", {})
