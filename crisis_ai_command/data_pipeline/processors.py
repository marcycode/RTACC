import torch
import numpy as np
from datetime import datetime, timedelta
import logging

class CUDADataProcessor:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_ready = False
        
        if torch.cuda.is_available():
            print(f"🚀 Processor initialized on: {self.device}")
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
            print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        else:
            print("🚀 Processor initialized on: CPU")
            
    def process_crisis_detection(self, data):
        """Enhanced crisis detection with more realistic thresholds"""
        try:
            # Calculate individual risk scores with improved logic
            weather_risk = self._calculate_weather_risk(data.get('weather', []))
            traffic_risk = self._calculate_traffic_risk(data.get('traffic', []))
            social_risk = self._calculate_social_risk(data.get('social', []))
            news_risk = self._calculate_news_risk(data.get('news', []))
            
            # Weighted overall crisis score (more conservative)
            weights = {
                'weather': 0.20,    # Reduced from 0.25
                'traffic': 0.25,    # Reduced from 0.30
                'social': 0.25,     # Reduced from 0.30
                'news': 0.30        # Increased from 0.15 (news is most reliable indicator)
            }
            
            crisis_score = (
                weather_risk * weights['weather'] +
                traffic_risk * weights['traffic'] +
                social_risk * weights['social'] +
                news_risk * weights['news']
            )
            
            # More realistic risk level thresholds
            if crisis_score >= 0.75:          # Raised from 0.7
                risk_level = 'CRITICAL'
            elif crisis_score >= 0.55:        # Raised from 0.5
                risk_level = 'HIGH'
            elif crisis_score >= 0.35:        # Raised from 0.3
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            return {
                'crisis_score': crisis_score,
                'risk_level': risk_level,
                'weather_risk': weather_risk,
                'traffic_risk': traffic_risk,
                'social_risk': social_risk,
                'news_risk': news_risk,
                'gpu_accelerated': torch.cuda.is_available(),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            print(f"⚠️ Crisis detection error: {e}")
            return self._default_crisis_result()
    
    def _calculate_weather_risk(self, weather_data):
        """Calculate weather risk with more realistic thresholds"""
        if not weather_data:
            return 0.1  # Baseline risk when no data
        
        latest_weather = weather_data[-1]
        risk_score = latest_weather.get('risk_score', 0)
        
        # More conservative weather risk calculation
        if risk_score > 0.8:
            return min(0.9, risk_score)  # Cap at 0.9 unless truly extreme
        elif risk_score > 0.6:
            return risk_score * 0.8      # Reduce by 20%
        elif risk_score > 0.3:
            return risk_score * 0.7      # Reduce by 30%
        else:
            return risk_score * 0.5      # Normal weather is low risk
    
    def _calculate_traffic_risk(self, traffic_data):
        """Calculate traffic risk with improved logic"""
        if not traffic_data:
            return 0.15  # Baseline traffic risk
        
        recent_traffic = traffic_data[-5:] if len(traffic_data) >= 5 else traffic_data
        
        # Calculate average congestion and incident rate
        congestion_levels = [t.get('congestion_level', 0) for t in recent_traffic]
        incidents = [t.get('incident_detected', False) for t in recent_traffic]
        
        avg_congestion = np.mean(congestion_levels) if congestion_levels else 0
        incident_rate = sum(incidents) / len(incidents) if incidents else 0
        
        # More realistic traffic risk scoring
        base_risk = avg_congestion * 0.6  # Normal congestion isn't a crisis
        incident_risk = incident_rate * 0.4  # Incidents add risk
        
        total_risk = base_risk + incident_risk
        
        # Traffic alone rarely causes critical situations
        return min(0.8, total_risk)  # Cap traffic risk at 0.8
    
    def _calculate_social_risk(self, social_data):
        """Calculate social media risk with more conservative approach"""
        if not social_data:
            return 0.1  # Baseline social risk
        
        recent_social = social_data[-10:] if len(social_data) >= 10 else social_data
        
        # Analyze sentiment and crisis keywords
        sentiments = [s.get('sentiment', 0) for s in recent_social]
        crisis_mentions = [s.get('crisis_keywords', False) for s in recent_social]
        
        avg_sentiment = np.mean(sentiments) if sentiments else 0
        crisis_rate = sum(crisis_mentions) / len(crisis_mentions) if crisis_mentions else 0
        
        # Social media risk calculation (more conservative)
        sentiment_risk = max(0, -avg_sentiment) * 0.3  # Negative sentiment contributes
        crisis_keyword_risk = crisis_rate * 0.4
        
        # Social media can be noisy, so we're more conservative
        total_risk = (sentiment_risk + crisis_keyword_risk) * 0.7  # Reduce overall impact
        
        return min(0.7, total_risk)  # Cap social risk at 0.7
    
    def _calculate_news_risk(self, news_data):
        """Calculate news risk - most reliable indicator"""
        if not news_data:
            return 0.05  # Very low baseline when no news
        
        recent_news = news_data[-10:] if len(news_data) >= 10 else news_data
        
        # News severity analysis
        severities = [n.get('severity', 0) for n in recent_news]
        
        if not severities:
            return 0.05
        
        # News risk calculation
        max_severity = max(severities)
        avg_severity = np.mean(severities)
        high_severity_count = sum(1 for s in severities if s > 0.5)
        
        # Weight recent high-severity news more heavily
        if max_severity > 0.7:
            base_risk = max_severity * 0.8
        elif max_severity > 0.4:
            base_risk = max_severity * 0.6
        else:
            base_risk = avg_severity * 0.4
        
        # Boost risk if multiple high-severity articles
        if high_severity_count > 2:
            base_risk = min(0.9, base_risk * 1.3)
        elif high_severity_count > 0:
            base_risk = min(0.8, base_risk * 1.1)
        
        return base_risk
    
    def predict_crisis_evolution(self, data, current_crisis):
        """Predict how the crisis might evolve"""
        try:
            current_score = current_crisis['crisis_score']
            
            # Analyze trends in the data
            trend_analysis = self._analyze_trends(data)
            
            # Simple prediction logic
            if trend_analysis['overall_trend'] > 0.1:
                prediction = 'escalating'
                confidence = min(0.9, 0.5 + abs(trend_analysis['overall_trend']))
            elif trend_analysis['overall_trend'] < -0.1:
                prediction = 'de-escalating'
                confidence = min(0.9, 0.5 + abs(trend_analysis['overall_trend']))
            else:
                prediction = 'stable'
                confidence = 0.6
            
            return {
                'prediction': prediction,
                'confidence': confidence,
                'trend_analysis': trend_analysis
            }
            
        except Exception as e:
            print(f"⚠️ Prediction error: {e}")
            return {
                'prediction': 'stable',
                'confidence': 0.5,
                'trend_analysis': {}
            }
    
    def _analyze_trends(self, data):
        """Analyze trends in the crisis data"""
        trends = {}
        
        # Weather trend
        weather_data = data.get('weather', [])
        if len(weather_data) >= 3:
            recent_risks = [w.get('risk_score', 0) for w in weather_data[-3:]]
            trends['weather_trend'] = recent_risks[-1] - recent_risks[0] if len(recent_risks) >= 2 else 0
        else:
            trends['weather_trend'] = 0
        
        # Traffic trend
        traffic_data = data.get('traffic', [])
        if len(traffic_data) >= 5:
            recent_congestion = [t.get('congestion_level', 0) for t in traffic_data[-5:]]
            trends['traffic_trend'] = np.mean(recent_congestion[-2:]) - np.mean(recent_congestion[:2]) if len(recent_congestion) >= 4 else 0
        else:
            trends['traffic_trend'] = 0
        
        # News trend
        news_data = data.get('news', [])
        if len(news_data) >= 3:
            recent_severity = [n.get('severity', 0) for n in news_data[-3:]]
            trends['news_trend'] = np.mean(recent_severity[-2:]) - np.mean(recent_severity[:1]) if len(recent_severity) >= 3 else 0
        else:
            trends['news_trend'] = 0
        
        # Overall trend (weighted average)
        trends['overall_trend'] = (
            trends['weather_trend'] * 0.2 +
            trends['traffic_trend'] * 0.3 +
            trends['news_trend'] * 0.5
        )
        
        return trends
    
    def optimize_resources(self, crisis_result, available_resources):
        """Optimize emergency resource allocation"""
        crisis_score = crisis_result['crisis_score']
        risk_level = crisis_result['risk_level']
        
        # More realistic resource allocation
        if risk_level == 'CRITICAL':
            deployment = 'full_emergency_response'
            urgency = 'immediate'
            response_time = '5-10 minutes'
            priority_level = 'Level 1'
            resources_needed = ['ambulance', 'fire_department', 'police', 'emergency_management', 'media_coordination']
            evacuation_recommended = True
        elif risk_level == 'HIGH':
            deployment = 'enhanced_monitoring'
            urgency = 'high'
            response_time = '10-20 minutes'
            priority_level = 'Level 2'
            resources_needed = ['police', 'emergency_management', 'standby_medical']
            evacuation_recommended = False
        elif risk_level == 'MEDIUM':
            deployment = 'increased_readiness'
            urgency = 'medium'
            response_time = '20-30 minutes'
            priority_level = 'Level 3'
            resources_needed = ['patrol', 'monitoring']
            evacuation_recommended = False
        else:  # LOW
            deployment = 'standard_monitoring'
            urgency = 'low'
            response_time = '30+ minutes'
            priority_level = 'Level 4'
            resources_needed = ['routine_patrol']
            evacuation_recommended = False
        
        return {
            'deployment': deployment,
            'urgency': urgency,
            'estimated_response_time': response_time,
            'priority_level': priority_level,
            'resources_needed': resources_needed,
            'evacuation_recommended': evacuation_recommended,
            'crisis_score': crisis_score,
            'optimization_timestamp': datetime.now()
        }
    
    def _default_crisis_result(self):
        """Return default crisis result when processing fails"""
        return {
            'crisis_score': 0.2,
            'risk_level': 'LOW',
            'weather_risk': 0.1,
            'traffic_risk': 0.2,
            'social_risk': 0.2,
            'news_risk': 0.1,
            'gpu_accelerated': torch.cuda.is_available(),
            'timestamp': datetime.now()
        }