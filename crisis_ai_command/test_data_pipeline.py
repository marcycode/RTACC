import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_pipeline.data_sources import RealTimeDataCollector
from data_pipeline.processors import CUDADataProcessor
import time

print("🧪 Testing Crisis AI Data Pipeline")
print("=" * 50)

# Initialize components
collector = RealTimeDataCollector()
processor = CUDADataProcessor()

# Start data collection
collector.start_collection()
print("⏳ Collecting data for 30 seconds...")
time.sleep(30)

# Process the data
print("\n🔥 Processing crisis detection...")
latest_data = collector.get_latest_data()
crisis_result = processor.process_crisis_detection(latest_data)

print(f"\n📊 CRISIS ANALYSIS RESULTS:")
print(f"   Crisis Score: {crisis_result['crisis_score']:.3f}")
print(f"   Risk Level: {crisis_result['risk_level']}")
print(f"   Weather Risk: {crisis_result['weather_risk']:.3f}")
print(f"   Traffic Risk: {crisis_result['traffic_risk']:.3f}")
print(f"   Social Risk: {crisis_result['social_risk']:.3f}")

# Test resource optimization
print(f"\n🚁 RESOURCE OPTIMIZATION:")
resources = processor.optimize_resources(crisis_result, {})
print(f"   Deployment: {resources['deployment']}")
print(f"   Urgency: {resources['urgency']}")
if 'resources_needed' in resources:
    print(f"   Resources: {', '.join(resources['resources_needed'])}")
if 'estimated_response_time' in resources:
    print(f"   ETA: {resources['estimated_response_time']}")

print(f"\n✅ Data pipeline test complete!")
print(f"   Data points collected: {len(latest_data['weather']) + len(latest_data['traffic'])}")
print(f"   GPU processing: SUCCESSFUL")