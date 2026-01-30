import re
from datetime import datetime
import subprocess
import os
import time
from transformers import pipeline
import wikipedia
import random

class AdvancedChatbot:
    def __init__(self):
        self.name = "AI ChatBot"
        print("\n🤖 Initializing AI ChatBot...")
        print("Loading AI models (this may take a moment)...\n")
        
        try:
            # Load question-answering model
            self.qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
            print("✓ Question-Answering Model Loaded")
        except Exception as e:
            print(f"⚠️  Q&A Model Error: {e}")
            self.qa_pipeline = None
        
        try:
            # Load text generation model for conversations
            self.chat_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")
            print("✓ Conversation Model Loaded")
        except Exception as e:
            print(f"⚠️  Chat Model Error: {e}")
            self.chat_pipeline = None
        
        print("\n" + "="*50)
        
        # Fallback responses
        self.default_responses = [
            "That's an interesting question! Let me think about that.",
            "I'm not sure about that. Can you provide more details?",
            "That's a great question! Here's what I know:",
            "Let me help you with that.",
        ]

    def get_ai_response(self, user_input):
        """Get response using AI models"""
        
        # Try question-answering first
        if self.qa_pipeline:
            try:
                # Search Wikipedia for context
                try:
                    search_results = wikipedia.search(user_input, results=1)
                    if search_results:
                        context = wikipedia.summary(search_results[0], sentences=5)
                    else:
                        context = user_input
                except:
                    context = user_input
                
                # Use QA model
                result = self.qa_pipeline(question=user_input, context=context)
                if result and result.get('answer'):
                    confidence = result.get('score', 0)
                    if confidence > 0.1:
                        return result['answer']
            except Exception as e:
                pass
        
        # Fallback to text generation
        if self.chat_pipeline:
            try:
                response = self.chat_pipeline(user_input, max_length=150, num_beams=4, early_stopping=True)
                if response and len(response) > 0:
                    return response[0]['generated_text']
            except Exception as e:
                pass
        
        # Final fallback
        return random.choice(self.default_responses)

    def speak(self, text):
        """Convert text to speech using Windows PowerShell"""
        print(f"🤖 ChatBot: {text}\n")
        
        try:
            text_escaped = text.replace('"', '\"').replace('$', '`$')
            ps_command = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text_escaped}")'
            subprocess.run(
                ['powershell', '-NoProfile', '-Command', ps_command],
                capture_output=True, 
                timeout=30
            )
        except Exception as e:
            print(f"⚠️  Voice output error: {e}\n")

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
            print(f"❌ Voice recognition error: {e}\n")
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
        print("I can answer any question you ask!")
        print("Say or type 'goodbye' to exit.")
        print(f"{'='*50}\n")
        
        greeting = f"Welcome to {self.name}! I'm powered by advanced AI and can answer any question. What would you like to know?"
        self.speak(greeting)
        
        while True:
            try:
                user_input = self.listen()
                
                if not user_input:
                    continue
                
                if re.search(r'\b(goodbye|bye|exit|quit)\b', user_input.lower()):
                    response = "Goodbye! Thanks for chatting with me!"
                    self.speak(response)
                    break
                
                print("🔄 Thinking...")
                response = self.get_ai_response(user_input)
                self.speak(response)
                
            except KeyboardInterrupt:
                self.speak("Goodbye! Thanks for chatting!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                self.speak("An error occurred. Please try again.")

if __name__ == "__main__":
    chatbot = AdvancedChatbot()
    chatbot.chat()
