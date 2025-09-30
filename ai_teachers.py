# ai_teachers.py - AI Teacher Module for Study Hub
import json
import requests
import os

class AITeacher:
    """Base class for AI teachers with subject-specific expertise"""
    
    def __init__(self, subject, model_name="llama3", ollama_url="http://localhost:11434/api/chat"):
        self.subject = subject
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.conversation_history = []
        self.system_prompt = self._get_system_prompt()
        
    def _get_system_prompt(self):
        """Get subject-specific system prompt"""
        prompts = {
            "math": "You are an expert Math teacher. Explain concepts clearly, provide step-by-step solutions, and use examples. Focus on building understanding, not just giving answers.",
            "science": "You are an expert Science teacher. Explain scientific concepts with real-world examples, break down complex topics, and encourage curiosity and experimentation.",
            "history": "You are an expert History teacher. Provide historical context, explain cause and effect, connect past events to present day, and make history engaging and relevant.",
            "language": "You are an expert Language teacher. Help with grammar, vocabulary, writing, and reading comprehension. Provide clear explanations and practice exercises.",
            "coding": "You are an expert Programming teacher. Explain coding concepts clearly, provide code examples, debug issues, and teach best practices.",
            "general": "You are a knowledgeable and patient tutor. Help students learn any subject by breaking down complex topics, providing examples, and adapting to their learning style."
        }
        return prompts.get(self.subject.lower(), prompts["general"])
    
    def ask(self, question):
        """Ask the AI teacher a question"""
        # Add system prompt if this is the first message
        if not self.conversation_history:
            self.conversation_history.append({
                "role": "system",
                "content": self.system_prompt
            })
        
        self.conversation_history.append({"role": "user", "content": question})
        
        try:
            res = requests.post(self.ollama_url, json={
                "model": self.model_name,
                "messages": self.conversation_history,
                "stream": False
            }, timeout=30)
            
            reply = res.json()["message"]["content"].strip()
        except Exception as e:
            reply = f"Error communicating with AI: {str(e)}"
        
        self.conversation_history.append({"role": "assistant", "content": reply})
        return reply
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def save_conversation(self, filename):
        """Save conversation to file"""
        with open(filename, "w") as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def generate_practice_problems(self, topic, difficulty="medium", count=5):
        """Generate practice problems for a topic"""
        prompt = f"Generate {count} {difficulty} difficulty practice problems about {topic}. Include the answers at the end."
        return self.ask(prompt)
    
    def explain_topic(self, topic, detail_level="detailed"):
        """Explain a topic in detail"""
        levels = {
            "simple": "Explain this like I'm 10 years old",
            "medium": "Explain this for a high school student",
            "detailed": "Provide a comprehensive explanation",
            "advanced": "Provide an advanced, in-depth explanation"
        }
        prompt = f"{levels.get(detail_level, levels['medium'])}: {topic}"
        return self.ask(prompt)


class MathTeacher(AITeacher):
    """Specialized Math teacher"""
    
    def __init__(self, model_name="llama3", ollama_url="http://localhost:11434/api/chat"):
        super().__init__("math", model_name, ollama_url)
    
    def solve_step_by_step(self, problem):
        """Solve a math problem with step-by-step explanation"""
        prompt = f"Solve this math problem step by step, explaining each step clearly:\n{problem}"
        return self.ask(prompt)


class ScienceTeacher(AITeacher):
    """Specialized Science teacher"""
    
    def __init__(self, model_name="llama3", ollama_url="http://localhost:11434/api/chat"):
        super().__init__("science", model_name, ollama_url)
    
    def explain_experiment(self, experiment):
        """Explain a scientific experiment"""
        prompt = f"Explain this scientific experiment, including the hypothesis, method, and expected results:\n{experiment}"
        return self.ask(prompt)


class HistoryTeacher(AITeacher):
    """Specialized History teacher"""
    
    def __init__(self, model_name="llama3", ollama_url="http://localhost:11434/api/chat"):
        super().__init__("history", model_name, ollama_url)
    
    def timeline_events(self, topic):
        """Create a timeline of historical events"""
        prompt = f"Create a chronological timeline of key events related to: {topic}"
        return self.ask(prompt)


class LanguageTeacher(AITeacher):
    """Specialized Language teacher"""
    
    def __init__(self, model_name="llama3", ollama_url="http://localhost:11434/api/chat"):
        super().__init__("language", model_name, ollama_url)
    
    def grammar_check(self, text):
        """Check grammar and provide corrections"""
        prompt = f"Check this text for grammar errors and provide corrections with explanations:\n{text}"
        return self.ask(prompt)


class CodingTeacher(AITeacher):
    """Specialized Coding teacher"""
    
    def __init__(self, model_name="llama3", ollama_url="http://localhost:11434/api/chat"):
        super().__init__("coding", model_name, ollama_url)
    
    def debug_code(self, code, error_message=""):
        """Help debug code"""
        prompt = f"Help debug this code:\n```\n{code}\n```\n"
        if error_message:
            prompt += f"Error message: {error_message}"
        return self.ask(prompt)
    
    def explain_code(self, code):
        """Explain what code does"""
        prompt = f"Explain what this code does, line by line:\n```\n{code}\n```"
        return self.ask(prompt)
