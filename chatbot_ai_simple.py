import re
from datetime import datetime
import subprocess
import os
import requests
import json

class AIEnabledChatbot:
    def __init__(self):
        self.name = "AI ChatBot"
        print("\n🤖 AI ChatBot Started")
        print("="*50)
        print("Features: Voice Input + AI Responses + Voice Output")
        print("="*50 + "\n")

    def get_ai_response_groq(self, user_input):
        """Get response from Groq API (Free, Fast AI)"""
        try:
            # You need to set your API key
            api_key = "YOUR_GROQ_API_KEY"  # Free API from https://console.groq.com
            
            if api_key == "YOUR_GROQ_API_KEY":
                return self.get_simple_ai_response(user_input)
            
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "system", "content": "You are a helpful AI assistant. Answer questions clearly and concisely."},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"⚠️  API Error: {e}")
        
        return self.get_simple_ai_response(user_input)

    def get_simple_ai_response(self, user_input):
        """Simple AI response without API"""
        user_lower = user_input.lower()
        
        # Knowledge base
        responses = {
            'hello|hi|hey': "Hello! I'm an AI chatbot. How can I help you today?",
            'how are you|how do you do': "I'm functioning well! Thanks for asking. How can I assist you?",
            'what is your name|who are you': "I'm an AI-powered chatbot designed to answer your questions.",
            'what time is it': f"The current time is {datetime.now().strftime('%I:%M %p')}.",
            'what is the date|what\' the date': f"Today is {datetime.now().strftime('%A, %B %d, %Y')}.",
            'what can you do|capabilities': "I can answer questions, provide information, tell time/date, and have conversations!",
            'thank you|thanks': "You're welcome! Happy to help.",
            'goodbye|bye|exit': "Goodbye! Have a great day!",
            'what is python': "Python is a versatile programming language used for web development, data science, AI, and more.",
            'what is ai|artificial intelligence': "AI is the simulation of human intelligence processes by computer systems. It learns from data and makes decisions.",
            'tell me a joke': "Why don't scientists trust atoms? Because they make up everything!",
            'what is machine learning': "Machine learning is a type of AI where systems learn from data without being explicitly programmed.",
            'how does the internet work': "The internet uses a network of connected computers that communicate using protocols like HTTP and TCP/IP.",
        }
        
        # Check for matching patterns
        for pattern, response in responses.items():
            if re.search(pattern, user_lower):
                return response
        
        # Default response for unknown questions
        return f"That's an interesting question about '{user_input}'. I'm learning more about this topic every day. Can you provide more details?"

    def speak(self, text):
        """Convert text to speech using Windows PowerShell"""
        print(f"🤖 ChatBot: {text}\n")
        
        try:
            text_escaped = text.replace('"', '\"').replace('$', '`$').replace('\n', ' ')
            ps_command = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text_escaped}")'
            subprocess.run(
                ['powershell', '-NoProfile', '-Command', ps_command],
                capture_output=True, 
                timeout=30
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
    
    if ($result -and $result.Text) {
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
                print("❌ No speech detected.\n")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}\n")
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
            print("💬 Switching to text input...\n")
            user_input = self.listen_text()
        
        return user_input

    def chat(self):
        """Start chatbot conversation"""
        print(f"\n{'='*50}")
        print(f"Welcome to {self.name}!")
        print("Speak or type any question!")
        print("Say 'goodbye' to exit")
        print(f"{'='*50}\n")
        
        greeting = "Welcome! I'm an AI chatbot. You can ask me anything!"
        self.speak(greeting)
        
        while True:
            try:
                user_input = self.listen()
                
                if not user_input:
                    continue
                
                if re.search(r'\b(goodbye|bye|exit|quit)\b', user_input.lower()):
                    self.speak("Goodbye! Have a great day!")
                    break
                
                print("🔄 Thinking...")
                response = self.get_simple_ai_response(user_input)
                self.speak(response)
                
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    chatbot = AIEnabledChatbot()
    chatbot.chat()
