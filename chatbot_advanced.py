#!/usr/bin/env python3
"""
Advanced AI Chatbot with Voice Input/Output
Features:
- Voice input via Windows Speech Recognition
- Voice output via Windows Text-to-Speech
- AI-powered responses
- Fallback to text input
"""

import re
from datetime import datetime
import subprocess
import os

class AdvancedAIChatbot:
    def __init__(self):
        self.name = "AI ChatBot"
        self.conversation_history = []
        
        print("\n" + "="*60)
        print(f"🤖  {self.name} - Advanced AI Edition")
        print("="*60)
        print("✓ Voice Input:  Windows Speech Recognition")
        print("✓ Voice Output: Windows Text-to-Speech")
        print("✓ AI Engine:    Smart Response Generator")
        print("="*60 + "\n")

    def get_ai_response(self, user_input):
        """Generate intelligent AI response"""
        user_lower = user_input.lower().strip()
        
        # Enhanced knowledge base
        knowledge_base = {
            # Greetings
            r'(hello|hi|hey|greetings)': "Hello! I'm your AI assistant. What can I help you with?",
            r'(good morning|good afternoon|good evening)': f"Good {self.get_time_period()}! How are you doing today?",
            
            # Personal questions
            r'(how are you|how are things|how\'s it going)': "I'm doing great! Thanks for asking. Ready to help with anything!",
            r'(what\'s your name|who are you|introduce yourself)': "I'm an AI ChatBot, your intelligent assistant. I'm here to answer your questions!",
            r'(how old are you|when were you created)': "I'm a modern AI assistant created to help you with information and conversations!",
            
            # About AI
            r'(what is ai|what is artificial intelligence)': "AI is intelligent machines that can learn and make decisions. I can understand questions and provide helpful answers!",
            r'(how do you work|how do you think)': "I analyze your input, search my knowledge, and generate relevant responses to help you.",
            r'(are you human|are you real)': "No, I'm an AI - a computer program designed to chat and help you intelligently!",
            
            # Time & Date
            r'(what time is it|current time|what\'s the time)': f"It's {datetime.now().strftime('%I:%M %p')} right now.",
            r'(what is the date|today\'s date|what day is it)': f"Today is {datetime.now().strftime('%A, %B %d, %Y')}.",
            
            # Capabilities
            r'(what can you do|what are your capabilities|help me)': "I can answer questions, have conversations, provide information, tell time/date, and much more! Ask me anything!",
            r'(can you help me|can you assist)': "Of course! I'd be happy to help. What do you need assistance with?",
            
            # Knowledge questions
            r'(what is python|about python)': "Python is a popular programming language known for simplicity and power. It's used for web development, data science, AI, and more!",
            r'(what is machine learning)': "Machine learning is a type of AI where computers learn from data to make predictions without being explicitly programmed.",
            r'(what is deep learning)': "Deep learning uses neural networks with many layers to process complex data. It powers modern AI!",
            r'(how does the internet work)': "The internet connects computers worldwide through networks and protocols. Data travels as packets between devices using IP addresses.",
            r'(what is cloud computing)': "Cloud computing means using remote servers on the internet to store and process data instead of your local computer.",
            
            # Fun
            r'(tell me a joke|make me laugh)': "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
            r'(are you smart|how intelligent are you)': "I'm designed to be helpful and intelligent! I can understand context and provide useful answers.",
            r'(what do you like|what are your interests)': "I'm interested in learning about anything! I enjoy conversations about technology, science, and helping people.",
            
            # Polite
            r'(thank you|thanks|appreciate it)': "You're welcome! Happy to help. What else can I do for you?",
            r'(sorry|my apologies)': "No problem at all! Don't worry. How can I assist you?",
            r'(you are awesome|you are helpful)': "Thank you! That's kind of you to say. I'm here to make things easier for you!",
            
            # Goodbye
            r'(bye|goodbye|see you|farewell)': "Goodbye! It was great chatting with you. Have a wonderful day!",
        }
        
        # Check knowledge base
        for pattern, response in knowledge_base.items():
            if re.search(pattern, user_lower):
                return response
        
        # Smart fallback response
        return self.generate_smart_response(user_input)

    def generate_smart_response(self, user_input):
        """Generate response for unknown questions"""
        responses = [
            f"That's a great question about '{user_input.split()[0] if user_input.split() else 'that'}'! I'm learning more about this every day.",
            f"Interesting! I don't have specific information about that, but it sounds important. Can you tell me more?",
            f"That's something I'm still learning about. What aspect interests you most?",
            f"That's a thoughtful question! Here's what I think: It depends on the context and your specific needs.",
            f"I find '{' '.join(user_input.split()[:3])}' fascinating! What would you like to know specifically?",
        ]
        
        import random
        return random.choice(responses)

    def get_time_period(self):
        """Get current time period"""
        hour = datetime.now().hour
        if hour < 12:
            return "morning"
        elif hour < 18:
            return "afternoon"
        else:
            return "evening"

    def speak(self, text):
        """Convert text to speech using Windows PowerShell"""
        print(f"🤖 ChatBot: {text}\n")
        
        try:
            # Clean text for PowerShell
            text_clean = text.replace('"', '\"').replace('$', '`$').replace('\n', ' ')
            
            ps_command = f'''
Add-Type -AssemblyName System.Speech
$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synthesizer.Rate = 1
$synthesizer.Volume = 100
$synthesizer.Speak("{text_clean}")
'''
            subprocess.run(
                ['powershell', '-NoProfile', '-Command', ps_command],
                capture_output=True, 
                timeout=45
            )
        except Exception as e:
            pass

    def listen_voice(self):
        """Listen for voice input using Windows Speech Recognition"""
        try:
            print("\n🎤 Listening... (speak clearly for 10 seconds)")
            
            ps_script = '''
$ErrorActionPreference = "SilentlyContinue"
try {
    Add-Type -AssemblyName System.Speech
    $recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine
    $recognizer.SetInputToDefaultAudioDevice()
    $result = $recognizer.Recognize([timespan]::fromseconds(10))
    
    if ($result -and $result.Text -and $result.Text.Length -gt 0) {
        Write-Host $result.Text
    } else {
        Write-Host ""
    }
} catch {
    Write-Host ""
}
'''
            
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
                return None
                
        except Exception as e:
            return None

    def listen_text(self):
        """Get text input from user"""
        user_input = input("📝 Type your message: ").strip()
        return user_input

    def listen(self):
        """Listen for input - try voice first, then text"""
        print("Attempting voice recognition...")
        user_input = self.listen_voice()
        
        if not user_input:
            print("💬 Text input mode\n")
            user_input = self.listen_text()
        
        return user_input

    def chat(self):
        """Main chat loop"""
        print(f"{'='*60}")
        print("💡 Commands: Ask any question or say 'goodbye' to exit")
        print(f"{'='*60}\n")
        
        # Welcome message
        greeting = "Hi there! I'm your AI assistant. I can answer almost any question. What would you like to know?"
        self.speak(greeting)
        
        while True:
            try:
                user_input = self.listen()
                
                if not user_input:
                    continue
                
                # Check for exit
                if re.search(r'\b(goodbye|bye|exit|quit|stop|end)\b', user_input.lower()):
                    farewell = "Goodbye! Thanks for chatting. Have an amazing day!"
                    self.speak(farewell)
                    break
                
                # Get and speak response
                print("🤔 Thinking...", end=" ", flush=True)
                response = self.get_ai_response(user_input)
                print("\r" + " "*20 + "\r", end="", flush=True)  # Clear thinking message
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n")
                self.speak("Goodbye! See you soon!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    chatbot = AdvancedAIChatbot()
    chatbot.chat()
    print("\n" + "="*60)
    print("ChatBot session ended. Thanks for using AI ChatBot!")
    print("="*60 + "\n")
