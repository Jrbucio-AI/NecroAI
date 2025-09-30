# educational_games.py - Educational Games Module for Study Hub
import random
import time
import json

class EducationalGame:
    """Base class for educational games"""
    
    def __init__(self, name, difficulty="medium"):
        self.name = name
        self.difficulty = difficulty
        self.score = 0
        self.questions_answered = 0
        self.correct_answers = 0
        
    def get_score(self):
        """Get current score"""
        return self.score
    
    def get_accuracy(self):
        """Get accuracy percentage"""
        if self.questions_answered == 0:
            return 0
        return (self.correct_answers / self.questions_answered) * 100
    
    def reset_stats(self):
        """Reset game statistics"""
        self.score = 0
        self.questions_answered = 0
        self.correct_answers = 0


class MathGame(EducationalGame):
    """Math practice games"""
    
    def __init__(self, difficulty="medium"):
        super().__init__("Math Challenge", difficulty)
        self.operations = {
            "easy": ["+", "-"],
            "medium": ["+", "-", "*"],
            "hard": ["+", "-", "*", "/"]
        }
        
    def generate_problem(self):
        """Generate a random math problem"""
        ops = self.operations.get(self.difficulty, self.operations["medium"])
        operation = random.choice(ops)
        
        if self.difficulty == "easy":
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
        elif self.difficulty == "medium":
            num1 = random.randint(1, 50)
            num2 = random.randint(1, 50)
        else:
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
        
        # Adjust for division to avoid decimals
        if operation == "/":
            num1 = num2 * random.randint(1, 10)
        
        problem = f"{num1} {operation} {num2}"
        answer = eval(problem)
        
        return problem, answer
    
    def check_answer(self, problem, user_answer):
        """Check if the answer is correct"""
        _, correct_answer = problem, eval(problem.replace("÷", "/").replace("×", "*"))
        self.questions_answered += 1
        
        try:
            is_correct = abs(float(user_answer) - correct_answer) < 0.01
            if is_correct:
                self.correct_answers += 1
                self.score += 10 * (1 if self.difficulty == "easy" else 2 if self.difficulty == "medium" else 3)
            return is_correct, correct_answer
        except:
            return False, correct_answer


class VocabularyGame(EducationalGame):
    """Vocabulary building game"""
    
    def __init__(self, difficulty="medium"):
        super().__init__("Vocabulary Builder", difficulty)
        self.word_lists = self._load_word_lists()
        
    def _load_word_lists(self):
        """Load word lists by difficulty"""
        return {
            "easy": [
                {"word": "happy", "definition": "feeling pleasure or joy", "synonym": "joyful"},
                {"word": "big", "definition": "large in size", "synonym": "large"},
                {"word": "fast", "definition": "moving quickly", "synonym": "quick"},
                {"word": "smart", "definition": "intelligent", "synonym": "clever"},
                {"word": "kind", "definition": "friendly and caring", "synonym": "nice"},
            ],
            "medium": [
                {"word": "ambiguous", "definition": "open to multiple interpretations", "synonym": "unclear"},
                {"word": "benevolent", "definition": "kind and generous", "synonym": "charitable"},
                {"word": "candid", "definition": "truthful and straightforward", "synonym": "honest"},
                {"word": "diligent", "definition": "showing care and effort", "synonym": "hardworking"},
                {"word": "eloquent", "definition": "fluent and persuasive in speaking", "synonym": "articulate"},
            ],
            "hard": [
                {"word": "ephemeral", "definition": "lasting for a very short time", "synonym": "transient"},
                {"word": "facetious", "definition": "treating serious issues with inappropriate humor", "synonym": "flippant"},
                {"word": "gregarious", "definition": "fond of company; sociable", "synonym": "outgoing"},
                {"word": "heterogeneous", "definition": "diverse in character or content", "synonym": "varied"},
                {"word": "incongruous", "definition": "not in harmony or keeping with", "synonym": "incompatible"},
            ]
        }
    
    def get_random_word(self):
        """Get a random word for practice"""
        words = self.word_lists.get(self.difficulty, self.word_lists["medium"])
        return random.choice(words)
    
    def check_definition(self, word_data, user_definition):
        """Check if the definition is close enough"""
        self.questions_answered += 1
        correct_definition = word_data["definition"].lower()
        user_def_lower = user_definition.lower()
        
        # Simple matching - check if key words are present
        key_words = correct_definition.split()
        matches = sum(1 for word in key_words if len(word) > 3 and word in user_def_lower)
        
        is_correct = matches >= len(key_words) * 0.5
        if is_correct:
            self.correct_answers += 1
            self.score += 15
        
        return is_correct, correct_definition


