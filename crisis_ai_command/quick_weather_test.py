import requests

# Test with a sample API call (you need your own key)
api_key = "be29262f2cb2aec7e1fde65b2c815590"  # Replace with your actual key
url = f"http://api.openweathermap.org/data/2.5/weather"

params = {
    'q': 'Washington,DC,US',
    'appid': api_key,
    'units': 'metric'
}

response = requests.get(url, params=params)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✅ Weather in DC: {data['weather'][0]['description']}")
    print(f"   Temperature: {data['main']['temp']}°C")
    print(f"   Wind: {data['wind']['speed']} m/s")
else:
    print(f"❌ Error: {response.text}")