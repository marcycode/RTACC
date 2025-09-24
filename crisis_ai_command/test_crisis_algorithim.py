import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_pipeline.data_sources import RealTimeDataCollector
from data_pipeline.processors import CUDADataProcessor
import time

def test_crisis_detection(location):
    print(f"\n🧪 Testing Crisis Detection for: {location}")
    print("=" * 50)
    
    collector = RealTimeDataCollector(location)
    processor = CUDADataProcessor()
    collector.start_collection()
    
    # Let some data collect
    print("⏳ Collecting data for 15 seconds...")
    time.sleep(15)
    
    latest_data = collector.get_latest_data()
    crisis_result = processor.process_crisis_detection(latest_data)
    
    print(f"\n📊 CRISIS ANALYSIS RESULTS:")
    print(f"   Weather Risk: {crisis_result['weather_risk']:.3f}")
    print(f"   Traffic Risk: {crisis_result['traffic_risk']:.3f}")
    print(f"   Social Risk: {crisis_result['social_risk']:.3f}")
    print(f"   News Risk: {crisis_result['news_risk']:.3f}")
    print(f"   Overall Crisis Score: {crisis_result['crisis_score']:.3f}")
    print(f"   Risk Level: {crisis_result['risk_level']}")
    
    # Show sample data that contributed to the score
    print(f"\n📝 SAMPLE DATA:")
    weather = latest_data.get('weather', [])
    if weather:
        w = weather[-1]
        print(f"   Weather: {w.get('weather_description', 'N/A')} - {w.get('temperature', 0):.1f}°C - Risk: {w.get('risk_score', 0):.3f}")
    
    traffic = latest_data.get('traffic', [])
    if traffic:
        print(f"   Traffic samples: {len(traffic)} points")
        for i, t in enumerate(traffic[-3:]):
            print(f"     Route {i+1}: Congestion {t.get('congestion_level', 0):.2f}, Incident: {t.get('incident_detected', False)}")
    
    news = latest_data.get('news', [])
    if news:
        print(f"   News samples: {len(news)} articles")
        for i, n in enumerate(news[-3:]):
            print(f"     Article {i+1}: {n.get('event_type', 'Unknown')} - Severity: {n.get('severity', 0):.3f}")
    
    # Should this be a critical alert?
    expected_level = "LOW" if crisis_result['crisis_score'] < 0.35 else "MEDIUM" if crisis_result['crisis_score'] < 0.55 else "HIGH" if crisis_result['crisis_score'] < 0.75 else "CRITICAL"
    
    print(f"\n✅ Expected Level: {expected_level}")
    print(f"🎯 Actual Level: {crisis_result['risk_level']}")
    print(f"{'✅ CORRECT' if expected_level == crisis_result['risk_level'] else '❌ NEEDS ADJUSTMENT'}")
    
    collector.running = False
    return crisis_result

if __name__ == "__main__":
    # Test multiple cities
    test_cities = [
        "Paris, France",
        "London, UK", 
        "Tokyo, Japan",
        "New York, NY, USA"
    ]
    
    for city in test_cities:
        test_crisis_detection(city)
        time.sleep(2)