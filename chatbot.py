import re
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import threading
import sys
import os

class SimpleChatbot:
    def __init__(self):
        self.name = "ChatBot"
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech with error handling
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)  # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume level
            # Set default voice
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)
            self.use_voice = True
        except Exception as e:
            print(f"⚠️  Text-to-speech initialization error: {e}")
            self.use_voice = False
        
        self.use_voice = True  # Flag to track if voice is working
        self.responses = {
            r'\bhello\b|\bhi\b|\bhey\b': [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Hey! What's on your mind?"
            ],
            r'\bhow are you\b|\bhow\'s it going\b': [
                "I'm doing great! Thanks for asking.",
                "I'm functioning well, thank you!",
                "All systems operational! How about you?"
            ],
            r'\bwhat\'s your name\b|\bwho are you\b': [
                f"I'm {self.name}, your personal assistant!",
                "I'm a simple chatbot here to help you.",
                "You can call me ChatBot!"
            ],
            r'\bwhat time is it\b|\bcurrent time\b': [
                lambda: f"The current time is {datetime.now().strftime('%H:%M:%S')}",
                lambda: f"It's {datetime.now().strftime('%I:%M %p')} right now.",
            ],
            r'\bwhat\'s the date\b|\btoday\'s date\b': [
                lambda: f"Today's date is {datetime.now().strftime('%B %d, %Y')}",
                lambda: f"It's {datetime.now().strftime('%A, %B %d, %Y')}",
            ],
            r'\bhelp\b|\bwhat can you do\b|\bcapabilities\b': [
                "I can answer simple questions, tell you the time/date, and chat with you!",
                "Try asking me about the time, date, or just have a casual conversation!",
                "I can: greet you, tell the time, share the date, and answer basic questions."
            ],
            r'\bthanks\b|\bthank you\b|\bappreciate it\b': [
                "You're welcome!",
                "Happy to help!",
                "Anytime! Glad I could assist."
            ],
            r'\bgoodbye\b|\bbye\b|\bsee you\b': [
                "Goodbye! Have a great day!",
                "See you later!",
                "Bye! Take care!"
            ],
            r'\bhow do i\b.*': [
                "I'd be happy to help! Can you be more specific about what you need?",
                "That's a good question! Try to be more specific so I can help better.",
            ],
        }
        self.default_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "That's interesting! Tell me more.",
            "I'm still learning. Can you ask me something else?",
            "Sorry, I didn't quite catch that. Try asking differently!",
        ]

    def get_response(self, user_input):
        """Generate a response based on user input"""
        user_input_lower = user_input.lower().strip()
        
        # Check against each pattern
        for pattern, responses in self.responses.items():
            if re.search(pattern, user_input_lower):
                # Select a response
                response = responses[0] if responses else "I don't know how to respond."
                
                # If it's a callable (lambda), call it
                if callable(response):
                    return response()
                return response
        
        # Default response
        import random
        return random.choice(self.default_responses)

    def speak(self, text):
        """Convert text to speech"""
        print(f"🤖 ChatBot: {text}\n")
        
        if not self.use_voice:
            return
        
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"⚠️  Voice output error: {e}")
            print("Continuing without voice...\n")

    def listen(self):
        """Listen for voice input and convert to text"""
        try:
            print("\n🎤 Listening... (speak now)")
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                # Set sensitivity
                self.recognizer.energy_threshold = 4000
                # Listen for longer (10 seconds)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            try:
                print("🔄 Processing speech...")
                user_input = self.recognizer.recognize_google(audio)
                print(f"✓ You: {user_input}\n")
                return user_input
            except sr.UnknownValueError:
                print("❌ Could not understand audio. Try speaking again.")
                return ""
            except sr.RequestError as e:
                print(f"❌ API Error: {e}")
                return ""
        except Exception as e:
            print(f"❌ Microphone Error: {e}")
            print("💬 Switching to text input mode...\n")
            self.use_voice = False
            return self.fallback_input()

    def fallback_input(self):
        """Fallback to text input if voice doesn't work"""
        user_input = input("📝 Type your message: ").strip()
        return user_input

    def chat(self):
        """Start the voice chatbot conversation"""
        print(f"\n{'='*50}")
        print(f"Welcome to {self.name}!")
        print("Say 'goodbye' to exit.")
        print(f"{'='*50}\n")
        
        # Greeting with voice
        greeting = f"Welcome to {self.name}! I'm ready to listen to your questions."
        self.speak(greeting)
        
        while True:
            try:
                user_input = self.listen()
                
                if not user_input:
                    continue
                
                # Check for exit conditions
                if re.search(r'\b(goodbye|bye|exit|quit)\b', user_input.lower()):
                    response = self.get_response(user_input)
                    self.speak(response)
                    break
                
                response = self.get_response(user_input)
                self.speak(response)
                
            except KeyboardInterrupt:
                self.speak("Goodbye! Thanks for chatting!")
                break
            except Exception as e:
                self.speak(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    chatbot = SimpleChatbot()
    chatbot.chat()
