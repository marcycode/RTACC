import requests
import json
import time
import threading
from datetime import datetime
import numpy as np
import os
from dotenv import load_dotenv
import geocoder


load_dotenv()

class RealTimeDataCollector:
    def __init__(self, location="Washington, DC, USA"):
        self.weather_data = []
        self.traffic_data = []
        self.news_data = []
        self.social_data = []
        self.running = False
    
        self.current_location = location
        self.location_coords = self._get_coordinates(location)
        
        self.weather_api_key = os.getenv('OPENWEATHER_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.here_api_key = os.getenv('HERE_API_KEY')
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        
        self.reddit = None
        if self.reddit_client_id and self.reddit_client_secret:
            try:
                import praw
                self.reddit = praw.Reddit(
                    client_id=self.reddit_client_id,
                    client_secret=self.reddit_client_secret,
                    user_agent='CrisisAI:v1.0'
                )
                print(f"🤖 Reddit API: ✅ Connected")
            except Exception as e:
                print(f"🤖 Reddit API: ❌ Error - {e}")
        
        print(f"🌐 Global Crisis Data Collector initialized")
        print(f"📍 Location: {self.current_location}")
        print(f"🗺️ Coordinates: {self.location_coords}")
        print(f"   Weather API: {'✅ Ready' if self.weather_api_key else '❌ No API key'}")
        print(f"   News API: {'✅ Ready' if self.news_api_key else '❌ No API key'}")
        print(f"   HERE Traffic: {'✅ Ready' if self.here_api_key else '❌ No API key'}")
        print(f"   Reddit Social: {'✅ Ready' if self.reddit else '❌ No API key'}")
        
    def _get_coordinates(self, location):
        """Get coordinates for a location using geocoding"""
        try:
           
            g = geocoder.osm(location)
            if g.ok:
                return {"lat": g.lat, "lon": g.lng, "country": g.country, "state": g.state, "city": g.city}
            
            
            major_cities = {
                "washington dc": {"lat": 38.9072, "lon": -77.0369, "country": "USA", "state": "DC", "city": "Washington"},
                "new york": {"lat": 40.7128, "lon": -74.0060, "country": "USA", "state": "NY", "city": "New York"},
                "los angeles": {"lat": 34.0522, "lon": -118.2437, "country": "USA", "state": "CA", "city": "Los Angeles"},
                "london": {"lat": 51.5074, "lon": -0.1278, "country": "UK", "state": "England", "city": "London"},
                "tokyo": {"lat": 35.6762, "lon": 139.6503, "country": "Japan", "state": "Tokyo", "city": "Tokyo"},
                "paris": {"lat": 48.8566, "lon": 2.3522, "country": "France", "state": "Île-de-France", "city": "Paris"},
                "berlin": {"lat": 52.5200, "lon": 13.4050, "country": "Germany", "state": "Berlin", "city": "Berlin"},
                "sydney": {"lat": -33.8688, "lon": 151.2093, "country": "Australia", "state": "NSW", "city": "Sydney"},
                "toronto": {"lat": 43.6532, "lon": -79.3832, "country": "Canada", "state": "Ontario", "city": "Toronto"},
                "mumbai": {"lat": 19.0760, "lon": 72.8777, "country": "India", "state": "Maharashtra", "city": "Mumbai"}
            }
            
            location_key = location.lower().replace(",", "").replace(" usa", "").replace(" us", "").strip()
            for city_key, coords in major_cities.items():
                if city_key in location_key or location_key in city_key:
                    return coords
                    
            print(f"⚠️ Location '{location}' not found, defaulting to Washington DC")
            return major_cities["washington dc"]
            
        except Exception as e:
            print(f"⚠️ Geocoding error: {e}, defaulting to Washington DC")
            return {"lat": 38.9072, "lon": -77.0369, "country": "USA", "state": "DC", "city": "Washington"}
    
    def change_location(self, new_location):
        """Change the monitoring location and restart data collection"""
        print(f"🌍 Changing location from {self.current_location} to {new_location}")
        
    
        was_running = self.running
        self.running = False
        time.sleep(2)  
        
        # Clear old data
        self.weather_data.clear()
        self.traffic_data.clear()
        self.news_data.clear()
        self.social_data.clear()
        
        # Update location
        self.current_location = new_location
        self.location_coords = self._get_coordinates(new_location)
        
        print(f"📍 New location: {self.current_location}")
        print(f"🗺️ Coordinates: {self.location_coords}")
        
        # Restart collection if it was running
        if was_running:
            self.start_collection()
            
        return self.location_coords
    
    def get_location_info(self):
        """Get current location information"""
        return {
            "location": self.current_location,
            "coordinates": self.location_coords,
            "country": self.location_coords.get("country", "Unknown"),
            "city": self.location_coords.get("city", "Unknown")
        }
    
    def start_collection(self):
        """Start all data collection threads"""
        self.running = True
        threading.Thread(target=self._collect_real_weather, daemon=True).start()
        threading.Thread(target=self._collect_real_news, daemon=True).start()
        threading.Thread(target=self._collect_real_traffic, daemon=True).start()
        threading.Thread(target=self._collect_real_social, daemon=True).start()
        print(f"🌐 Real-time data collection started for {self.current_location}!")
        
    def _collect_real_weather(self):
        """Collect REAL weather data for current location"""
        while self.running:
            try:
                if self.weather_api_key:
                    url = f"http://api.openweathermap.org/data/2.5/weather"
                    params = {
                        'lat': self.location_coords["lat"],
                        'lon': self.location_coords["lon"],
                        'appid': self.weather_api_key,
                        'units': 'metric'
                    }
                    
                    response = requests.get(url, params=params, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        
                        wind_speed = data.get('wind', {}).get('speed', 0) * 3.6
                        temp = data['main']['temp']
                        humidity = data['main']['humidity']
                        pressure = data['main']['pressure']
                        
                        # Enhanced risk calculation based on location climate
                        risk_score = 0.0
                        
                        # Temperature risk (varies by location/season)
                        if self.location_coords.get("country") in ["Canada", "Russia", "Finland"]:
                            # Cold climate countries
                            if temp < -20 or temp > 30:
                                risk_score += 0.3
                        elif self.location_coords.get("country") in ["India", "UAE", "Saudi Arabia"]:
                            # Hot climate countries
                            if temp < 0 or temp > 45:
                                risk_score += 0.3
                        else:
                            # Temperate climates
                            if temp < -10 or temp > 40:
                                risk_score += 0.3
                        
                        # Wind risk
                        if wind_speed > 25:
                            risk_score += 0.3
                        
                        # Pressure risk
                        if pressure < 1000:
                            risk_score += 0.3
                            
                        # Humidity risk
                        if humidity > 90:
                            risk_score += 0.1
                            
                        weather_point = {
                            'timestamp': datetime.now(),
                            'location': f'{self.current_location}_REAL',
                            'temperature': temp,
                            'humidity': humidity,
                            'wind_speed': wind_speed,
                            'precipitation': data.get('rain', {}).get('1h', 0),
                            'pressure': pressure,
                            'weather_description': data['weather'][0]['description'],
                            'risk_score': min(1.0, risk_score),
                            'real_data': True
                        }
                        
                        self.weather_data.append(weather_point)
                        print(f"🌤️ Real weather ({self.location_coords['city']}): {temp}°C, {data['weather'][0]['description']}, Risk: {risk_score:.2f}")
                        
            except Exception as e:
                print(f"⚠️ Weather collection error: {e}")
                
            time.sleep(300)  # 5 minutes
            
    def _collect_real_news(self):
        """Collect REAL news for current location"""
        while self.running:
            try:
                if self.news_api_key:
                    # Location-specific news queries
                    location_terms = [
                        self.location_coords.get("city", ""),
                        self.location_coords.get("state", ""),
                        self.location_coords.get("country", "")
                    ]
                    location_query = " OR ".join([term for term in location_terms if term])
                    
                    crisis_keywords = ['emergency', 'disaster', 'flooding', 'fire', 'accident', 'evacuation', 'alert', 'storm']
                    
                    for keyword in crisis_keywords:
                        url = "https://newsapi.org/v2/everything"
                        params = {
                            'q': f'{keyword} AND ({location_query})',
                            'sortBy': 'publishedAt',
                            'language': 'en',
                            'pageSize': 5,
                            'apiKey': self.news_api_key
                        }
                        
                        response = requests.get(url, params=params, timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            
                            for article in data.get('articles', [])[:2]:
                                title = article.get('title', '').lower()
                                description = article.get('description', '').lower()
                                
                                severity = 0.0
                                high_severity_words = ['critical', 'emergency', 'disaster', 'evacuate', 'dangerous', 'severe']
                                medium_severity_words = ['alert', 'warning', 'incident', 'closed', 'delayed', 'storm']
                                
                                for word in high_severity_words:
                                    if word in title or word in description:
                                        severity += 0.3
                                        
                                for word in medium_severity_words:
                                    if word in title or word in description:
                                        severity += 0.1
                                        
                                severity = min(1.0, severity)
                                
                                news_point = {
                                    'timestamp': datetime.now(),
                                    'event_type': keyword,
                                    'severity': severity,
                                    'location': self.current_location,
                                    'description': article.get('title', ''),
                                    'source': article.get('source', {}).get('name', 'Unknown'),
                                    'url': article.get('url', ''),
                                    'real_data': True
                                }
                                
                                self.news_data.append(news_point)
                                print(f"📰 Real news ({self.location_coords['city']}): {keyword} - Severity: {severity:.2f}")
                                
                                time.sleep(1)
                        
                        time.sleep(2)
                        
            except Exception as e:
                print(f"⚠️ News collection error: {e}")
                
            time.sleep(600)  # 10 minutes
            
    def _collect_real_traffic(self):
        """Collect REAL traffic data for current location"""
        while self.running:
            try:
                if self.here_api_key:
                    # Create traffic monitoring zones around the location
                    base_lat = self.location_coords["lat"]
                    base_lon = self.location_coords["lon"]
                    
                    # Generate monitoring zones based on city size
                    zones = []
                    for i in range(5):
                        zones.append({
                            "name": f"{self.location_coords['city']}_Zone_{i+1}",
                            "lat": base_lat + np.random.normal(0, 0.05),
                            "lon": base_lon + np.random.normal(0, 0.05),
                            "radius": 2000 + i * 1000
                        })
                    
                    base_url = "https://data.traffic.hereapi.com/v7/flow"
                    
                    for zone in zones:
                        params = {
                            'apikey': self.here_api_key,
                            'in': f"circle:{zone['lat']},{zone['lon']};r={zone['radius']}",
                            'locationReferencing': 'shape'
                        }
                        
                        try:
                            response = requests.get(base_url, params=params, timeout=15)
                            if response.status_code == 200:
                                data = response.json()
                                results = data.get('results', [])
                                
                                if results:
                                    for result in results[:2]:
                                        location = result.get('location', {})
                                        current_flow = result.get('currentFlow', {})
                                        free_flow = result.get('freeFlow', {})
                                        
                                        current_speed = current_flow.get('speed', 50)
                                        free_flow_speed = free_flow.get('speed', 80)
                                        jam_factor = current_flow.get('jamFactor', 0)
                                        
                                        if free_flow_speed > 0:
                                            speed_ratio = current_speed / free_flow_speed
                                            congestion_level = max(0, min(1, 1 - speed_ratio))
                                        else:
                                            congestion_level = jam_factor / 10.0 if jam_factor else 0.3
                                        
                                        incident_detected = (
                                            jam_factor > 7 or 
                                            speed_ratio < 0.3 or 
                                            congestion_level > 0.8
                                        )
                                        
                                        traffic_point = {
                                            'timestamp': datetime.now(),
                                            'location': f"{zone['name']}_Real",
                                            'congestion_level': min(1.0, congestion_level),
                                            'incident_detected': incident_detected,
                                            'average_speed': current_speed,
                                            'free_flow_speed': free_flow_speed,
                                            'jam_factor': jam_factor,
                                            'speed_ratio': speed_ratio,
                                            'confidence': current_flow.get('confidence', 0.8),
                                            'real_data': True
                                        }
                                        
                                        self.traffic_data.append(traffic_point)
                                        print(f"🚗 Real traffic ({self.location_coords['city']}): {zone['name']} - Congestion: {congestion_level:.2f}")
                                        
                                else:
                                    self._add_single_traffic_simulation(zone['name'])
                                    
                            else:
                                self._add_single_traffic_simulation(zone['name'])
                                
                        except Exception as e:
                            print(f"⚠️ HERE API error for {zone['name']}: {e}")
                            self._add_single_traffic_simulation(zone['name'])
                            
                        time.sleep(3)
                        
                else:
                    self._add_enhanced_traffic_simulation()
                    
            except Exception as e:
                print(f"⚠️ Traffic collection error: {e}")
                self._add_enhanced_traffic_simulation()
                
            time.sleep(180)  # 3 minutes
            
    def _collect_real_social(self):
        """Collect location-specific social media data"""
        while self.running:
            try:
                if self.reddit:
                    # Find relevant subreddits for the location
                    location_subreddits = self._get_location_subreddits()
                    crisis_keywords = ['emergency', 'traffic', 'accident', 'flooding', 'fire', 'evacuation', 'alert', 'closure', 'storm']
                    
                    for subreddit_name in location_subreddits:
                        try:
                            subreddit = self.reddit.subreddit(subreddit_name)
                            
                            for submission in subreddit.new(limit=3):
                                title = submission.title.lower()
                                selftext = submission.selftext.lower() if submission.selftext else ""
                                
                                crisis_detected = any(keyword in title or keyword in selftext 
                                                    for keyword in crisis_keywords)
                                
                                positive_words = ['good', 'great', 'excellent', 'clear', 'normal', 'safe']
                                negative_words = ['bad', 'terrible', 'awful', 'emergency', 'crisis', 'accident', 'closed', 'delayed']
                                
                                sentiment = 0.0
                                text_combined = title + " " + selftext
                                
                                for word in positive_words:
                                    sentiment += text_combined.count(word) * 0.1
                                for word in negative_words:
                                    sentiment -= text_combined.count(word) * 0.15
                                
                                sentiment = np.clip(sentiment, -1, 1)
                                
                                social_point = {
                                    'timestamp': datetime.now(),
                                    'sentiment': sentiment,
                                    'mention_count': submission.score + submission.num_comments,
                                    'crisis_keywords': crisis_detected,
                                    'location': f"r/{subreddit_name}",
                                    'trending_topics': [word for word in crisis_keywords if word in text_combined] or ['normal'],
                                    'engagement': submission.score,
                                    'comments': submission.num_comments,
                                    'real_data': True
                                }
                                
                                self.social_data.append(social_point)
                                print(f"📱 Real social ({self.location_coords['city']}): r/{subreddit_name} - Sentiment: {sentiment:.2f}")
                                
                                time.sleep(2)
                                
                        except Exception as e:
                            print(f"⚠️ Subreddit {subreddit_name} error: {e}")
                            
                        time.sleep(10)
                        
                else:
                    self._add_enhanced_social_simulation()
                    
            except Exception as e:
                print(f"⚠️ Social collection error: {e}")
                self._add_enhanced_social_simulation()
                
            time.sleep(300)  # 5 minutes
            
    def _get_location_subreddits(self):
        """Get relevant subreddits for the current location"""
        city = self.location_coords.get("city", "").lower().replace(" ", "")
        state = self.location_coords.get("state", "").lower().replace(" ", "")
        country = self.location_coords.get("country", "").lower()
        
        # Common subreddit patterns
        subreddits = ['news', 'worldnews']
        
        # Add location-specific subreddits
        if city:
            subreddits.extend([city, f"{city}news"])
        if state and country == "usa":
            subreddits.extend([state])
        
        # Major city subreddits
        city_subreddits = {
            "washington": ["washingtondc", "dmv"],
            "new york": ["nyc", "newyorkcity"],
            "los angeles": ["losangeles", "la"],
            "london": ["london", "unitedkingdom"],
            "tokyo": ["tokyo", "japan"],
            "paris": ["paris", "france"],
            "berlin": ["berlin", "germany"],
            "sydney": ["sydney", "australia"],
            "toronto": ["toronto", "canada"],
            "mumbai": ["mumbai", "india"]
        }
        
        for city_key, city_subs in city_subreddits.items():
            if city_key in city:
                subreddits.extend(city_subs)
                break
        
        return list(set(subreddits))[:5]  # Limit to 5 subreddits
    
    def _add_single_traffic_simulation(self, location_name):
        """Add single simulated traffic point"""
        current_hour = datetime.now().hour
        
        if 7 <= current_hour <= 9 or 17 <= current_hour <= 19:
            base_congestion = 0.7
            incident_chance = 0.15
        elif 22 <= current_hour or current_hour <= 5:
            base_congestion = 0.1
            incident_chance = 0.05
        else:
            base_congestion = 0.4
            incident_chance = 0.08
            
        traffic_point = {
            'timestamp': datetime.now(),
            'location': f"{location_name}_Sim",
            'congestion_level': max(0, min(1, np.random.normal(base_congestion, 0.2))),
            'incident_detected': np.random.random() < incident_chance,
            'average_speed': max(5, np.random.normal(45 * (1 - base_congestion), 10)),
            'real_data': False
        }
        self.traffic_data.append(traffic_point)
        
    def _add_enhanced_traffic_simulation(self):
        """Enhanced traffic simulation as fallback"""
        current_hour = datetime.now().hour
        
        if 7 <= current_hour <= 9 or 17 <= current_hour <= 19:
            base_congestion = 0.7
            incident_chance = 0.15
        elif 22 <= current_hour or current_hour <= 5:
            base_congestion = 0.1
            incident_chance = 0.05
        else:
            base_congestion = 0.4
            incident_chance = 0.08
            
        city_name = self.location_coords.get("city", "City")
        routes = [f"{city_name}_Route_{i+1}" for i in range(5)]
        
        for route in routes:
            traffic_point = {
                'timestamp': datetime.now(),
                'location': f"{route}_Sim",
                'congestion_level': max(0, min(1, np.random.normal(base_congestion, 0.2))),
                'incident_detected': np.random.random() < incident_chance,
                'average_speed': max(5, np.random.normal(45 * (1 - base_congestion), 10)),
                'real_data': False
            }
            self.traffic_data.append(traffic_point)
            
    def _add_enhanced_social_simulation(self):
        """Enhanced social simulation as fallback"""
        base_sentiment = np.random.normal(-0.1, 0.3)
        recent_news = self.news_data[-5:] if self.news_data else []
        news_amplification = sum(item.get('severity', 0) for item in recent_news) * 0.1
        
        social_point = {
            'timestamp': datetime.now(),
            'sentiment': np.clip(base_sentiment - news_amplification, -1, 1),
            'mention_count': max(0, np.random.poisson(50 + news_amplification * 100)),
            'crisis_keywords': np.random.random() > (0.8 - news_amplification),
            'location': f"{self.location_coords.get('city', 'City')}_Zone_{np.random.randint(1, 20)}",
            'real_data': False
        }
        self.social_data.append(social_point)
        
    def get_latest_data(self):
        """Get the most recent data from all sources"""
        return {
            'weather': self.weather_data[-10:] if self.weather_data else [],
            'traffic': self.traffic_data[-15:] if self.traffic_data else [],
            'news': self.news_data[-10:] if self.news_data else [],
            'social': self.social_data[-20:] if self.social_data else []
        }
        
    def get_data_status(self):
        """Get status of real vs simulated data"""
        weather_real = any(item.get('real_data', False) for item in self.weather_data[-5:])
        news_real = any(item.get('real_data', False) for item in self.news_data[-5:])
        traffic_real = any(item.get('real_data', False) for item in self.traffic_data[-5:])
        social_real = any(item.get('real_data', False) for item in self.social_data[-5:])
        
        return {
            'weather_real': weather_real,
            'news_real': news_real,
            'traffic_real': traffic_real,
            'social_real': social_real
        }