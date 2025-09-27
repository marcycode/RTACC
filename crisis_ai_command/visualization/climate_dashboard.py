import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from data_pipeline.climate_sources import ClimateDataCollector

class ClimateCrisisMap:
    def __init__(self):
        self.climate_collector = ClimateDataCollector()
        
    def create_enhanced_crisis_map(self, coordinates, latest_data, crisis_result):
        """Create crisis map with real-time climate overlays"""
        lat, lon = coordinates
        
        # Base crisis map
        fig = go.Figure()
        
        # Add base map
        fig.add_trace(go.Scattermapbox(
            lat=[lat], lon=[lon],
            mode='markers',
            marker=dict(size=20, color=self._get_crisis_color(crisis_result['risk_level'])),
            text=f"Crisis Level: {crisis_result['risk_level']}<br>Score: {crisis_result['crisis_score']:.3f}",
            name="Crisis Center"
        ))
        
        # Get climate overlay data
        weather_data = latest_data.get('weather', [{}])[-1] if latest_data.get('weather') else {}
        climate_overlays = self.climate_collector.get_climate_overlays(coordinates, weather_data)
        
        # Add flood zones if present
        if 'flood_zones' in climate_overlays:
            self._add_flood_overlay(fig, climate_overlays['flood_zones'])
        
        # Add wildfire zones if present  
        if 'wildfire_zones' in climate_overlays:
            self._add_wildfire_overlay(fig, climate_overlays['wildfire_zones'])
        
        # Add weather radar visualization
        self._add_weather_patterns(fig, coordinates, weather_data)
        
        # Configure map layout
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=lat, lon=lon),
                zoom=10
            ),
            showlegend=True,
            title="🌪️ Real-Time Climate Crisis Visualization",
            height=700
        )
        
        return fig
    
    def _add_flood_overlay(self, fig, flood_data):
        """Add flood risk heatmap overlay"""
        lat_range = flood_data['lat_range']
        lon_range = flood_data['lon_range'] 
        flood_risk = np.array(flood_data['flood_risk'])
        
        # Create flood risk contour
        fig.add_trace(go.Densitymapbox(
            lat=np.repeat(lat_range, len(lon_range)),
            lon=np.tile(lon_range, len(lat_range)),
            z=flood_risk.flatten(),
            colorscale=[[0, 'rgba(0,0,255,0)'], [0.5, 'rgba(0,100,255,0.3)'], [1, 'rgba(0,0,255,0.7)']],
            showscale=True,
            colorbar=dict(title="Flood Risk", x=0.02),
            name="Flood Zones",
            hovertemplate="Flood Risk: %{z:.2f}<extra></extra>"
        ))
    
    def _add_wildfire_overlay(self, fig, fire_data):
        """Add wildfire spread simulation"""
        lat_range = fire_data['lat_range']
        lon_range = fire_data['lon_range']
        fire_risk = np.array(fire_data['fire_risk'])
        
        # Create fire risk heatmap
        fig.add_trace(go.Densitymapbox(
            lat=np.repeat(lat_range, len(lon_range)),
            lon=np.tile(lon_range, len(lat_range)),
            z=fire_risk.flatten(),
            colorscale=[[0, 'rgba(255,165,0,0)'], [0.5, 'rgba(255,69,0,0.4)'], [1, 'rgba(139,0,0,0.8)']],
            showscale=True,
            colorbar=dict(title="Fire Risk", x=0.98),
            name="Wildfire Zones",
            hovertemplate="Fire Risk: %{z:.2f}<extra></extra>"
        ))
    
    def _add_weather_patterns(self, fig, coordinates, weather_data):
        """Add animated weather pattern visualization"""
        lat, lon = coordinates
        
        # Wind direction arrows
        if 'wind_direction' in weather_data and 'wind_speed' in weather_data:
            wind_dir = weather_data['wind_direction']
            wind_speed = weather_data['wind_speed']
            
            # Create wind arrows in grid pattern
            arrow_positions = []
            for i in range(-2, 3):
                for j in range(-2, 3):
                    arrow_lat = lat + i * 0.02
                    arrow_lon = lon + j * 0.02
                    arrow_positions.append((arrow_lat, arrow_lon))
            
            for arrow_lat, arrow_lon in arrow_positions:
                # Calculate arrow end point based on wind direction
                arrow_length = wind_speed * 0.001
                end_lat = arrow_lat + arrow_length * np.cos(np.radians(wind_dir))
                end_lon = arrow_lon + arrow_length * np.sin(np.radians(wind_dir))
                
                fig.add_trace(go.Scattermapbox(
                    lat=[arrow_lat, end_lat],
                    lon=[arrow_lon, end_lon],
                    mode='lines+markers',
                    line=dict(color='white', width=2),
                    marker=dict(size=[0, 10], symbol=['circle', 'triangle-up'], color='white'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        # Precipitation intensity circles
        if 'precipitation' in weather_data and weather_data['precipitation'] > 0:
            precip = weather_data['precipitation']
            fig.add_trace(go.Scattermapbox(
                lat=[lat], lon=[lon],
                mode='markers',
                marker=dict(
                    size=precip * 20,
                    color='rgba(0, 100, 255, 0.3)',
                    line=dict(color='blue', width=2)
                ),
                name=f"Precipitation: {precip}mm",
                hovertemplate=f"Precipitation: {precip}mm<extra></extra>"
            ))
    
    def _get_crisis_color(self, risk_level):
        """Get color for crisis level"""
        colors = {
            'LOW': 'green',
            'MEDIUM': 'yellow', 
            'HIGH': 'orange',
            'CRITICAL': 'red'
        }
        return colors.get(risk_level, 'gray')