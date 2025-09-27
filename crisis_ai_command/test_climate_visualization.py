import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_pipeline.data_sources import RealTimeDataCollector
from data_pipeline.processors import CUDADataProcessor
from data_pipeline.climate_sources import ClimateDataCollector
from visualization.climate_dashboard import ClimateCrisisMap
import time

def test_climate_visualization(location):
    print(f"\n🌪️ Testing Climate Visualization for: {location}")
    print("=" * 60)
    
    collector = RealTimeDataCollector(location)
    processor = CUDADataProcessor()
    climate_collector = ClimateDataCollector()
    climate_map = ClimateCrisisMap()
    
    collector.start_collection()
    
    print("⏳ Collecting climate data for 15 seconds...")
    time.sleep(15)
    
    latest_data = collector.get_latest_data()
    crisis_result = processor.process_crisis_detection(latest_data)
    coordinates = collector._get_coordinates()
    
    # Test climate overlay generation
    weather_data = latest_data.get('weather', [{}])[-1] if latest_data.get('weather') else {}
    climate_overlays = climate_collector.get_climate_overlays(coordinates, weather_data)
    
    print(f"\n🌦️ CLIMATE OVERLAY RESULTS:")
    print(f"   Radar Layers Available: {len(climate_overlays.get('radar_layers', {}))}")
    print(f"   Flood Zones: {'✅ Generated' if 'flood_zones' in climate_overlays else '❌ Not Applicable'}")
    print(f"   Wildfire Zones: {'✅ Generated' if 'wildfire_zones' in climate_overlays else '❌ Not Applicable'}")
    
    if 'flood_zones' in climate_overlays:
        flood_data = climate_overlays['flood_zones']
        print(f"   Max Flood Risk: {flood_data['max_risk']:.3f}")
    
    if 'wildfire_zones' in climate_overlays:
        fire_data = climate_overlays['wildfire_zones']
        print(f"   Fire Danger Index: {fire_data['fire_danger_index']:.3f}")
    
    print(f"\n📊 ENHANCED CRISIS ANALYSIS:")
    print(f"   Overall Crisis Score: {crisis_result['crisis_score']:.3f}")
    print(f"   Risk Level: {crisis_result['risk_level']}")
    print(f"   Weather Contribution: {crisis_result['weather_risk']:.3f}")
    
    # Weather details for visualization
    print(f"\n🌡️ WEATHER VISUALIZATION DATA:")
    print(f"   Temperature: {weather_data.get('temperature', 0):.1f}°C")
    print(f"   Precipitation: {weather_data.get('precipitation', 0):.1f}mm")
    print(f"   Wind Speed: {weather_data.get('wind_speed', 0):.1f} m/s")
    print(f"   Wind Direction: {weather_data.get('wind_direction', 0):.1f}°")
    print(f"   Humidity: {weather_data.get('humidity', 0):.1f}%")
    
    collector.running = False
    return climate_overlays, crisis_result

if __name__ == "__main__":
    # Test climate visualization for extreme weather locations
    test_cities = [
        "Miami, FL, USA",      # Hurricane risk
        "Los Angeles, CA, USA", # Wildfire risk  
        "Houston, TX, USA",    # Flood risk
        "Phoenix, AZ, USA"     # Extreme heat
    ]
    
    for city in test_cities:
        test_climate_visualization(city)
        time.sleep(2)