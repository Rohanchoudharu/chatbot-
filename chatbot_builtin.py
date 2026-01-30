import re
from datetime import datetime
import speech_recognition as sr
import os
import subprocess

class SimpleChatbot:
    def __init__(self):
        self.name = "ChatBot"
        self.recognizer = sr.Recognizer()
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
        
        for pattern, responses in self.responses.items():
            if re.search(pattern, user_input_lower):
                response = responses[0] if responses else "I don't know how to respond."
                if callable(response):
                    return response()
                return response
        
        import random
        return random.choice(self.default_responses)

    def speak(self, text):
        """Convert text to speech using Windows PowerShell"""
        print(f"🤖 ChatBot: {text}\n")
        
        try:
            # Use PowerShell to speak (works on all Windows systems)
            # Escape special characters for PowerShell
            text_escaped = text.replace('"', '\"').replace('$', '`$')
            ps_command = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text_escaped}")'
            subprocess.run(['powershell', '-Command', ps_command], capture_output=True, timeout=30)
        except Exception as e:
            print(f"⚠️  Voice output not available: {e}\n")

    def listen_voice(self):
        """Listen for voice input"""
        try:
            print("\n🎤 Listening... (speak now)")
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.energy_threshold = 4000
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            try:
                print("🔄 Processing speech...")
                user_input = self.recognizer.recognize_google(audio)
                print(f"✓ You: {user_input}\n")
                return user_input
            except sr.UnknownValueError:
                print("❌ Could not understand audio. Switching to text input.\n")
                return None
            except sr.RequestError as e:
                print(f"❌ API Error. Switching to text input.\n")
                return None
        except Exception as e:
            print(f"❌ Microphone Error: {e}. Using text input.\n")
            return None

    def listen_text(self):
        """Get text input"""
        user_input = input("📝 Type your message: ").strip()
        return user_input

    def listen(self):
        """Listen for input - try voice first, fallback to text"""
        user_input = self.listen_voice()
        if user_input is None or user_input == "":
            user_input = self.listen_text()
        return user_input

    def chat(self):
        """Start the chatbot conversation"""
        print(f"\n{'='*50}")
        print(f"Welcome to {self.name}!")
        print("Say or type 'goodbye' to exit.")
        print(f"{'='*50}\n")
        
        greeting = f"Welcome to {self.name}! I'm ready to listen to your questions."
        self.speak(greeting)
        
        while True:
            try:
                user_input = self.listen()
                
                if not user_input:
                    continue
                
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
                print(f"❌ Error: {e}")
                self.speak("An error occurred. Please try again.")

if __name__ == "__main__":
    chatbot = SimpleChatbot()
    chatbot.chat()
