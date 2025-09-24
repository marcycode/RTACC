import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_pipeline.data_sources import RealTimeDataCollector
from data_pipeline.processors import CUDADataProcessor
import time

print("🌍 Testing REAL-TIME Crisis AI System")
print("=" * 60)

# Initialize components
collector = RealTimeDataCollector()
processor = CUDADataProcessor()

collector.start_collection()
print("⏳ Collecting REAL data for 60 seconds...")
time.sleep(60)  

# Get data status
status = collector.get_data_status()
print(f"\n📡 DATA SOURCE STATUS:")
print(f"   Real Weather: {'✅ LIVE' if status['weather_real'] else '❌ Simulated'}")
print(f"   Real News: {'✅ LIVE' if status['news_real'] else '❌ Simulated'}")
print(f"   Traffic: 🔄 Enhanced Simulation")
print(f"   Social: 🔄 Enhanced Simulation")

# Process the data
print(f"\n🧠 AI CRISIS ANALYSIS (GPU-Accelerated):")
latest_data = collector.get_latest_data()
crisis_result = processor.process_crisis_detection(latest_data)

print(f"\n🚨 REAL-TIME CRISIS ASSESSMENT:")
print(f"   Overall Crisis Score: {crisis_result['crisis_score']:.3f}")
print(f"   Risk Level: {crisis_result['risk_level']}")
print(f"   Weather Risk: {crisis_result['weather_risk']:.3f}")
print(f"   Traffic Risk: {crisis_result['traffic_risk']:.3f}")
print(f"   Social Media Risk: {crisis_result['social_risk']:.3f}")
print(f"   News Alert Risk: {crisis_result['news_risk']:.3f}")
print(f"   GPU Accelerated: {'✅' if crisis_result['gpu_accelerated'] else '❌'}")

# Advanced analysis
prediction = processor.predict_crisis_evolution(latest_data, crisis_result)
print(f"\n🔮 AI PREDICTION:")
print(f"   Trend: {prediction['prediction'].upper()}")
print(f"   Confidence: {prediction['confidence']:.1%}")

# Resource optimization
resources = processor.optimize_resources(crisis_result, {})
print(f"\n🚁 EMERGENCY RESPONSE COORDINATION:")
print(f"   Deployment Type: {resources['deployment']}")
print(f"   Urgency Level: {resources['urgency']}")
print(f"   Response Time: {resources['estimated_response_time']}")
print(f"   Priority: Level {resources['priority_level']}")
if 'resources_needed' in resources:
    print(f"   Resources: {', '.join(resources['resources_needed'])}")
if resources.get('evacuation_recommended'):
    print(f"   🚨 EVACUATION RECOMMENDED")

# Data summary
print(f"\n📊 REAL-TIME DATA SUMMARY:")
print(f"   Weather Points: {len(latest_data['weather'])}")
print(f"   Traffic Points: {len(latest_data['traffic'])}")
print(f"   News Articles: {len(latest_data['news'])}")
print(f"   Social Signals: {len(latest_data['social'])}")

print(f"\n🏆 SYSTEM STATUS: OPERATIONAL")
print(f"✅ Ready for NVIDIA GTC Contest Demo!")