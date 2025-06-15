# brain.py – FINAL BUILD FOR NECRO AI
import os, json, time, requests, pyttsx3, subprocess, datetime
from vosk import Model, KaldiRecognizer
import pyaudio
from logic_engine import analyze_input
import updater
updater.run_updater()

# === NECRO SETTINGS ===
TTS_ENABLED = False  # Toggle with "mute voice" or "unmute voice"
AUTHORIZED_USER = "jrbucio"
AI_NAME = "Necro"
MODEL_NAME = "llama3"
OLLAMA_URL = "http://localhost:11434/api/chat"
HISTORY_FILE = "memory.json"
TASKS_FILE = "tasks.json"
LAST_RESPONSE_FILE = "last_response.txt"
VOSK_PATH = "vosk-model"

# === MEMORY ===
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE) as f:
        history = json.load(f)
else:
    history = []

# === TASK MEMORY ===
if os.path.exists(TASKS_FILE):
    with open(TASKS_FILE) as f:
        tasks = json.load(f)
else:
    tasks = []

# === TTS OUTPUT ===
def speak(text):
    print(f"{AI_NAME}: {text}")
    if TTS_ENABLED:
        engine.say(text)
        engine.runAndWait()
    with open(LAST_RESPONSE_FILE, "w") as f:
        f.write(text)

# === STT INPUT ===
model = Model(VOSK_PATH)
rec = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio().open(rate=16000, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=8000)
mic.start_stream()

def get_voice_input():
    print("🎤 Listening...")
    while True:
        data = mic.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())["text"]
            if result:
                print(f"{AUTHORIZED_USER}: {result}")
                return result
# === LOGIC + RESPONSE FLOW ===
def ask(prompt):
    # Logic engine: alerts if destructive, vague, etc.
    alerts = analyze_input(prompt)
    if alerts:
        for alert in alerts:
            speak(f"⚠️ {alert}")
        return "Alert raised. Please confirm your intent."

    history.append({"role": "user", "content": prompt})
    res = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "messages": history,
        "stream": False
    })

    try:
        reply = res.json()["message"]["content"].strip()
    except:
        reply = "Something went wrong processing my response."

    history.append({"role": "assistant", "content": reply})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

    return reply

# === TASK SCHEDULER ===
def add_task(task):
    timestamp = datetime.datetime.now().isoformat()
    tasks.append({"task": task, "created": timestamp})
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)
    speak(f"Task added: {task}")

def list_tasks():
    if not tasks:
        speak("You have no tasks.")
    else:
        for i, t in enumerate(tasks, 1):
            speak(f"Task {i}: {t['task']}")

def clear_tasks():
    tasks.clear()
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)
    speak("All tasks cleared.")

# === TERMINAL COMMAND EXECUTION ===
def run_command(cmd, user):
    if user != AUTHORIZED_USER:
        speak("Unauthorized user. Command denied.")
        return
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
        speak("Command executed.")
        print(output.decode())
    except subprocess.CalledProcessError as e:
        speak(f"Command error: {e}")
    except Exception as e:
        speak(f"Failed: {e}")

# === SELF-CORRECTION BASE ===
def review_last_response():
    if os.path.exists(LAST_RESPONSE_FILE):
        with open(LAST_RESPONSE_FILE) as f:
            last = f.read()
        speak("My last response was:")
        speak(last)
    else:
        speak("No response history found.")
# === PERSONALITY MEMORY ===
personality = {
    "tone": "balanced",
    "style": "adaptive",
    "humor": True,
    "formality": "casual"
}

def apply_personality(text):
    if not personality["humor"]:
        text = text.replace("😄", "").replace("😂", "")
    if personality["formality"] == "formal":
        text = text.replace("wanna", "want to").replace("gonna", "going to")
    return text

# === FINAL MAIN LOOP ===
print(f"🧠 {AI_NAME.upper()} is active. Say 'exit' to shut down.")

while True:
    user_input = get_voice_input()

    if user_input.lower() in ['exit', 'quit', 'shutdown']:
        speak(f"{AI_NAME} shutting down. Goodbye, {AUTHORIZED_USER}.")
        break

    # Commands & Triggers
    if user_input.lower().startswith("run command"):
        command = user_input[11:].strip()
        run_command(command, AUTHORIZED_USER)
        continue

    elif "mute voice" in user_input.lower():
        TTS_ENABLED = False
        print("🔇 Voice muted.")
        continue

    elif "unmute voice" in user_input.lower():
        TTS_ENABLED = True
        print("🔊 Voice unmuted.")
        continue

    elif user_input.lower().startswith("add task"):
        task = user_input[8:].strip()
        add_task(task)
        continue

    elif "list tasks" in user_input.lower():
        list_tasks()
        continue

    elif "clear tasks" in user_input.lower():
        clear_tasks()
        continue

    elif "review response" in user_input.lower():
        review_last_response()
        continue

    elif "change tone to" in user_input.lower():
        tone = user_input.split("change tone to")[-1].strip()
        personality["tone"] = tone
        speak(f"Tone changed to {tone}.")
        continue

    # Default: Talk to LLaMA
    response = ask(user_input)
    response = apply_personality(response)
    speak(response)
