#!/usr/bin/env python3
"""
Advanced Online AI ChatBot - Google Powered
Uses Google Search, Wikipedia, and other premium sources
for real-time answers to any question
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

class AdvancedOnlineAIChatbot:
    def __init__(self):
        self.name = "Online AI ChatBot"
        
        print("\n" + "="*60)
        print(f"🌐 {self.name} - Google Powered")
        print("="*60)
        print("✓ Google Search: Enabled")
        print("✓ Wikipedia Integration: Active")
        print("✓ Real-time Answers: Available")
        print("✓ Voice Input/Output: Enabled")
        print("="*60 + "\n")
        
        # Headers for web requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def search_google(self, query):
        """Search using Bing (free alternative - works reliably)"""
        try:
            print("  🔍 Searching Web...", end=" ", flush=True)
            
            # Use Bing Search (completely free, no API key needed)
            url = "https://api.bing.microsoft.com/v7.0/search"
            headers = {
                'Ocp-Apim-Subscription-Key': 'demo'  # Will try without key first
            }
            params = {
                'q': query,
                'count': 3
            }
            
            try:
                response = requests.get(url, headers=headers, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('webPages') and data['webPages'].get('value'):
                        result = data['webPages']['value'][0]
                        snippet = result.get('snippet')
                        if snippet:
                            print("✓ Found!")
                            return snippet
            except:
                pass
            
            # Fallback: Use direct web search via requests
            search_url = f"https://www.google.com/search?q={quote(query)}"
            response = requests.get(search_url, headers=self.headers, timeout=5)
            if response.status_code == 200:
                # Extract answer from page
                import re as regex
                # Look for featured snippet
                matches = regex.findall(r'<span[^>]*>([^<]{50,300})</span>', response.text)
                if matches:
                    for match in matches:
                        cleaned = match.strip()
                        if len(cleaned) > 30 and not cleaned.startswith('<'):
                            print("✓ Found!")
                            return cleaned
            
            print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def search_web_instant(self, query):
        """Search the web using instant answers from various sources"""
        try:
            print("  🌐 Searching instant answers...", end=" ", flush=True)
            
            # Use Jina Reader for real-time web content
            url = f"https://r.jina.ai/https://www.google.com/search?q={quote(query)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200 and len(response.text) > 50:
                # Get first 500 chars of response
                text = response.text[:500].strip()
                if len(text) > 30:
                    print("✓ Found!")
                    return text
            
            print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def search_duckduckgo(self, query):
        """Search using DuckDuckGo (no auth needed)"""
        try:
            print("  🔍 Searching DuckDuckGo...", end=" ", flush=True)
            
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_redirect': 1
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                # Check for direct answer
                if data.get('AbstractText'):
                    print("✓ Found!")
                    return data.get('AbstractText')
                elif data.get('Answer'):
                    print("✓ Found!")
                    return data.get('Answer')
                
                # Check related topics
                if data.get('RelatedTopics'):
                    topics = data.get('RelatedTopics')
                    if topics and len(topics) > 0:
                        text = topics[0].get('Text', '')
                        if text:
                            print("✓ Found!")
                            return text
            
            print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def search_wikipedia(self, query):
        """Search Wikipedia for answers"""
        try:
            print("  📚 Searching Wikipedia...", end=" ", flush=True)
            
            # Search for the topic
            search_results = wikipedia.search(query, results=1)
            
            if search_results:
                try:
                    # Get the summary
                    summary = wikipedia.summary(search_results[0], sentences=5)
                    print("✓ Found!")
                    return summary
                except:
                    pass
            
            print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def search_jina(self, query):
        """Search using Jina Reader (real-time web search)"""
        try:
            print("  🌐 Searching web...", end=" ", flush=True)
            
            # Jina is a free service for web scraping
            url = f"https://r.jina.ai/{quote('https://www.google.com/search?q=' + quote(query))}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                # Parse response
                text = response.text[:500]
                if text and len(text) > 10:
                    print("✓ Found!")
                    return text
            
            print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def search_openweather(self, query):
        """Get weather information"""
        try:
            if any(word in query.lower() for word in ['weather', 'temperature', 'climate', 'rain', 'wind']):
                print("  🌤️  Checking weather API...", end=" ", flush=True)
                
                # Extract city name
                city = query.replace('weather', '').replace('temperature', '').replace('in', '').strip()
                if not city:
                    city = "London"
                
                # Use Open-Meteo API (free, no auth required)
                url = "https://geocoding-api.open-meteo.com/v1/search"
                params = {'name': city, 'count': 1, 'language': 'en'}
                
                response = requests.get(url, params=params, timeout=5)
                if response.status_code == 200:
                    geo_data = response.json()
                    if geo_data['results']:
                        loc = geo_data['results'][0]
                        lat, lon = loc['latitude'], loc['longitude']
                        
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
                            
                            result = f"Weather in {loc['name']}, {loc.get('country', '')}: {current['temperature_2m']}°C, Humidity: {current['relative_humidity_2m']}%, Wind: {current['wind_speed_10m']} km/h"
                            print("✓ Found!")
                            return result
                
                print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def get_online_answer(self, query):
        """Get answer from various online sources"""
        
        print(f"\n📡 Searching internet for: '{query}'")
        print("  Checking multiple sources...")
        
        # Try different sources in order - use working APIs
        sources = [
            self.search_web_instant,   # Real-time web search
            self.search_wikipedia,     # Wikipedia for detailed info
            self.search_openweather,   # Weather data
        ]
        
        for source in sources:
            try:
                answer = source(query)
                if answer and len(answer.strip()) > 10:
                    return answer
            except Exception as e:
                continue
        
        return None

    def get_response(self, user_input):
        """Get response for user input"""
        try:
            # Get answer from internet
            answer = self.get_online_answer(user_input)
            
            if answer:
                # Clean up the answer
                answer = answer.strip()
                # Remove wiki citations
                answer = re.sub(r'\[\d+\]', '', answer)
                # Remove excessive newlines
                answer = ' '.join(answer.split())
                
                if len(answer) > 1000:
                    answer = answer[:1000] + "..."
                
                return answer
            else:
                return f"I searched multiple sources but couldn't find specific information about '{user_input}'. Try rephrasing or ask something more specific."
        
        except Exception as e:
            return f"I encountered an issue searching the internet: {str(e)}"

    def speak(self, text):
        """Convert text to speech using Windows PowerShell"""
        # Limit text length for display
        display_text = text[:250] + "..." if len(text) > 250 else text
        print(f"\n🤖 ChatBot: {display_text}\n")
        
        try:
            # Limit speech to first 500 characters
            speech_text = text[:500] if len(text) > 500 else text
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
                print(f"✓ You: {text}")
                return text
            else:
                return None
                
        except Exception as e:
            return None

    def listen_text(self):
        """Get text input from user"""
        user_input = input("📝 Type your question: ").strip()
        return user_input

    def listen(self):
        """Listen for input - try voice first, then text"""
        print("Attempting voice recognition...")
        user_input = self.listen_voice()
        
        if not user_input:
            print("💬 Using text input mode")
            user_input = self.listen_text()
        
        return user_input

    def chat(self):
        """Main chat loop"""
        print(f"{'='*60}")
        print("🌐 Ask any question - I'll search the internet in real-time!")
        print("💡 Type 'goodbye' to exit or 'help' for options")
        print(f"{'='*60}\n")
        
        # Welcome message
        greeting = "Hello! I'm an online AI assistant connected to the internet. I can search and answer any question for you. What would you like to know?"
        self.speak(greeting)
        
        question_count = 0
        
        while True:
            try:
                user_input = self.listen()
                
                if not user_input:
                    continue
                
                # Check for help
                if user_input.lower() == 'help':
                    help_text = "You can ask me about: weather, facts, places, people, science, technology, current events, and more! Just ask naturally."
                    self.speak(help_text)
                    continue
                
                # Check for exit
                if re.search(r'\b(goodbye|bye|exit|quit|stop|end|close)\b', user_input.lower()):
                    farewell = "Goodbye! Thanks for chatting. Have a great day!"
                    self.speak(farewell)
                    break
                
                # Get answer from internet
                question_count += 1
                response = self.get_response(user_input)
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    # Check internet connection
    try:
        requests.get('https://www.google.com', timeout=2)
        print("✓ Internet connection detected!")
    except:
        print("⚠️  Warning: No internet connection detected!")
        print("This chatbot needs internet to work properly.\n")
    
    chatbot = AdvancedOnlineAIChatbot()
    chatbot.chat()
    
    print("\n" + "="*60)
    print("Online AI ChatBot session ended. Thank you for using!")
    print("="*60 + "\n")
