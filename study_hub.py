# study_hub.py - Main Study Hub Application
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import threading
import time

# Import study hub modules
from ai_teachers import MathTeacher, ScienceTeacher, HistoryTeacher, LanguageTeacher, CodingTeacher, AITeacher
from educational_games import MathGame, VocabularyGame, MemoryGame, TypingGame, QuizGame, generate_sample_quizzes
from study_tools import FlashcardDeck, NoteManager, PomodoroTimer, StudyProgress
from video_essay_generator import VideoEssayGenerator, TextToSpeechConverter

# Configure appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StudyHubApp(ctk.CTk):
    """Main Study Hub Application"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Study Hub - Complete Learning Platform")
        self.geometry("1200x800")
        
        # Initialize components
        self.current_teacher = None
        self.current_game = None
        self.note_manager = NoteManager()
        self.pomodoro = PomodoroTimer()
        self.study_progress = StudyProgress()
        self.essay_generator = VideoEssayGenerator()
        self.tts_converter = TextToSpeechConverter()
        
        # Create main layout
        self.create_layout()
        
    def create_layout(self):
        """Create the main application layout"""
        # Create sidebar for navigation
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        
        # Logo/Title
        self.logo_label = ctk.CTkLabel(self.sidebar, text="📚 Study Hub", 
                                       font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.pack(pady=20)
        
        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("🏠 Home", self.show_home),
            ("👨‍🏫 AI Teachers", self.show_ai_teachers),
            ("🎮 Games", self.show_games),
            ("📝 Notes", self.show_notes),
            ("🃏 Flashcards", self.show_flashcards),
            ("⏰ Pomodoro", self.show_pomodoro),
            ("🎥 Video Essays", self.show_video_essays),
            ("📊 Progress", self.show_progress),
        ]
        
        for text, command in nav_items:
            btn = ctk.CTkButton(self.sidebar, text=text, command=command, 
                               width=180, anchor="w")
            btn.pack(pady=5, padx=10)
            self.nav_buttons[text] = btn
        
        # Main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Show home screen by default
        self.show_home()
    
    def clear_main_frame(self):
        """Clear the main content frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        """Show home/dashboard screen"""
        self.clear_main_frame()
        
        # Welcome section
        welcome_frame = ctk.CTkFrame(self.main_frame)
        welcome_frame.pack(fill=tk.X, padx=20, pady=20)
        
        title = ctk.CTkLabel(welcome_frame, text="Welcome to Study Hub!", 
                            font=ctk.CTkFont(size=32, weight="bold"))
        title.pack(pady=10)
        
        subtitle = ctk.CTkLabel(welcome_frame, 
                               text="Your complete learning platform with AI teachers, games, and study tools",
                               font=ctk.CTkFont(size=14))
        subtitle.pack(pady=5)
        
        # Quick stats
        stats_frame = ctk.CTkFrame(self.main_frame)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        today_time = self.study_progress.get_today_study_time()
        week_time = self.study_progress.get_week_study_time()
        
        stats_label = ctk.CTkLabel(stats_frame, 
                                   text=f"📈 Today: {today_time//60} min | This Week: {week_time//60} min",
                                   font=ctk.CTkFont(size=16))
        stats_label.pack(pady=10)
        
        # Quick access features
        features_frame = ctk.CTkFrame(self.main_frame)
        features_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        features_title = ctk.CTkLabel(features_frame, text="Features", 
                                     font=ctk.CTkFont(size=20, weight="bold"))
        features_title.pack(pady=10)
        
        # Feature cards
        feature_grid = ctk.CTkFrame(features_frame)
        feature_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        features = [
            ("👨‍🏫 AI Teachers", "Get help from AI tutors in Math, Science, History, Language, and Coding"),
            ("🎮 Educational Games", "Learn through fun games: Math, Vocabulary, Memory, Typing, and Quizzes"),
            ("📝 Smart Notes", "Take and organize notes with search and categorization"),
            ("🃏 Flashcards", "Create flashcard decks for memorization and spaced repetition"),
            ("⏰ Pomodoro Timer", "Stay focused with the Pomodoro technique (25min work, 5min break)"),
            ("🎥 Video Essays", "Generate AI-powered educational video essay scripts on any topic"),
        ]
        
        row, col = 0, 0
        for title, desc in features:
            card = ctk.CTkFrame(feature_grid)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
            ctk.CTkLabel(card, text=desc, wraplength=250).pack(pady=5, padx=10)
            
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        feature_grid.grid_columnconfigure(0, weight=1)
        feature_grid.grid_columnconfigure(1, weight=1)
    
    def show_ai_teachers(self):
        """Show AI Teachers interface"""
        self.clear_main_frame()
        
        title = ctk.CTkLabel(self.main_frame, text="👨‍🏫 AI Teachers", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        # Teacher selection
        selection_frame = ctk.CTkFrame(self.main_frame)
        selection_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ctk.CTkLabel(selection_frame, text="Select a subject:", 
                    font=ctk.CTkFont(size=16)).pack(side=tk.LEFT, padx=10)
        
        subjects = ["Math", "Science", "History", "Language", "Coding", "General"]
        self.subject_var = tk.StringVar(value="Math")
        subject_menu = ctk.CTkOptionMenu(selection_frame, variable=self.subject_var, 
                                        values=subjects, command=self.change_teacher)
        subject_menu.pack(side=tk.LEFT, padx=10)
        
        # Chat area
        self.teacher_chat_display = ctk.CTkTextbox(self.main_frame, width=900, height=400)
        self.teacher_chat_display.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.teacher_chat_display.insert("1.0", "👨‍🏫 Select a subject and ask your AI teacher anything!\n\n")
        
        # Input area
        input_frame = ctk.CTkFrame(self.main_frame)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.teacher_input = ctk.CTkEntry(input_frame, placeholder_text="Ask a question...")
        self.teacher_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.teacher_input.bind("<Return>", lambda e: self.ask_teacher())
        
        send_btn = ctk.CTkButton(input_frame, text="Ask", command=self.ask_teacher)
        send_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ctk.CTkButton(input_frame, text="Clear Chat", command=self.clear_teacher_chat)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Initialize first teacher
        self.change_teacher("Math")
    
    def change_teacher(self, subject):
        """Change the current AI teacher"""
        teacher_classes = {
            "Math": MathTeacher,
            "Science": ScienceTeacher,
            "History": HistoryTeacher,
            "Language": LanguageTeacher,
            "Coding": CodingTeacher,
            "General": lambda: AITeacher("general")
        }
        
        if subject in teacher_classes:
            self.current_teacher = teacher_classes[subject]()
            self.append_to_teacher_chat(f"\n📚 Switched to {subject} Teacher\n\n")
    
    def ask_teacher(self):
        """Ask the current teacher a question"""
        question = self.teacher_input.get().strip()
        if not question or not self.current_teacher:
            return
        
        self.teacher_input.delete(0, tk.END)
        self.append_to_teacher_chat(f"You: {question}\n\n")
        
        # Get response in thread
        def get_response():
            response = self.current_teacher.ask(question)
            self.append_to_teacher_chat(f"Teacher: {response}\n\n")
        
        threading.Thread(target=get_response, daemon=True).start()
    
    def clear_teacher_chat(self):
        """Clear the teacher chat"""
        self.teacher_chat_display.delete("1.0", tk.END)
        if self.current_teacher:
            self.current_teacher.reset_conversation()
            subject = self.subject_var.get()
            self.append_to_teacher_chat(f"👨‍🏫 Chat cleared. {subject} Teacher ready!\n\n")
    
    def append_to_teacher_chat(self, text):
        """Append text to teacher chat"""
        self.teacher_chat_display.insert(tk.END, text)
        self.teacher_chat_display.see(tk.END)
    
    def show_games(self):
        """Show educational games interface"""
        self.clear_main_frame()
        
        title = ctk.CTkLabel(self.main_frame, text="🎮 Educational Games", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        # Game selection
        game_frame = ctk.CTkFrame(self.main_frame)
        game_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        games = [
            ("Math Challenge", "Practice arithmetic with timed problems", self.launch_math_game),
            ("Vocabulary Builder", "Expand your vocabulary with word definitions", self.launch_vocab_game),
            ("Type Master", "Improve typing speed and accuracy", self.launch_typing_game),
            ("Quiz Master", "Test your knowledge across subjects", self.launch_quiz_game),
        ]
        
        for i, (name, desc, command) in enumerate(games):
            card = ctk.CTkFrame(game_frame)
            card.pack(fill=tk.X, padx=10, pady=10)
            
            ctk.CTkLabel(card, text=name, font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=10, pady=5)
            ctk.CTkLabel(card, text=desc).pack(anchor="w", padx=10)
            ctk.CTkButton(card, text="Play", command=command).pack(anchor="e", padx=10, pady=5)
    
    def launch_math_game(self):
        """Launch math game"""
        self.clear_main_frame()
        
        title = ctk.CTkLabel(self.main_frame, text="🎮 Math Challenge", 
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        # Difficulty selection
        diff_frame = ctk.CTkFrame(self.main_frame)
        diff_frame.pack(pady=10)
        
        ctk.CTkLabel(diff_frame, text="Difficulty:").pack(side=tk.LEFT, padx=5)
        self.math_diff_var = tk.StringVar(value="medium")
        ctk.CTkOptionMenu(diff_frame, variable=self.math_diff_var, 
                         values=["easy", "medium", "hard"]).pack(side=tk.LEFT, padx=5)
        
        # Game area
        self.math_game_frame = ctk.CTkFrame(self.main_frame)
        self.math_game_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Problem display
        self.math_problem_label = ctk.CTkLabel(self.math_game_frame, text="", 
                                              font=ctk.CTkFont(size=32, weight="bold"))
        self.math_problem_label.pack(pady=30)
        
        # Answer input
        self.math_answer_entry = ctk.CTkEntry(self.math_game_frame, 
                                             placeholder_text="Your answer", width=200)
        self.math_answer_entry.pack(pady=10)
        self.math_answer_entry.bind("<Return>", lambda e: self.check_math_answer())
        
        # Buttons
        btn_frame = ctk.CTkFrame(self.math_game_frame)
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="Submit", command=self.check_math_answer).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="New Problem", command=self.new_math_problem).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="Back", command=self.show_games).pack(side=tk.LEFT, padx=5)
        
        # Score display
        self.math_score_label = ctk.CTkLabel(self.math_game_frame, text="Score: 0 | Accuracy: 0%")
        self.math_score_label.pack(pady=10)
        
        # Result label
        self.math_result_label = ctk.CTkLabel(self.math_game_frame, text="")
        self.math_result_label.pack(pady=10)
        
        # Initialize game
        self.current_game = MathGame(self.math_diff_var.get())
        self.new_math_problem()
    
    def new_math_problem(self):
        """Generate new math problem"""
        if not self.current_game:
            self.current_game = MathGame(self.math_diff_var.get())
        
        self.current_math_problem, self.current_math_answer = self.current_game.generate_problem()
        self.math_problem_label.configure(text=self.current_math_problem)
        self.math_answer_entry.delete(0, tk.END)
        self.math_result_label.configure(text="")
    
    def check_math_answer(self):
        """Check math answer"""
        user_answer = self.math_answer_entry.get().strip()
        if not user_answer:
            return
        
        is_correct, correct_answer = self.current_game.check_answer(
            self.current_math_problem, user_answer)
        
        if is_correct:
            self.math_result_label.configure(text="✅ Correct!", text_color="green")
        else:
            self.math_result_label.configure(
                text=f"❌ Incorrect. Answer: {correct_answer}", text_color="red")
        
        # Update score
        score = self.current_game.get_score()
        accuracy = self.current_game.get_accuracy()
        self.math_score_label.configure(text=f"Score: {score} | Accuracy: {accuracy:.1f}%")
        
        # Generate new problem after delay
        self.after(1500, self.new_math_problem)
    
    def launch_vocab_game(self):
        """Launch vocabulary game"""
        messagebox.showinfo("Vocabulary Game", "Vocabulary game coming soon!")
    
    def launch_typing_game(self):
        """Launch typing game"""
        messagebox.showinfo("Typing Game", "Typing game coming soon!")
    
    def launch_quiz_game(self):
        """Launch quiz game"""
        messagebox.showinfo("Quiz Game", "Quiz game coming soon!")
    
    def show_notes(self):
        """Show notes interface"""
        self.clear_main_frame()
        
        title = ctk.CTkLabel(self.main_frame, text="📝 Smart Notes", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        # Toolbar
        toolbar = ctk.CTkFrame(self.main_frame)
        toolbar.pack(fill=tk.X, padx=20, pady=10)
        
        ctk.CTkButton(toolbar, text="➕ New Note", command=self.create_note).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(toolbar, text="💾 Save", command=self.save_current_note).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(toolbar, text="🗑️ Delete", command=self.delete_note).pack(side=tk.LEFT, padx=5)
        
        # Content area
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Notes list (left side)
        list_frame = ctk.CTkFrame(content_frame, width=250)
        list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        ctk.CTkLabel(list_frame, text="Your Notes", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.notes_listbox = tk.Listbox(list_frame, bg="#2b2b2b", fg="white", selectmode=tk.SINGLE)
        self.notes_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.notes_listbox.bind("<<ListboxSelect>>", self.load_selected_note)
        
        # Editor (right side)
        editor_frame = ctk.CTkFrame(content_frame)
        editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.note_title_entry = ctk.CTkEntry(editor_frame, placeholder_text="Note Title")
        self.note_title_entry.pack(fill=tk.X, padx=10, pady=5)
        
        self.note_subject_entry = ctk.CTkEntry(editor_frame, placeholder_text="Subject (optional)")
        self.note_subject_entry.pack(fill=tk.X, padx=10, pady=5)
        
        self.note_editor = ctk.CTkTextbox(editor_frame)
        self.note_editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.refresh_notes_list()
    
    def create_note(self):
        """Create new note"""
        self.note_title_entry.delete(0, tk.END)
        self.note_subject_entry.delete(0, tk.END)
        self.note_editor.delete("1.0", tk.END)
        self.current_note_index = None
    
    def save_current_note(self):
        """Save current note"""
        title = self.note_title_entry.get().strip()
        subject = self.note_subject_entry.get().strip() or "general"
        content = self.note_editor.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showwarning("Warning", "Please enter a title")
            return
        
        if hasattr(self, 'current_note_index') and self.current_note_index is not None:
            self.note_manager.update_note(self.current_note_index, content)
        else:
            self.note_manager.add_note(title, content, subject)
        
        self.refresh_notes_list()
        messagebox.showinfo("Success", "Note saved!")
    
    def delete_note(self):
        """Delete selected note"""
        if hasattr(self, 'current_note_index') and self.current_note_index is not None:
            if messagebox.askyesno("Confirm", "Delete this note?"):
                self.note_manager.delete_note(self.current_note_index)
                self.create_note()
                self.refresh_notes_list()
    
    def load_selected_note(self, event):
        """Load selected note from list"""
        selection = self.notes_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index < len(self.note_manager.notes):
            note = self.note_manager.notes[index]
            self.note_title_entry.delete(0, tk.END)
            self.note_title_entry.insert(0, note.title)
            self.note_subject_entry.delete(0, tk.END)
            self.note_subject_entry.insert(0, note.subject)
            self.note_editor.delete("1.0", tk.END)
            self.note_editor.insert("1.0", note.content)
            self.current_note_index = index
    
    def refresh_notes_list(self):
        """Refresh notes list"""
        self.notes_listbox.delete(0, tk.END)
        for note in self.note_manager.notes:
            self.notes_listbox.insert(tk.END, f"{note.title} ({note.subject})")
    
    def show_flashcards(self):
        """Show flashcards interface"""
        self.clear_main_frame()
        
        title = ctk.CTkLabel(self.main_frame, text="🃏 Flashcards", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        info = ctk.CTkLabel(self.main_frame, text="Flashcard system coming soon!")
        info.pack(pady=50)
    
    def show_pomodoro(self):
        """Show Pomodoro timer interface"""
        self.clear_main_frame()
        
        title = ctk.CTkLabel(self.main_frame, text="⏰ Pomodoro Timer", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        # Timer display
        self.timer_label = ctk.CTkLabel(self.main_frame, text="25:00", 
                                       font=ctk.CTkFont(size=72, weight="bold"))
        self.timer_label.pack(pady=30)
        
        # Session type
        self.session_label = ctk.CTkLabel(self.main_frame, text="Work Session", 
                                         font=ctk.CTkFont(size=20))
        self.session_label.pack(pady=10)
        
        # Controls
        control_frame = ctk.CTkFrame(self.main_frame)
        control_frame.pack(pady=20)
        
        self.pomodoro_start_btn = ctk.CTkButton(control_frame, text="▶️ Start", 
                                               command=self.start_pomodoro)
        self.pomodoro_start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pomodoro_pause_btn = ctk.CTkButton(control_frame, text="⏸️ Pause", 
                                               command=self.pause_pomodoro, state="disabled")
        self.pomodoro_pause_btn.pack(side=tk.LEFT, padx=5)
        
        ctk.CTkButton(control_frame, text="🔄 Reset", 
                     command=self.reset_pomodoro).pack(side=tk.LEFT, padx=5)
        
        # Stats
        stats_label = ctk.CTkLabel(self.main_frame, 
                                  text=f"Sessions completed: {self.pomodoro.sessions_completed}")
        stats_label.pack(pady=10)
        
        # Start update loop
        self.update_pomodoro_display()
    
    def start_pomodoro(self):
        """Start Pomodoro timer"""
        self.pomodoro.start()
        self.pomodoro_start_btn.configure(state="disabled")
        self.pomodoro_pause_btn.configure(state="normal")
    
    def pause_pomodoro(self):
        """Pause Pomodoro timer"""
        self.pomodoro.pause()
        self.pomodoro_start_btn.configure(state="normal")
        self.pomodoro_pause_btn.configure(state="disabled")
    
    def reset_pomodoro(self):
        """Reset Pomodoro timer"""
        self.pomodoro.reset()
        self.pomodoro_start_btn.configure(state="normal")
        self.pomodoro_pause_btn.configure(state="disabled")
        self.update_pomodoro_display()
    
    def update_pomodoro_display(self):
        """Update Pomodoro display"""
        if hasattr(self, 'timer_label'):
            remaining = self.pomodoro.get_remaining_time()
            time_str = self.pomodoro.format_time(remaining)
            self.timer_label.configure(text=time_str)
            
            session_type = self.pomodoro.session_type.replace("_", " ").title()
            self.session_label.configure(text=f"{session_type} Session")
            
            if self.pomodoro.is_finished() and self.pomodoro.is_running:
                self.pomodoro.pause()
                messagebox.showinfo("Pomodoro", f"{session_type} session complete!")
                self.pomodoro.next_session()
                self.pomodoro_start_btn.configure(state="normal")
                self.pomodoro_pause_btn.configure(state="disabled")
            
            self.after(1000, self.update_pomodoro_display)
    
    def show_video_essays(self):
        """Show video essay generator interface"""
        self.clear_main_frame()
        
        title = ctk.CTkLabel(self.main_frame, text="🎥 Video Essay Generator", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        # Input section
        input_frame = ctk.CTkFrame(self.main_frame)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ctk.CTkLabel(input_frame, text="Topic:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        self.essay_topic_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter essay topic...")
        self.essay_topic_entry.pack(fill=tk.X, padx=10, pady=5)
        
        duration_frame = ctk.CTkFrame(input_frame)
        duration_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(duration_frame, text="Duration (minutes):").pack(side=tk.LEFT, padx=5)
        self.essay_duration_var = tk.StringVar(value="10")
        ctk.CTkOptionMenu(duration_frame, variable=self.essay_duration_var, 
                         values=["5", "10", "15", "20", "30", "60"]).pack(side=tk.LEFT, padx=5)
        
        ctk.CTkButton(input_frame, text="🎬 Generate Essay", 
                     command=self.generate_essay).pack(pady=10)
        
        # Output area
        self.essay_output = ctk.CTkTextbox(self.main_frame)
        self.essay_output.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.essay_output.insert("1.0", "Enter a topic and click 'Generate Essay' to create an AI-powered educational video essay script.\n\nYou can generate essays from 5 to 60+ minutes in length!")
    
    def generate_essay(self):
        """Generate video essay"""
        topic = self.essay_topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Warning", "Please enter a topic")
            return
        
        duration = int(self.essay_duration_var.get())
        
        self.essay_output.delete("1.0", tk.END)
        self.essay_output.insert("1.0", f"Generating {duration}-minute essay on '{topic}'...\n\nThis may take a moment...\n\n")
        
        def generate():
            essay = self.essay_generator.generate_full_script(topic, duration)
            if isinstance(essay, dict) and "script" in essay:
                script = essay["script"]
                word_count = essay["word_count"]
                self.essay_output.delete("1.0", tk.END)
                self.essay_output.insert("1.0", f"📝 Essay Topic: {topic}\n")
                self.essay_output.insert(tk.END, f"⏱️ Target Duration: {duration} minutes\n")
                self.essay_output.insert(tk.END, f"📊 Word Count: {word_count}\n")
                self.essay_output.insert(tk.END, f"\n{'='*60}\n\n")
                self.essay_output.insert(tk.END, script)
            else:
                self.essay_output.delete("1.0", tk.END)
                self.essay_output.insert("1.0", f"Error: {essay.get('error', 'Unknown error')}")
        
        threading.Thread(target=generate, daemon=True).start()
    
    def show_progress(self):
        """Show progress and statistics"""
        self.clear_main_frame()
        
        title = ctk.CTkLabel(self.main_frame, text="📊 Your Progress", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)
        
        # Stats cards
        stats_frame = ctk.CTkFrame(self.main_frame)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        today_time = self.study_progress.get_today_study_time()
        week_time = self.study_progress.get_week_study_time()
        total_time = self.study_progress.total_study_time
        
        # Time stats
        time_card = ctk.CTkFrame(stats_frame)
        time_card.pack(fill=tk.X, padx=10, pady=10)
        
        ctk.CTkLabel(time_card, text="⏱️ Study Time", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        ctk.CTkLabel(time_card, text=f"Today: {today_time//60} minutes").pack(pady=5)
        ctk.CTkLabel(time_card, text=f"This Week: {week_time//60} minutes").pack(pady=5)
        ctk.CTkLabel(time_card, text=f"Total: {total_time//3600} hours").pack(pady=5)
        
        # Subject breakdown
        subject_card = ctk.CTkFrame(stats_frame)
        subject_card.pack(fill=tk.X, padx=10, pady=10)
        
        ctk.CTkLabel(subject_card, text="📚 Study by Subject", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        subjects = self.study_progress.get_subject_stats()
        if subjects:
            for subject, time_seconds in subjects.items():
                ctk.CTkLabel(subject_card, 
                           text=f"{subject}: {time_seconds//60} minutes").pack(pady=2)
        else:
            ctk.CTkLabel(subject_card, text="No study data yet").pack(pady=5)


if __name__ == "__main__":
    app = StudyHubApp()
    app.mainloop()
