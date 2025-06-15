 # gui.py – NECRO GUI (ChatGPT-style interface)
import customtkinter as ctk
import tkinter as tk
import json, requests, os

# === SETTINGS ===
MODEL_NAME = "llama3"
OLLAMA_URL = "http://localhost:11434/api/chat"
HISTORY_FILE = "memory.json"
TASKS_FILE = "tasks.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# === INIT MEMORY ===
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE) as f:
        chat_history = json.load(f)
else:
    chat_history = []

TTS_ENABLED = False

# === GUI CLASS ===
class NecroGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Necro AI Assistant")
        self.geometry("800x600")
        self.configure(padx=10, pady=10)

        # Chat log
        self.chat_display = ctk.CTkTextbox(self, width=750, height=450, wrap=tk.WORD)
        self.chat_display.pack(pady=(0,10))
        self.chat_display.insert(tk.END, "🤖 NECRO READY.\n\n")
        self.chat_display.configure(state="disabled")

        # Input frame
        self.entry_frame = ctk.CTkFrame(self)
        self.entry_frame.pack(fill=tk.X)

        self.entry = ctk.CTkEntry(self.entry_frame, width=600)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5), pady=5)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=5)

        # Buttons below
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=5)

        self.mute_button = ctk.CTkButton(self.button_frame, text="🔇 Mute", command=self.toggle_tts)
        self.mute_button.grid(row=0, column=0, padx=5)

        self.task_button = ctk.CTkButton(self.button_frame, text="📋 Show Tasks", command=self.show_tasks)
        self.task_button.grid(row=0, column=1, padx=5)

        self.clear_button = ctk.CTkButton(self.button_frame, text="🗑️ Clear Chat", command=self.clear_chat)
        self.clear_button.grid(row=0, column=2, padx=5)

    def toggle_tts(self):
        global TTS_ENABLED
        TTS_ENABLED = not TTS_ENABLED
        self.mute_button.configure(text="🔊 Unmute" if not TTS_ENABLED else "🔇 Mute")

    def clear_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.insert(tk.END, "🤖 NECRO RESET.\n\n")
        self.chat_display.configure(state="disabled")

    def show_tasks(self):
        if not os.path.exists(TASKS_FILE):
            self.print_message("📝 No tasks saved.")
            return
        with open(TASKS_FILE) as f:
            tasks = json.load(f)
        if not tasks:
            self.print_message("📝 Task list is empty.")
        else:
            self.print_message("📋 TASKS:")
            for i, t in enumerate(tasks, 1):
                self.print_message(f"  {i}. {t['task']}")

import threading  # ⬅️ Make sure this is at the top of your file

def send_message(self, event=None):
    user_input = self.entry.get().strip()
    if not user_input: return
    self.entry.delete(0, tk.END)
    self.print_message(f"You: {user_input}")

    # Run AI call in a separate thread to avoid freezing
    def run_ai():
        response = self.ask_necro(user_input)
        self.print_message(f"Necro: {response}")
        if TTS_ENABLED:
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(response)
                engine.runAndWait()
            except:
                self.print_message("⚠️ TTS failed.")

    threading.Thread(target=run_ai, daemon=True).start()


    def ask_necro(self, prompt):
        global chat_history
        chat_history.append({"role": "user", "content": prompt})
        try:
            res = requests.post(OLLAMA_URL, json={
                "model": MODEL_NAME,
                "messages": chat_history,
                "stream": False
            })
            reply = res.json()["message"]["content"].strip()
        except Exception as e:
            reply = f"[Error]: {e}"

        chat_history.append({"role": "assistant", "content": reply})
        with open(HISTORY_FILE, "w") as f:
            json.dump(chat_history, f)
        return reply

    def print_message(self, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, message + "\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.configure(state="disabled")


if __name__ == "__main__":
    app = NecroGUI()
    app.mainloop()

