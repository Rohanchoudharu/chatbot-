import re
from datetime import datetime
import subprocess
import os
import time

class SimpleChatbot:
    def __init__(self):
        self.name = "ChatBot"
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
            text_escaped = text.replace('"', '\"').replace('$', '`$')
            ps_command = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text_escaped}")'
            subprocess.run(['powershell', '-Command', ps_command], capture_output=True, timeout=30)
        except Exception as e:
            print(f"⚠️  Voice output error: {e}\n")

    def record_and_transcribe_powershell(self):
        """Record audio using Windows built-in voice recognition"""
        try:
            # Create a PowerShell script to record and transcribe speech
            ps_script = '''
[System.Reflection.Assembly]::LoadWithPartialName('System.Speech') | Out-Null
$recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine
$recognizer.LoadGrammar((New-Object System.Speech.Recognition.Grammar([System.Speech.Recognition.SrgsGrammar.SrgsDocument]::FromFile("C:\\temp\\grammar.xml"))))

try {
    $recognizer.SetInputToDefaultAudioDevice()
    $result = $recognizer.Recognize(5)
    if ($result) {
        Write-Host $result.Text
    }
} catch {
    Write-Host ""
}
'''
            result = subprocess.run(['powershell', '-Command', ps_script], 
                                    capture_output=True, text=True, timeout=15)
            return result.stdout.strip() if result.stdout.strip() else None
        except Exception as e:
            print(f"Note: {e}")
            return None

    def listen_voice(self):
        """Listen for voice input using Windows Speech Recognition via PowerShell"""
        try:
            print("\n🎤 Listening... (speak clearly for 10 seconds)")
            
            # PowerShell script for Windows speech recognition
            ps_script = '''
$ErrorActionPreference = "SilentlyContinue"
try {
    Add-Type -AssemblyName System.Speech
    $recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine
    $recognizer.SetInputToDefaultAudioDevice()
    $result = $recognizer.Recognize([timespan]::fromseconds(10))
    
    if ($result -and $result.Text) {
        Write-Host $result.Text
    } else {
        Write-Host ""
    }
} catch {
    Write-Host ""
}
'''
            
            # Run PowerShell script
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', ps_script],
                capture_output=True, 
                text=True, 
                timeout=15
            )
            
            text = result.stdout.strip()
            
            if text and len(text) > 0:
                print(f"✓ You: {text}\n")
                return text
            else:
                print("❌ No speech detected. Try speaking louder.\n")
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ Listening timed out.\n")
            return None
        except Exception as e:
            print(f"❌ Voice recognition not available: {e}\n")
            return None

    def listen_text(self):
        """Get text input"""
        user_input = input("📝 Type your message: ").strip()
        return user_input

    def listen(self):
        """Listen for input - try voice first, fallback to text"""
        print("Attempting voice input...")
        
        user_input = self.listen_voice()
        if user_input is None or user_input == "":
            print("💬 Switching to text input mode...\n")
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

if __name__ == "__main__":
    chatbot = SimpleChatbot()
    chatbot.chat()
