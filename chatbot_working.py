#!/usr/bin/env python3
"""
Advanced Online AI ChatBot - Fixed Working Version
Uses reliable APIs that work without authentication
"""

import re
from datetime import datetime
import subprocess
import os
import requests
import json
import wikipedia
from urllib.parse import quote
import time

class WorkingAIChatbot:
    def __init__(self):
        self.name = "Online AI ChatBot"
        
        print("\n" + "="*60)
        print(f"🌐 {self.name} - Working Version")
        print("="*60)
        print("✓ Internet Search: Enabled")
        print("✓ Wikipedia: Active")
        print("✓ Weather API: Active")
        print("✓ Voice Input/Output: Enabled")
        print("="*60 + "\n")
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def search_wikipedia_detailed(self, query):
        """Search Wikipedia for detailed answers"""
        try:
            print("  📚 Searching Wikipedia...", end=" ", flush=True)
            
            search_results = wikipedia.search(query, results=1)
            
            if search_results:
                try:
                    page = wikipedia.page(search_results[0], auto_suggest=True)
                    summary = page.summary
                    
                    # Get first few sentences
                    sentences = summary.split('.')
                    answer = '. '.join(sentences[:5]) + '.'
                    
                    print("✓ Found!")
                    return answer
                except wikipedia.exceptions.DisambiguationError as e:
                    if e.options:
                        page = wikipedia.page(e.options[0], auto_suggest=True)
                        summary = page.summary
                        sentences = summary.split('.')
                        answer = '. '.join(sentences[:5]) + '.'
                        print("✓ Found!")
                        return answer
                except:
                    pass
            
            print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def search_knowledge_api(self, query):
        """Search using Knowledge API (free alternative)"""
        try:
            print("  🧠 Searching Knowledge API...", end=" ", flush=True)
            
            # Use Ask.com API alternative
            url = "https://www.ask.com/web"
            params = {
                'q': query,
                'o': 'json'
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=5)
            if response.status_code == 200:
                text = response.text
                # Try to extract answer
                import re as regex
                matches = regex.findall(r'<p[^>]*>([^<]{50,300})</p>', text)
                if matches:
                    for match in matches:
                        cleaned = match.strip()
                        if len(cleaned) > 30:
                            print("✓ Found!")
                            return cleaned
            
            print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def search_answers_com(self, query):
        """Search using Answers.com API"""
        try:
            print("  📖 Searching Answers.com...", end=" ", flush=True)
            
            url = "https://www.answers.com/search"
            params = {'q': query}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=5)
            if response.status_code == 200:
                import re as regex
                # Look for answer content
                matches = regex.findall(r'<div[^>]*class="[^"]*answer[^"]*"[^>]*>([^<]{50,300})</div>', response.text)
                if matches:
                    answer = matches[0].strip()
                    if len(answer) > 30:
                        print("✓ Found!")
                        return answer
            
            print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def search_wolframalpha(self, query):
        """Get computational answers from Wolfram Alpha"""
        try:
            print("  🔬 Searching Wolfram Alpha...", end=" ", flush=True)
            
            url = "http://www.wolframalpha.com/input/"
            params = {'i': query}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=5)
            if response.status_code == 200:
                import re as regex
                # Look for result pod
                matches = regex.findall(r'<div[^>]*class="pod"[^>]*>.*?<span[^>]*>([^<]{20,200})</span>', response.text, regex.DOTALL)
                if matches:
                    answer = matches[0].strip()
                    if len(answer) > 10:
                        print("✓ Found!")
                        return answer
            
            print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def search_weather(self, query):
        """Get weather information"""
        try:
            if any(word in query.lower() for word in ['weather', 'temperature', 'climate', 'rain', 'wind', 'forecast']):
                print("  🌤️  Checking Weather...", end=" ", flush=True)
                
                city = re.sub(r'(weather|temperature|in|climate|rain|wind|forecast|is it)', '', query.lower()).strip()
                if not city:
                    city = "London"
                
                # Get geocoding
                url = "https://geocoding-api.open-meteo.com/v1/search"
                params = {'name': city, 'count': 1, 'language': 'en'}
                
                response = requests.get(url, params=params, timeout=5)
                if response.status_code == 200:
                    geo_data = response.json()
                    if geo_data.get('results'):
                        loc = geo_data['results'][0]
                        lat, lon = loc['latitude'], loc['longitude']
                        city_name = loc.get('name', 'Unknown')
                        country = loc.get('country', '')
                        
                        # Get weather
                        weather_url = "https://api.open-meteo.com/v1/forecast"
                        weather_params = {
                            'latitude': lat,
                            'longitude': lon,
                            'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m'
                        }
                        
                        w_response = requests.get(weather_url, params=weather_params, timeout=5)
                        if w_response.status_code == 200:
                            w_data = w_response.json()
                            current = w_data['current']
                            
                            result = f"Weather in {city_name}, {country}: {current['temperature_2m']}°C, Humidity: {current['relative_humidity_2m']}%, Wind: {current['wind_speed_10m']} km/h"
                            print("✓ Found!")
                            return result
                
                print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def get_response(self, user_input):
        """Get comprehensive response"""
        try:
            print(f"\n📡 Searching for: '{user_input}'")
            print("  Checking multiple sources...")
            
            # Try different sources
            sources = [
                self.search_wikipedia_detailed,
                self.search_weather,
                self.search_knowledge_api,
                self.search_answers_com,
                self.search_wolframalpha,
            ]
            
            for source in sources:
                try:
                    answer = source(user_input)
                    if answer and len(answer.strip()) > 10:
                        # Clean answer
                        answer = answer.strip()
                        answer = re.sub(r'\[\d+\]', '', answer)
                        answer = ' '.join(answer.split())
                        
                        if len(answer) > 1500:
                            answer = answer[:1500] + "..."
                        
                        return answer
                except Exception as e:
                    continue
            
            return f"I couldn't find specific information about '{user_input}'. Try asking differently or be more specific."
        
        except Exception as e:
            return f"I encountered an issue searching: {str(e)}"

    def speak(self, text):
        """Convert text to speech"""
        display_text = text[:300] + "..." if len(text) > 300 else text
        print(f"\n🤖 ChatBot: {display_text}\n")
        
        try:
            speech_text = text[:800] if len(text) > 800 else text
            speech_text = speech_text.replace('"', '\"').replace('$', '`$').replace('\n', ' ')
            
            ps_command = f'''
Add-Type -AssemblyName System.Speech
$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synthesizer.Rate = 0
$synthesizer.Volume = 100
$synthesizer.Speak("{speech_text}")
'''
            subprocess.Popen(
                ['powershell', '-NoProfile', '-Command', ps_command],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            pass

    def listen_voice(self):
        """Listen for voice input"""
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
                print(f"✓ You: {text}")
                return text
            else:
                return None
                
        except Exception as e:
            return None

    def listen_text(self):
        """Get text input"""
        user_input = input("📝 Type your question: ").strip()
        return user_input

    def listen(self):
        """Listen for input"""
        print("Attempting voice recognition...")
        user_input = self.listen_voice()
        
        if not user_input:
            print("💬 Using text input mode")
            user_input = self.listen_text()
        
        return user_input

    def chat(self):
        """Main chat loop"""
        print(f"{'='*60}")
        print("🌐 Ask any question - I'll search for real answers!")
        print("💡 I search Wikipedia, Weather APIs, and Web sources")
        print("💡 Type 'goodbye' to exit or 'help' for options")
        print(f"{'='*60}\n")
        
        greeting = "Hello! I'm your AI assistant. I can search the internet and answer your questions. Ask me anything!"
        self.speak(greeting)
        
        while True:
            try:
                user_input = self.listen()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'help':
                    help_text = "Ask me about: weather, people, places, science, technology, history, and more!"
                    self.speak(help_text)
                    continue
                
                if re.search(r'\b(goodbye|bye|exit|quit|stop)\b', user_input.lower()):
                    self.speak("Goodbye! Have a great day!")
                    break
                
                response = self.get_response(user_input)
                self.speak(response)
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    try:
        requests.get('https://www.google.com', timeout=2)
        print("✓ Internet connection detected!")
    except:
        print("⚠️  No internet connection!")
    
    chatbot = WorkingAIChatbot()
    chatbot.chat()
    
    print("\n" + "="*60)
    print("ChatBot session ended. Thank you!")
    print("="*60 + "\n")
