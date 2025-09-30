#!/usr/bin/env python3
# study_hub_cli.py - Command-line version of Study Hub
import sys
import os

# Import study hub modules
from ai_teachers import MathTeacher, ScienceTeacher, HistoryTeacher, LanguageTeacher, CodingTeacher, AITeacher
from educational_games import MathGame, VocabularyGame, QuizGame, generate_sample_quizzes
from study_tools import NoteManager, PomodoroTimer, StudyProgress
from video_essay_generator import VideoEssayGenerator

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def main_menu():
    """Display main menu"""
    clear_screen()
    print_header("📚 STUDY HUB - Complete Learning Platform")
    print("1. 👨‍🏫 AI Teachers")
    print("2. 🎮 Educational Games")
    print("3. 📝 Notes Manager")
    print("4. ⏰ Pomodoro Timer")
    print("5. 🎥 Video Essay Generator")
    print("6. 📊 Progress Tracker")
    print("0. Exit")
    print()
    
    choice = input("Select an option (0-6): ").strip()
    return choice

def ai_teachers_menu():
    """AI Teachers interface"""
    clear_screen()
    print_header("👨‍🏫 AI Teachers")
    print("1. Math Teacher")
    print("2. Science Teacher")
    print("3. History Teacher")
    print("4. Language Teacher")
    print("5. Coding Teacher")
    print("6. General Tutor")
    print("0. Back to Main Menu")
    print()
    
    choice = input("Select a teacher (0-6): ").strip()
    
    if choice == "0":
        return
    
    teachers = {
        "1": ("Math", MathTeacher()),
        "2": ("Science", ScienceTeacher()),
        "3": ("History", HistoryTeacher()),
        "4": ("Language", LanguageTeacher()),
        "5": ("Coding", CodingTeacher()),
        "6": ("General", AITeacher("general"))
    }
    
    if choice not in teachers:
        print("Invalid choice!")
        input("Press Enter to continue...")
        return
    
    subject, teacher = teachers[choice]
    
    clear_screen()
    print_header(f"{subject} Teacher")
    print("Type 'back' to return to teacher menu")
    print("Type 'clear' to clear conversation history")
    print()
    
    while True:
        question = input(f"\n{subject} Question: ").strip()
        
        if question.lower() == 'back':
            break
        elif question.lower() == 'clear':
            teacher.reset_conversation()
            print("✓ Conversation cleared!")
            continue
        elif not question:
            continue
        
        print(f"\n{subject} Teacher: ", end="", flush=True)
        response = teacher.ask(question)
        print(response)

