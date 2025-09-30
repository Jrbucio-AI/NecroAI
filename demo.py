#!/usr/bin/env python3
# demo.py - Demonstration of Study Hub features
"""
This script demonstrates the key features of the Study Hub application.
Run this to see the capabilities without needing the GUI or interactive CLI.
"""

from ai_teachers import MathTeacher, ScienceTeacher, HistoryTeacher
from educational_games import MathGame, VocabularyGame, generate_sample_quizzes
from study_tools import NoteManager, PomodoroTimer, StudyProgress
from video_essay_generator import VideoEssayGenerator

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def demo_ai_teachers():
    """Demonstrate AI Teachers"""
    print_section("🎓 AI TEACHERS DEMO")
    
    print("Study Hub includes specialized AI teachers for different subjects:")
    print("- Math Teacher (step-by-step problem solving)")
    print("- Science Teacher (experiments and concepts)")
    print("- History Teacher (timelines and context)")
    print("- Language Teacher (grammar and writing)")
    print("- Coding Teacher (debugging and explanations)")
    print()
    
    print("Note: AI teachers require Ollama with llama3 model running.")
    print("Example question: 'Explain the Pythagorean theorem step by step'")
    print()

def demo_educational_games():
    """Demonstrate Educational Games"""
    print_section("🎮 EDUCATIONAL GAMES DEMO")
    
    print("1. MATH CHALLENGE")
    print("-" * 70)
    game = MathGame("medium")
    for i in range(3):
        problem, answer = game.generate_problem()
        print(f"Problem {i+1}: {problem} = {answer}")
    print(f"Game features: Multiple difficulties, score tracking, accuracy stats")
    print()
    
    print("2. VOCABULARY BUILDER")
    print("-" * 70)
    vocab_game = VocabularyGame("medium")
    word = vocab_game.get_random_word()
    print(f"Word: {word['word']}")
    print(f"Definition: {word['definition']}")
    print(f"Synonym: {word['synonym']}")
    print(f"Game features: Word definitions, synonyms, difficulty levels")
    print()
    
    print("3. QUIZ MASTER")
    print("-" * 70)
    quizzes = generate_sample_quizzes()
    print(f"Available subjects: {', '.join(quizzes.keys())}")
    quiz = quizzes['science'][0]
    print(f"\nSample question: {quiz['question']}")
    for i, option in enumerate(quiz['options']):
        print(f"  {chr(65+i)}) {option}")
    print(f"Answer: {quiz['answer']}")
    print()

def demo_study_tools():
    """Demonstrate Study Tools"""
    print_section("📚 STUDY TOOLS DEMO")
    
    print("1. NOTES MANAGER")
    print("-" * 70)
    note_manager = NoteManager()
    note_manager.add_note(
        "Physics - Newton's Laws",
        "1. Law of Inertia\n2. F = ma\n3. Action-Reaction",
        "Physics"
    )
    note_manager.add_note(
        "Math - Quadratic Formula",
        "x = (-b ± √(b²-4ac)) / 2a",
        "Math"
    )
    print(f"✓ Created {len(note_manager.notes)} sample notes")
    for note in note_manager.notes:
        print(f"  - {note.title} ({note.subject})")
    print(f"Features: Search, categorize, tag, edit, organize by subject")
    print()
    
    print("2. POMODORO TIMER")
    print("-" * 70)
    pomodoro = PomodoroTimer(work_minutes=25, break_minutes=5, long_break_minutes=15)
    print(f"Work session: {pomodoro.work_duration // 60} minutes")
    print(f"Short break: {pomodoro.break_duration // 60} minutes")
    print(f"Long break (every 4 sessions): {pomodoro.long_break_duration // 60} minutes")
    print(f"Features: Start/pause/reset, session tracking, break reminders")
    print()
    
    print("3. PROGRESS TRACKER")
    print("-" * 70)
    progress = StudyProgress()
    progress.log_session("Math", 1500, "practice")  # 25 minutes
    progress.log_session("Science", 900, "reading")  # 15 minutes
    progress.log_session("Math", 600, "homework")    # 10 minutes
    
    print(f"Total study time: {progress.total_study_time // 60} minutes")
    print(f"Today's study time: {progress.get_today_study_time() // 60} minutes")
    print("\nStudy time by subject:")
    for subject, time_sec in progress.get_subject_stats().items():
        print(f"  {subject}: {time_sec // 60} minutes")
    print(f"Features: Daily/weekly stats, subject breakdown, session history")
    print()

def demo_video_essays():
    """Demonstrate Video Essay Generator"""
    print_section("🎬 VIDEO ESSAY GENERATOR DEMO")
    
    print("The Video Essay Generator creates AI-powered educational content.")
    print()
    print("Features:")
    print("- Generate essays from 5 to 60+ minutes in length")
    print("- Comprehensive outlines and scripts")
    print("- Visual suggestions for video production")
    print("- Study guides and quizzes from essays")
    print("- Text-to-speech conversion support")
    print()
    
    generator = VideoEssayGenerator()
    print("Example topics you can generate:")
    topics = [
        "The History of Artificial Intelligence",
        "Understanding Quantum Mechanics",
        "The Renaissance: Art and Science",
        "Climate Change: Causes and Solutions",
        "Introduction to Machine Learning",
    ]
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    print()
    print("Note: Essay generation requires Ollama with llama3 model running.")
    print("Generated essays include narration text, visual cues, and educational content.")
    print()

def demo_flashcards():
    """Demonstrate Flashcards"""
    print_section("🃏 FLASHCARDS DEMO")
    
    from study_tools import FlashcardDeck
    
    # Create a sample deck
    deck = FlashcardDeck("Spanish Vocabulary", "Language")
    deck.add_card("Hola", "Hello")
    deck.add_card("Gracias", "Thank you")
    deck.add_card("Por favor", "Please")
    deck.add_card("Adiós", "Goodbye")
    
    print(f"Created deck: {deck.name} ({deck.category})")
    print(f"Cards in deck: {len(deck.cards)}")
    print()
    print("Sample flashcards:")
    for i, card in enumerate(deck.cards[:3], 1):
        print(f"  {i}. Front: {card.front}")
        print(f"     Back: {card.back}")
        print()
    
    print("Features:")
    print("- Create multiple decks by category")
    print("- Track review progress")
    print("- Spaced repetition support")
    print("- Save/load decks")
    print("- Shuffle for practice")
    print()

def main():
    """Run all demonstrations"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  📚 STUDY HUB - COMPLETE LEARNING PLATFORM DEMO".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    print("\nWelcome to Study Hub! This demo showcases all the features.")
    print("Study Hub transforms learning with AI teachers, games, and tools.")
    
    demo_ai_teachers()
    demo_educational_games()
    demo_study_tools()
    demo_flashcards()
    demo_video_essays()
    
    print_section("🚀 GETTING STARTED")
    print("To use Study Hub:")
    print()
    print("1. INSTALL DEPENDENCIES:")
    print("   pip install -r requirements.txt")
    print()
    print("2. SETUP OLLAMA (for AI features):")
    print("   - Download from https://ollama.ai")
    print("   - Run: ollama pull llama3")
    print("   - Start: ollama serve")
    print()
    print("3. RUN THE APPLICATION:")
    print("   - GUI version: python study_hub.py")
    print("   - CLI version: python study_hub_cli.py")
    print()
    print("📖 For full documentation, see README.md")
    print()
    print("="*70)
    print("Happy Learning! 🎓✨")
    print("="*70)
    print()

if __name__ == "__main__":
    main()
