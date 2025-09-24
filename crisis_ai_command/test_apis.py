import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("🧪 Testing API Keys")
print("=" * 30)

# Test Weather API
weather_key = "be29262f2cb2aec7e1fde65b2c815590"
print(f"Weather API Key: {weather_key[:10]}...{weather_key[-4:] if weather_key else 'None'}")

if weather_key:
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': 38.9072,
        'lon': -77.0369,
        'appid': weather_key,
        'units': 'metric'
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Weather API: {data['weather'][0]['description']}, {data['main']['temp']}°C")
    else:
        print(f"❌ Weather API Error: {response.status_code} - {response.text}")

# Test News API
news_key = os.getenv('NEWS_API_KEY')
print(f"News API Key: {news_key[:10]}...{news_key[-4:] if news_key else 'None'}")

if news_key:
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': 'emergency AND Washington',
        'pageSize': 1,
        'apiKey': news_key
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        if articles:
            print(f"✅ News API: Found {data['totalResults']} articles")
        else:
            print("✅ News API working, no articles found")
    else:
        print(f"❌ News API Error: {response.status_code} - {response.text}")

print("\nIf you see errors above, check your API keys!")