def games_menu():
    """Educational Games interface"""
    while True:
        clear_screen()
        print_header("🎮 Educational Games")
        print("1. Math Challenge")
        print("2. Vocabulary Builder")
        print("3. Quiz Master")
        print("0. Back to Main Menu")
        print()
        
        choice = input("Select a game (0-3): ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            play_math_game()
        elif choice == "2":
            play_vocab_game()
        elif choice == "3":
            play_quiz_game()
        else:
            print("Invalid choice!")
            input("Press Enter to continue...")

def play_math_game():
    """Play math challenge game"""
    clear_screen()
    print_header("🎮 Math Challenge")
    
    print("Select difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    
    diff_choice = input("\nDifficulty (1-3): ").strip()
    difficulties = {"1": "easy", "2": "medium", "3": "hard"}
    difficulty = difficulties.get(diff_choice, "medium")
    
    game = MathGame(difficulty)
    print(f"\nStarting {difficulty} Math Challenge!")
    print("Type 'quit' to stop playing\n")
    
    while True:
        problem, answer = game.generate_problem()
        user_answer = input(f"\n{problem} = ").strip()
        
        if user_answer.lower() == 'quit':
            break
        
        is_correct, correct_answer = game.check_answer(problem, user_answer)
        
        if is_correct:
            print("✅ Correct!")
        else:
            print(f"❌ Incorrect. Answer: {correct_answer}")
        
        print(f"Score: {game.get_score()} | Accuracy: {game.get_accuracy():.1f}%")
    
    print(f"\nFinal Score: {game.get_score()}")
    print(f"Final Accuracy: {game.get_accuracy():.1f}%")
    print(f"Questions Answered: {game.questions_answered}")
    input("\nPress Enter to continue...")

def play_vocab_game():
    """Play vocabulary game"""
    clear_screen()
    print_header("🎮 Vocabulary Builder")
    
    print("Select difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    
    diff_choice = input("\nDifficulty (1-3): ").strip()
    difficulties = {"1": "easy", "2": "medium", "3": "hard"}
    difficulty = difficulties.get(diff_choice, "medium")
    
    game = VocabularyGame(difficulty)
    print(f"\nStarting {difficulty} Vocabulary Builder!")
    print("Type 'quit' to stop playing\n")
    
    while True:
        word_data = game.get_random_word()
        print(f"\nWord: {word_data['word']}")
        user_def = input("Definition: ").strip()
        
        if user_def.lower() == 'quit':
            break
        
        is_correct, correct_def = game.check_definition(word_data, user_def)
        
        if is_correct:
            print("✅ Good answer!")
        else:
            print(f"❌ Not quite. Correct definition: {correct_def}")
        print(f"Synonym: {word_data['synonym']}")
        
        print(f"\nScore: {game.get_score()} | Accuracy: {game.get_accuracy():.1f}%")
    
    print(f"\nFinal Score: {game.get_score()}")
    input("\nPress Enter to continue...")

def play_quiz_game():
    """Play quiz game"""
    clear_screen()
    print_header("🎮 Quiz Master")
    
    print("Select subject:")
    print("1. Science")
    print("2. History")
    print("3. Math")
    
    subj_choice = input("\nSubject (1-3): ").strip()
    subjects = {"1": "science", "2": "history", "3": "math"}
    subject = subjects.get(subj_choice, "science")
    
    quizzes = generate_sample_quizzes()
    questions = quizzes.get(subject, [])
    
    if not questions:
        print("No quiz available for this subject!")
        input("Press Enter to continue...")
        return
    
    game = QuizGame(subject)
    game.create_quiz(questions)
    
    print(f"\n{subject.title()} Quiz - {len(questions)} questions")
    print("="*60)
    
    for i, q in enumerate(questions):
        print(f"\nQuestion {i+1}: {q['question']}")
        for j, option in enumerate(q['options']):
            print(f"  {chr(65+j)}) {option}")
        
        user_answer = input("\nYour answer (A-D): ").strip().upper()
        
        # Convert letter to full answer
        if user_answer in ['A', 'B', 'C', 'D']:
            idx = ord(user_answer) - 65
            if 0 <= idx < len(q['options']):
                user_answer = q['options'][idx]
        
        is_correct, correct = game.check_answer(i, user_answer)
        
        if is_correct:
            print("✅ Correct!")
        else:
            print(f"❌ Incorrect. Answer: {correct}")
    
    print(f"\n{'='*60}")
    print(f"Quiz Complete!")
    print(f"Score: {game.get_score()}")
    print(f"Accuracy: {game.get_accuracy():.1f}%")
    input("\nPress Enter to continue...")

def notes_menu():
    """Notes manager interface"""
    note_manager = NoteManager()
    
    while True:
        clear_screen()
        print_header("📝 Notes Manager")
        print("1. Create New Note")
        print("2. View All Notes")
        print("3. Search Notes")
        print("4. Delete Note")
        print("0. Back to Main Menu")
        print()
        
        choice = input("Select an option (0-4): ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            create_note(note_manager)
        elif choice == "2":
            view_notes(note_manager)
        elif choice == "3":
            search_notes(note_manager)
        elif choice == "4":
            delete_note(note_manager)
        else:
            print("Invalid choice!")
            input("Press Enter to continue...")

def create_note(note_manager):
    """Create a new note"""
    clear_screen()
    print_header("📝 Create New Note")
    
    title = input("Note Title: ").strip()
    if not title:
        print("Title cannot be empty!")
        input("Press Enter to continue...")
        return
    
    subject = input("Subject (optional): ").strip() or "general"
    print("\nEnter note content (type 'END' on a new line to finish):")
    
    lines = []
    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)
    
    content = "\n".join(lines)
    note_manager.add_note(title, content, subject)
    
    print("\n✓ Note saved successfully!")
    input("Press Enter to continue...")

def view_notes(note_manager):
    """View all notes"""
    clear_screen()
    print_header("📝 All Notes")
    
    if not note_manager.notes:
        print("No notes found.")
        input("\nPress Enter to continue...")
        return
    
    for i, note in enumerate(note_manager.notes):
        print(f"\n{i+1}. {note.title} ({note.subject})")
        print(f"   Created: {note.created_at[:10]}")
        print(f"   {note.content[:100]}..." if len(note.content) > 100 else f"   {note.content}")
    
    note_num = input("\nEnter note number to view full content (or press Enter to go back): ").strip()
    
    if note_num.isdigit():
        idx = int(note_num) - 1
        if 0 <= idx < len(note_manager.notes):
            note = note_manager.notes[idx]
            clear_screen()
            print_header(note.title)
            print(f"Subject: {note.subject}")
            print(f"Created: {note.created_at}")
            print(f"Updated: {note.updated_at}")
            print("\n" + "="*60 + "\n")
            print(note.content)
            input("\n\nPress Enter to continue...")

def search_notes(note_manager):
    """Search notes"""
    clear_screen()
    print_header("🔍 Search Notes")
    
    query = input("Enter search query: ").strip()
    if not query:
        return
    
    results = note_manager.search_notes(query)
    
    if not results:
        print(f"\nNo notes found matching '{query}'")
    else:
        print(f"\nFound {len(results)} note(s):")
        for idx, note in results:
            print(f"\n{idx+1}. {note.title} ({note.subject})")
            print(f"   {note.content[:100]}..." if len(note.content) > 100 else f"   {note.content}")
    
    input("\nPress Enter to continue...")

def delete_note(note_manager):
    """Delete a note"""
    clear_screen()
    print_header("🗑️ Delete Note")
    
    if not note_manager.notes:
        print("No notes to delete.")
        input("\nPress Enter to continue...")
        return
    
    for i, note in enumerate(note_manager.notes):
        print(f"{i+1}. {note.title} ({note.subject})")
    
    note_num = input("\nEnter note number to delete (or press Enter to cancel): ").strip()
    
    if note_num.isdigit():
        idx = int(note_num) - 1
        if 0 <= idx < len(note_manager.notes):
            confirm = input(f"Delete '{note_manager.notes[idx].title}'? (yes/no): ").strip().lower()
            if confirm == 'yes':
                note_manager.delete_note(idx)
                print("✓ Note deleted!")
            else:
                print("Cancelled.")
        else:
            print("Invalid note number!")
    
    input("\nPress Enter to continue...")

def pomodoro_menu():
    """Pomodoro timer interface"""
    clear_screen()
    print_header("⏰ Pomodoro Timer")
    print("Pomodoro timer feature available in GUI version.")
    print("\nThe Pomodoro technique: 25min work + 5min break")
    print("After 4 sessions, take a 15min break")
    input("\nPress Enter to continue...")

def video_essay_menu():
    """Video essay generator interface"""
    clear_screen()
    print_header("🎥 Video Essay Generator")
    
    topic = input("Enter essay topic: ").strip()
    if not topic:
        return
    
    print("\nSelect duration:")
    print("1. 5 minutes")
    print("2. 10 minutes")
    print("3. 15 minutes")
    print("4. 30 minutes")
    
    dur_choice = input("\nDuration (1-4): ").strip()
    durations = {"1": 5, "2": 10, "3": 15, "4": 30}
    duration = durations.get(dur_choice, 10)
    
    print(f"\n🎬 Generating {duration}-minute essay on '{topic}'...")
    print("This may take a moment...\n")
    
    generator = VideoEssayGenerator()
    essay = generator.generate_full_script(topic, duration)
    
    if isinstance(essay, dict) and "script" in essay:
        clear_screen()
        print_header(f"Video Essay: {topic}")
        print(f"Duration: {duration} minutes")
        print(f"Word Count: {essay['word_count']}")
        print("\n" + "="*60 + "\n")
        print(essay['script'])
        
        save = input("\n\nSave essay to file? (yes/no): ").strip().lower()
        if save == 'yes':
            filename = input("Filename (without extension): ").strip()
            if filename:
                import json
                with open(f"{filename}.json", "w") as f:
                    json.dump(essay, f, indent=2)
                print(f"✓ Saved to {filename}.json")
    else:
        print(f"\nError: {essay.get('error', 'Unknown error')}")
    
    input("\n\nPress Enter to continue...")

def progress_menu():
    """Progress tracker interface"""
    progress = StudyProgress()
    
    clear_screen()
    print_header("📊 Your Progress")
    
    today_time = progress.get_today_study_time()
    week_time = progress.get_week_study_time()
    total_time = progress.total_study_time
    
    print(f"Today: {today_time//60} minutes")
    print(f"This Week: {week_time//60} minutes")
    print(f"Total: {total_time//3600} hours {(total_time%3600)//60} minutes")
    
    print("\n" + "="*60)
    print("\nStudy Time by Subject:")
    
    subjects = progress.get_subject_stats()
    if subjects:
        for subject, time_seconds in subjects.items():
            hours = time_seconds // 3600
            minutes = (time_seconds % 3600) // 60
            print(f"  {subject}: {hours}h {minutes}m")
    else:
        print("  No study data yet")
    
    input("\n\nPress Enter to continue...")

def main():
    """Main program loop"""
    while True:
        choice = main_menu()
        
        if choice == "0":
            clear_screen()
            print("\n📚 Thank you for using Study Hub! Happy learning! 🎓\n")
            break
        elif choice == "1":
            ai_teachers_menu()
        elif choice == "2":
            games_menu()
        elif choice == "3":
            notes_menu()
        elif choice == "4":
            pomodoro_menu()
        elif choice == "5":
            video_essay_menu()
        elif choice == "6":
            progress_menu()
        else:
            print("Invalid choice!")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n📚 Study Hub terminated. Goodbye! 🎓\n")
        sys.exit(0)
