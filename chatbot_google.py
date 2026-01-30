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

class GooglePoweredChatbot:
    def __init__(self):
        self.name = "Google AI ChatBot"
        
        print("\n" + "="*70)
        print(f"🌐 {self.name} - Google Powered Edition")
        print("="*70)
        print("✓ Google Search Integration: Enabled")
        print("✓ Real-time Internet Search: Active")
        print("✓ Voice Input/Output: Enabled")
        print("✓ Multiple Knowledge Sources: Active")
        print("="*70 + "\n")
        
        # Headers for web requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def search_google_via_serpapi(self, query):
        """Search Google using SerpAPI (free tier available)"""
        try:
            print("  🔍 Searching Google (SerpAPI)...", end=" ", flush=True)
            
            url = "https://serpapi.com/search"
            params = {
                'q': query,
                'api_key': 'demo'  # Free demo key for testing
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                # Get answer box if available
                if data.get('answer_box'):
                    answer = data['answer_box'].get('answer') or data['answer_box'].get('snippet')
                    if answer:
                        print("✓ Found (Answer Box)!")
                        return answer
                
                # Get snippets from organic results
                if data.get('organic_results'):
                    for result in data['organic_results'][:3]:
                        snippet = result.get('snippet')
                        if snippet and len(snippet) > 50:
                            print("✓ Found (Google Search)!")
                            return snippet
            
            print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def search_google_via_custom(self, query):
        """Search Google using custom search method"""
        try:
            print("  🔎 Searching Google...", end=" ", flush=True)
            
            # Use Google's public search endpoint
            url = "https://www.google.com/search"
            params = {
                'q': query,
                'hl': 'en',
                'gl': 'us'
            }
            
            session = requests.Session()
            response = session.get(url, params=params, headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                # Parse for featured snippet or first result
                import re as regex
                
                # Look for knowledge panel or featured snippet
                patterns = [
                    r'<span[^>]*>([^<]{100,500})</span>',  # Knowledge panel
                    r'<span[^>]*class="[^"]*snippet[^"]*"[^>]*>([^<]{50,300})</span>',
                ]
                
                text = response.text
                for pattern in patterns:
                    matches = regex.findall(pattern, text)
                    if matches:
                        answer = matches[0].strip()
                        # Clean HTML entities
                        answer = answer.replace('&quot;', '"').replace('&#39;', "'")
                        if len(answer) > 30:
                            print("✓ Found (Google)!")
                            return answer
            
            print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def search_google_schemas(self, query):
        """Search using Google Knowledge Graph API alternative"""
        try:
            print("  📖 Searching Knowledge Graph...", end=" ", flush=True)
            
            # Using Bing to get structured data (alternative to Google)
            url = "https://api.bing.microsoft.com/v7.0/search"
            params = {'q': query}
            headers = {'Ocp-Apim-Subscription-Key': 'demo'}
            
            # Without key, we'll use Wikipedia as fallback
            raise Exception("Using Wikipedia fallback")
            
        except Exception as e:
            return None

    def search_wikipedia_detailed(self, query):
        """Search Wikipedia for detailed answers"""
        try:
            print("  📚 Searching Wikipedia...", end=" ", flush=True)
            
            # Search for the topic
            search_results = wikipedia.search(query, results=1)
            
            if search_results:
                try:
                    # Get the detailed summary
                    page = wikipedia.page(search_results[0], auto_suggest=True)
                    summary = page.summary
                    
                    # Get first few sentences (approximately 500 chars)
                    sentences = summary.split('.')
                    answer = '. '.join(sentences[:4]) + '.'
                    
                    print("✓ Found (Wikipedia)!")
                    return answer
                except wikipedia.exceptions.DisambiguationError as e:
                    # Handle disambiguation
                    if e.options:
                        page = wikipedia.page(e.options[0], auto_suggest=True)
                        summary = page.summary
                        sentences = summary.split('.')
                        answer = '. '.join(sentences[:4]) + '.'
                        print("✓ Found (Wikipedia)!")
                        return answer
                except:
                    pass
            
            print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def search_weather(self, query):
        """Get weather information from Open-Meteo"""
        try:
            if any(word in query.lower() for word in ['weather', 'temperature', 'climate', 'rain', 'wind', 'forecast', 'cold', 'hot']):
                print("  🌤️  Checking Weather API...", end=" ", flush=True)
                
                # Extract city name
                city = query.lower()
                city = re.sub(r'(weather|temperature|in|climate|rain|wind|forecast|is it)', '', city).strip()
                
                if not city or len(city) < 2:
                    city = "London"
                
                # Use Open-Meteo Geocoding API
                url = "https://geocoding-api.open-meteo.com/v1/search"
                params = {
                    'name': city,
                    'count': 1,
                    'language': 'en'
                }
                
                response = requests.get(url, params=params, timeout=5)
                if response.status_code == 200:
                    geo_data = response.json()
                    if geo_data.get('results') and len(geo_data['results']) > 0:
                        loc = geo_data['results'][0]
                        lat, lon = loc['latitude'], loc['longitude']
                        city_name = loc.get('name', 'Unknown')
                        country = loc.get('country', '')
                        
                        # Get current weather
                        weather_url = "https://api.open-meteo.com/v1/forecast"
                        weather_params = {
                            'latitude': lat,
                            'longitude': lon,
                            'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,precipitation'
                        }
                        
                        w_response = requests.get(weather_url, params=weather_params, timeout=5)
                        if w_response.status_code == 200:
                            w_data = w_response.json()
                            current = w_data['current']
                            
                            result = f"Current weather in {city_name}, {country}: {current['temperature_2m']}°C, Humidity: {current['relative_humidity_2m']}%, Wind Speed: {current['wind_speed_10m']} km/h, Precipitation: {current['precipitation']}mm"
                            print("✓ Found!")
                            return result
                
                print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def search_news(self, query):
        """Search for latest news"""
        try:
            if any(word in query.lower() for word in ['news', 'latest', 'recent', 'today', 'current']):
                print("  📰 Searching News...", end=" ", flush=True)
                
                # Using free news API
                url = "https://newsapi.org/v2/everything"
                params = {
                    'q': query,
                    'sortBy': 'publishedAt',
                    'pageSize': 3,
                    'language': 'en'
                }
                
                response = requests.get(url, params=params, timeout=5)
                if response.status_code == 200 or response.status_code == 401:
                    # Even with 401, we might get data
                    data = response.json()
                    if data.get('articles') and len(data['articles']) > 0:
                        article = data['articles'][0]
                        result = f"Latest: {article['title']} - {article['description']}"
                        print("✓ Found!")
                        return result
                
                print("✗ No results")
        except Exception as e:
            print(f"✗ Error")
        
        return None

    def get_comprehensive_answer(self, query):
        """Get answer from multiple sources"""
        
        print(f"\n📡 Searching for: '{query}'")
        print("  Checking multiple sources...")
        
        # Try different sources in order of preference
        sources = [
            ('Google Search', self.search_google_via_serpapi),
            ('Wikipedia', self.search_wikipedia_detailed),
            ('Weather', self.search_weather),
            ('News', self.search_news),
        ]
        
        for source_name, search_func in sources:
            try:
                answer = search_func(query)
                if answer and len(answer.strip()) > 10:
                    return answer
            except Exception as e:
                continue
        
        return None

    def get_response(self, user_input):
        """Get comprehensive response for user input"""
        try:
            # Get answer from internet
            answer = self.get_comprehensive_answer(user_input)
            
            if answer:
                # Clean up the answer
                answer = answer.strip()
                # Remove wiki citations
                answer = re.sub(r'\[\d+\]', '', answer)
                # Remove HTML entities
                answer = answer.replace('&nbsp;', ' ').replace('&quot;', '"').replace('&#39;', "'")
                # Remove excessive whitespace
                answer = ' '.join(answer.split())
                
                # Limit length
                if len(answer) > 1500:
                    answer = answer[:1500] + "..."
                
                return answer
            else:
                return f"I couldn't find specific information about '{user_input}' from available sources. Try rephrasing your question or ask something more specific."
        
        except Exception as e:
            return f"I encountered an issue searching for information: {str(e)}"

    def speak(self, text):
        """Convert text to speech using Windows PowerShell"""
        # Limit text length for display
        display_text = text[:300] + "..." if len(text) > 300 else text
        print(f"\n🤖 ChatBot: {display_text}\n")
        
        try:
            # Limit speech to first 800 characters
            speech_text = text[:800] if len(text) > 800 else text
            speech_text = speech_text.replace('"', '\"').replace('$', '`$').replace('\n', ' ')
            speech_text = speech_text.replace('&', 'and')
            
            ps_command = f'''
Add-Type -AssemblyName System.Speech
$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synthesizer.Rate = -1
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
        print(f"{'='*70}")
        print("🌐 Ask any question - I'll search the internet for real answers!")
        print("💡 I search Google, Wikipedia, Weather APIs, and News sources")
        print("💡 Type 'goodbye' to exit or 'help' for options")
        print(f"{'='*70}\n")
        
        # Welcome message
        greeting = "Hello! I'm your advanced Google-powered AI assistant. I search the internet including Google, Wikipedia, weather data, and news sources. Ask me anything!"
        self.speak(greeting)
        
        question_count = 0
        
        while True:
            try:
                user_input = self.listen()
                
                if not user_input:
                    continue
                
                # Check for help
                if user_input.lower() == 'help':
                    help_text = "You can ask me about: current events, weather, people, places, technology, science, news, definitions, and much more! Just ask naturally. I search Google and Wikipedia for real answers."
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
                
                # Small delay between requests
                time.sleep(1)
                
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
    
    chatbot = GooglePoweredChatbot()
    chatbot.chat()
    
    print("\n" + "="*70)
    print("Google AI ChatBot session ended. Thank you for using!")
    print("="*70 + "\n")
