# video_essay_generator.py - AI Video Essay Generator Module
import json
import requests
import os
from datetime import datetime

class VideoEssayGenerator:
    """Generate long-form educational video essays using AI"""
    
    def __init__(self, model_name="llama3", ollama_url="http://localhost:11434/api/chat"):
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.essays = []
        
    def generate_essay_outline(self, topic, duration_minutes=10):
        """Generate an outline for a video essay"""
        prompt = f"""Create a detailed outline for a {duration_minutes}-minute educational video essay about: {topic}

Please structure the outline with:
1. Introduction (hook and thesis)
2. Main sections (3-5 key points)
3. Examples and explanations for each point
4. Conclusion (summary and takeaways)

Make it engaging, informative, and suitable for visual presentation."""

        try:
            res = requests.post(self.ollama_url, json={
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }, timeout=60)
            
            outline = res.json()["message"]["content"].strip()
            return outline
        except Exception as e:
            return f"Error generating outline: {str(e)}"
    
    def generate_full_script(self, topic, duration_minutes=10, detail_level="detailed"):
        """Generate a complete video essay script"""
        sections_needed = max(3, duration_minutes // 3)
        
        prompt = f"""Write a complete {duration_minutes}-minute educational video essay script about: {topic}

Requirements:
- Write in a conversational, engaging tone
- Include {sections_needed} main sections
- Each section should flow naturally to the next
- Include interesting facts, examples, and explanations
- Add suggestions for visuals in [brackets]
- Make it suitable for narration
- Total word count should be approximately {duration_minutes * 150} words

Start with a hook, develop the content thoroughly, and end with a memorable conclusion."""

        try:
            res = requests.post(self.ollama_url, json={
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }, timeout=120)
            
            script = res.json()["message"]["content"].strip()
            
            essay_data = {
                "topic": topic,
                "duration_minutes": duration_minutes,
                "script": script,
                "created_at": datetime.now().isoformat(),
                "word_count": len(script.split())
            }
            
            self.essays.append(essay_data)
            return essay_data
        except Exception as e:
            return {"error": f"Error generating script: {str(e)}"}
    
    def expand_section(self, section_topic, target_words=500):
        """Expand a specific section with more detail"""
        prompt = f"""Expand on this topic in detail for an educational video essay: {section_topic}

Write approximately {target_words} words with:
- Clear explanations
- Interesting examples
- Relevant context
- Engaging narrative style
- Suggestions for visuals in [brackets]"""

        try:
            res = requests.post(self.ollama_url, json={
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }, timeout=60)
            
            expanded_content = res.json()["message"]["content"].strip()
            return expanded_content
        except Exception as e:
            return f"Error expanding section: {str(e)}"
    
    def generate_visual_suggestions(self, script_excerpt):
        """Generate suggestions for visuals to accompany the script"""
        prompt = f"""For this video essay script excerpt, suggest specific visuals, animations, or graphics that would enhance the presentation:

{script_excerpt}

Provide 5-10 specific visual suggestions with descriptions."""

        try:
            res = requests.post(self.ollama_url, json={
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }, timeout=30)
            
            suggestions = res.json()["message"]["content"].strip()
            return suggestions
        except Exception as e:
            return f"Error generating visual suggestions: {str(e)}"
    
    def generate_quiz_from_essay(self, essay_script):
        """Generate a quiz based on the essay content"""
        prompt = f"""Based on this video essay script, create 10 multiple-choice questions to test understanding:

{essay_script[:2000]}...

Format each question as:
Q: [question]
A) [option]
B) [option]
C) [option]
D) [option]
Answer: [correct letter]"""

        try:
            res = requests.post(self.ollama_url, json={
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }, timeout=45)
            
            quiz = res.json()["message"]["content"].strip()
            return quiz
        except Exception as e:
            return f"Error generating quiz: {str(e)}"
    
    def save_essay(self, essay_data, filename):
        """Save essay to file"""
        with open(filename, "w") as f:
            json.dump(essay_data, f, indent=2)
    
    def load_essay(self, filename):
        """Load essay from file"""
        with open(filename, "r") as f:
            return json.load(f)
    
    def get_estimated_duration(self, text, words_per_minute=150):
        """Estimate duration based on word count"""
        word_count = len(text.split())
        minutes = word_count / words_per_minute
        return minutes
    
    def generate_series(self, main_topic, num_episodes=5, episode_duration=10):
        """Generate a series of related video essays"""
        prompt = f"""Create an outline for a {num_episodes}-episode educational video series about: {main_topic}

For each episode, provide:
1. Episode title
2. Key topics covered
3. Learning objectives
4. Brief episode summary

Each episode should be approximately {episode_duration} minutes."""

        try:
            res = requests.post(self.ollama_url, json={
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }, timeout=60)
            
            series_outline = res.json()["message"]["content"].strip()
            return series_outline
        except Exception as e:
            return f"Error generating series: {str(e)}"
    
    def create_study_guide(self, essay_script):
        """Create a study guide from the essay"""
        prompt = f"""Create a comprehensive study guide based on this video essay:

{essay_script[:2000]}...

Include:
1. Key concepts and definitions
2. Main points and arguments
3. Important facts and figures
4. Discussion questions
5. Further reading suggestions"""

        try:
            res = requests.post(self.ollama_url, json={
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }, timeout=45)
            
            study_guide = res.json()["message"]["content"].strip()
            return study_guide
        except Exception as e:
            return f"Error creating study guide: {str(e)}"


class TextToSpeechConverter:
    """Convert text scripts to speech (placeholder for TTS integration)"""
    
    def __init__(self):
        self.available = False
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.available = True
        except:
            self.engine = None
    
    def text_to_speech(self, text, output_file=None, rate=150):
        """Convert text to speech"""
        if not self.available:
            return "TTS engine not available"
        
        self.engine.setProperty('rate', rate)
        
        if output_file:
            self.engine.save_to_file(text, output_file)
            self.engine.runAndWait()
            return f"Saved to {output_file}"
        else:
            self.engine.say(text)
            self.engine.runAndWait()
            return "Speech completed"
    
    def get_available_voices(self):
        """Get list of available voices"""
        if not self.available:
            return []
        
        voices = self.engine.getProperty('voices')
        return [{"id": v.id, "name": v.name} for v in voices]
    
    def set_voice(self, voice_id):
        """Set the TTS voice"""
        if self.available:
            self.engine.setProperty('voice', voice_id)
