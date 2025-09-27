import requests
import numpy as np
from datetime import datetime, timedelta
import torch

class ClimateDataCollector:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    def get_weather_radar_data(self, coordinates, zoom=5):
        """Get precipitation radar overlays from OpenWeatherMap"""
        lat, lon = coordinates
        base_url = "http://maps.openweathermap.org/maps/2.0/weather"
        
        # Get multiple radar layers
        layers = {
            'precipitation': f"{base_url}/PR0/{zoom}/{int(lat)}/{int(lon)}.png",
            'temperature': f"{base_url}/TA2/{zoom}/{int(lat)}/{int(lon)}.png", 
            'wind': f"{base_url}/WND/{zoom}/{int(lat)}/{int(lon)}.png",
            'pressure': f"{base_url}/APM/{zoom}/{int(lat)}/{int(lon)}.png"
        }
        return layers
    
    def simulate_flood_zones(self, coordinates, precipitation_data):
        """Simulate potential flood zones based on elevation and precipitation"""
        lat, lon = coordinates
        
        # Create flood risk heatmap data
        grid_size = 50
        lat_range = np.linspace(lat - 0.1, lat + 0.1, grid_size)
        lon_range = np.linspace(lon - 0.1, lon + 0.1, grid_size)
        
        # Simulate elevation-based flood risk
        flood_risk = np.zeros((grid_size, grid_size))
        for i, lat_val in enumerate(lat_range):
            for j, lon_val in enumerate(lon_range):
                # Simulate risk based on distance from center and precipitation
                distance_factor = np.sqrt((lat_val - lat)**2 + (lon_val - lon)**2)
                precip_factor = precipitation_data.get('intensity', 0) / 10.0
                flood_risk[i, j] = max(0, precip_factor - distance_factor * 100)
        
        return {
            'lat_range': lat_range.tolist(),
            'lon_range': lon_range.tolist(), 
            'flood_risk': flood_risk.tolist(),
            'max_risk': float(np.max(flood_risk))
        }
    
    def simulate_wildfire_spread(self, coordinates, weather_data):
        """Simulate wildfire spread based on wind and temperature"""
        lat, lon = coordinates
        temp = weather_data.get('temperature', 20)
        wind_speed = weather_data.get('wind_speed', 0)
        humidity = weather_data.get('humidity', 50)
        
        # Fire danger index calculation
        fire_danger = ((temp - 10) * wind_speed) / (humidity + 1)
        
        if fire_danger > 5:  # High fire danger threshold
            # Simulate fire spread zones
            grid_size = 30
            lat_range = np.linspace(lat - 0.05, lat + 0.05, grid_size)
            lon_range = np.linspace(lon - 0.05, lon + 0.05, grid_size)
            
            fire_risk = np.zeros((grid_size, grid_size))
            center_i, center_j = grid_size // 2, grid_size // 2
            
            for i in range(grid_size):
                for j in range(grid_size):
                    distance = np.sqrt((i - center_i)**2 + (j - center_j)**2)
                    fire_risk[i, j] = max(0, fire_danger - distance * 0.5)
            
            return {
                'lat_range': lat_range.tolist(),
                'lon_range': lon_range.tolist(),
                'fire_risk': fire_risk.tolist(),
                'fire_danger_index': float(fire_danger)
            }
        
        return None
    
    def get_climate_overlays(self, coordinates, weather_data):
        """Generate all climate visualization overlays"""
        overlays = {
            'radar_layers': self.get_weather_radar_data(coordinates),
            'timestamp': datetime.now().isoformat()
        }
        
        # Add flood simulation if precipitation detected
        if weather_data.get('precipitation', 0) > 1.0:
            overlays['flood_zones'] = self.simulate_flood_zones(coordinates, weather_data)
        
        # Add wildfire simulation if conditions are dry and hot
        wildfire_data = self.simulate_wildfire_spread(coordinates, weather_data)
        if wildfire_data:
            overlays['wildfire_zones'] = wildfire_data
        
        return overlays