class MemoryGame(EducationalGame):
    """Memory matching game for learning"""
    
    def __init__(self, topic="general", difficulty="medium"):
        super().__init__("Memory Match", difficulty)
        self.topic = topic
        self.cards = []
        self.matched_pairs = 0
        
    def create_deck(self, pairs):
        """Create a deck of cards for matching"""
        # pairs is a list of tuples (item1, item2)
        deck = []
        for i, (item1, item2) in enumerate(pairs):
            deck.append({"id": i, "content": item1, "matched": False})
            deck.append({"id": i, "content": item2, "matched": False})
        random.shuffle(deck)
        self.cards = deck
        return deck
    
    def check_match(self, card1_index, card2_index):
        """Check if two cards match"""
        if card1_index >= len(self.cards) or card2_index >= len(self.cards):
            return False
        
        card1 = self.cards[card1_index]
        card2 = self.cards[card2_index]
        
        if card1["id"] == card2["id"] and not card1["matched"]:
            self.cards[card1_index]["matched"] = True
            self.cards[card2_index]["matched"] = True
            self.matched_pairs += 1
            self.score += 20
            return True
        return False


class TypingGame(EducationalGame):
    """Typing speed and accuracy game"""
    
    def __init__(self, difficulty="medium"):
        super().__init__("Type Master", difficulty)
        self.texts = self._load_texts()
        
    def _load_texts(self):
        """Load practice texts by difficulty"""
        return {
            "easy": [
                "The quick brown fox jumps over the lazy dog.",
                "Practice makes perfect.",
                "Learning is a lifelong journey.",
            ],
            "medium": [
                "Education is the most powerful weapon which you can use to change the world.",
                "The beautiful thing about learning is that no one can take it away from you.",
                "Success is the sum of small efforts repeated day in and day out.",
            ],
            "hard": [
                "In the midst of chaos, there is also opportunity. Knowledge is power, and with great power comes great responsibility.",
                "The capacity to learn is a gift; the ability to learn is a skill; the willingness to learn is a choice.",
                "Intelligence plus character - that is the goal of true education. We must remember that intelligence is not enough.",
            ]
        }
    
    def get_text(self):
        """Get a random text for typing practice"""
        texts = self.texts.get(self.difficulty, self.texts["medium"])
        return random.choice(texts)
    
    def calculate_wpm(self, text, time_seconds, errors=0):
        """Calculate words per minute"""
        words = len(text.split())
        minutes = time_seconds / 60
        wpm = words / minutes if minutes > 0 else 0
        accuracy = max(0, 100 - (errors * 5))
        return wpm, accuracy


class QuizGame(EducationalGame):
    """General knowledge quiz game"""
    
    def __init__(self, subject="general", difficulty="medium"):
        super().__init__("Quiz Master", difficulty)
        self.subject = subject
        
    def create_quiz(self, questions):
        """Create a quiz from a list of questions"""
        # questions format: [{"question": "...", "options": [...], "answer": "..."}]
        self.quiz_questions = questions
        random.shuffle(self.quiz_questions)
        return self.quiz_questions
    
    def check_answer(self, question_index, user_answer):
        """Check quiz answer"""
        if question_index >= len(self.quiz_questions):
            return False, ""
        
        question = self.quiz_questions[question_index]
        correct_answer = question.get("answer", "")
        
        self.questions_answered += 1
        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
        
        if is_correct:
            self.correct_answers += 1
            self.score += 10
        
        return is_correct, correct_answer


# Sample quiz data generator
def generate_sample_quizzes():
    """Generate sample quiz questions for different subjects"""
    return {
        "science": [
            {
                "question": "What is the chemical symbol for water?",
                "options": ["H2O", "O2", "CO2", "H2"],
                "answer": "H2O"
            },
            {
                "question": "What planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "answer": "Mars"
            },
        ],
        "history": [
            {
                "question": "In what year did World War II end?",
                "options": ["1943", "1944", "1945", "1946"],
                "answer": "1945"
            },
            {
                "question": "Who was the first President of the United States?",
                "options": ["Thomas Jefferson", "George Washington", "John Adams", "Benjamin Franklin"],
                "answer": "George Washington"
            },
        ],
        "math": [
            {
                "question": "What is the square root of 144?",
                "options": ["10", "11", "12", "13"],
                "answer": "12"
            },
            {
                "question": "What is 15% of 200?",
                "options": ["20", "25", "30", "35"],
                "answer": "30"
            },
        ]
    }
