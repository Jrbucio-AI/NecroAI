# Study Hub - Complete Learning Platform

Welcome to **Study Hub**, a comprehensive educational platform powered by AI! This application transforms learning into an engaging, interactive experience with AI teachers, educational games, study tools, and AI-generated video essay scripts.

## 🌟 Features

### 👨‍🏫 AI Teachers
Get personalized help from AI tutors specializing in:
- **Math** - Step-by-step problem solving and concept explanations
- **Science** - Scientific concepts, experiments, and real-world applications
- **History** - Historical timelines, context, and analysis
- **Language** - Grammar, vocabulary, writing assistance
- **Coding** - Programming concepts, debugging, and code explanations
- **General** - Any other subject or topic

Each AI teacher adapts to your learning style and provides detailed, understandable explanations.

### 🎮 Educational Games
Learn through fun and interactive games:
- **Math Challenge** - Practice arithmetic with timed problems (easy/medium/hard)
- **Vocabulary Builder** - Expand your vocabulary with definitions and synonyms
- **Memory Match** - Match pairs to reinforce learning concepts
- **Type Master** - Improve typing speed and accuracy
- **Quiz Master** - Test knowledge across different subjects

### 📝 Study Tools
Essential tools for effective studying:
- **Smart Notes** - Create, organize, and search notes by subject
- **Flashcards** - Build flashcard decks for memorization and spaced repetition
- **Pomodoro Timer** - Stay focused with 25-minute work sessions and 5-minute breaks
- **Progress Tracking** - Monitor your study time and progress across subjects

### 🎥 Video Essay Generator
Generate AI-powered educational video essays:
- Create essay scripts from 5 minutes to 60+ minutes
- Comprehensive outlines and detailed content
- Suitable for any educational topic
- Includes suggestions for visuals and graphics
- Generate study guides and quizzes from essays

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Ollama with llama3 model (or compatible AI model)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Jrbucio-AI/NecroAI.git
cd NecroAI
```

2. **Install dependencies**
```bash
pip install customtkinter requests pyttsx3 pyaudio vosk
```

3. **Install and start Ollama**
- Download Ollama from https://ollama.ai
- Install the llama3 model:
```bash
ollama pull llama3
```
- Start Ollama (it runs on http://localhost:11434 by default)

4. **Run Study Hub**
```bash
python study_hub.py
```

## 📚 Usage Guide

### Using AI Teachers
1. Click "👨‍🏫 AI Teachers" in the sidebar
2. Select a subject from the dropdown menu
3. Type your question in the input field
4. Press Enter or click "Ask" to get a response
5. Continue the conversation to dive deeper into topics

### Playing Educational Games
1. Click "🎮 Games" in the sidebar
2. Select a game from the list
3. Choose your difficulty level
4. Follow the game instructions
5. Track your score and accuracy

### Taking Notes
1. Click "📝 Notes" in the sidebar
2. Click "➕ New Note" to create a note
3. Enter a title and subject
4. Write your note content
5. Click "💾 Save" to save your note
6. Click on saved notes in the list to view/edit them

### Using Pomodoro Timer
1. Click "⏰ Pomodoro" in the sidebar
2. Click "▶️ Start" to begin a 25-minute work session
3. Focus on your studies during the work session
4. Take a 5-minute break when the timer completes
5. After 4 sessions, take a longer 15-minute break

### Generating Video Essays
1. Click "🎥 Video Essays" in the sidebar
2. Enter your essay topic
3. Select desired duration (5-60+ minutes)
4. Click "🎬 Generate Essay"
5. Wait for AI to generate the complete script
6. Use the script for learning or content creation

### Tracking Progress
1. Click "📊 Progress" in the sidebar
2. View your study time statistics
3. See breakdown by subject
4. Monitor your daily and weekly progress

## 🎯 Tips for Effective Use

### Studying Tips
- Use the Pomodoro timer to maintain focus and avoid burnout
- Take notes during AI teacher sessions for better retention
- Review your notes regularly and update them with new information
- Practice with educational games to reinforce concepts
- Track your progress to stay motivated

### AI Teacher Tips
- Ask specific questions for better answers
- Request step-by-step explanations for complex topics
- Ask for examples to understand concepts better
- Don't hesitate to ask follow-up questions
- Use different teachers for different subjects

### Video Essay Tips
- Start with shorter essays (10-15 minutes) for focused topics
- Generate longer essays (30-60 minutes) for comprehensive overviews
- Use generated scripts as study guides
- Break down long essays into manageable sections
- Create quizzes based on essay content to test understanding

## 🔧 Configuration

### Changing AI Model
Edit the `MODEL_NAME` variable in the respective files:
- `ai_teachers.py` - Line with model initialization
- `video_essay_generator.py` - Line with model initialization

Example:
```python
MODEL_NAME = "llama3"  # or "mistral", "codellama", etc.
```

### Customizing Pomodoro Times
Edit the timer initialization in `study_tools.py`:
```python
PomodoroTimer(work_minutes=25, break_minutes=5, long_break_minutes=15)
```

### Adjusting Game Difficulty
Modify difficulty ranges in `educational_games.py` for each game class.

## 📁 Project Structure

```
NecroAI/
├── study_hub.py              # Main application with GUI
├── ai_teachers.py            # AI teacher module
├── educational_games.py      # Educational games module
├── study_tools.py            # Study tools (notes, flashcards, timer)
├── video_essay_generator.py  # Video essay generation module
├── brain.py                  # Original AI assistant (legacy)
├── gui.py                    # Original GUI (legacy)
├── logic_engine.py           # Input analysis engine
└── updater.py                # Updater utility
```

## 🔒 Data Storage

Study Hub stores your data locally in JSON files:
- `notes.json` - Your study notes
- `study_progress.json` - Progress tracking data
- `memory.json` - AI conversation history
- `tasks.json` - Task list (legacy)

## 🛠️ Troubleshooting

### Ollama Connection Issues
- Ensure Ollama is running: `ollama serve`
- Check if llama3 model is installed: `ollama list`
- Verify Ollama is running on port 11434

### TTS (Text-to-Speech) Issues
- TTS is optional and requires `pyttsx3`
- If TTS fails, the app will continue to work normally
- Install TTS dependencies: `pip install pyttsx3`

### GUI Display Issues
- Ensure `customtkinter` is installed: `pip install customtkinter`
- Update to the latest version: `pip install --upgrade customtkinter`
- Check your display scaling settings

## 🤝 Contributing

Contributions are welcome! Here are some ideas:
- Add more educational games
- Improve AI teacher prompts
- Add new study tools
- Enhance the UI/UX
- Add export/import features for notes and flashcards
- Integrate more AI models

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Powered by [Ollama](https://ollama.ai) and LLaMA 3
- Inspired by the need for better educational tools

## 📧 Support

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Happy Learning! 📚✨**
