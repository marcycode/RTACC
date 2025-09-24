import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_pipeline.data_sources import RealTimeDataCollector
from data_pipeline.processors import CUDADataProcessor

class DynamicCrisisDashboard:
    def __init__(self):
        self.processor = CUDADataProcessor()
        self.current_location = "Washington, DC, USA"  # Default location
        self.collector = None
        self.location_coordinates = {}
        
    def set_location(self, location):
        """Update the current location and reinitialize data collector"""
        self.current_location = location
        if self.collector:
            self.collector.running = False
        self.collector = RealTimeDataCollector(location)
        self.collector.start_collection()
        
        # Update location coordinates for map centering
        self._update_location_coordinates(location)
    
    def _update_location_coordinates(self, location):
        """Get coordinates for the location to center the map"""
        # Common city coordinates - you can expand this or use a geocoding API
        coordinates_db = {
            "Washington, DC, USA": {"lat": 38.9072, "lon": -77.0369, "zoom": 10},
            "New York, NY, USA": {"lat": 40.7128, "lon": -74.0060, "zoom": 10},
            "Los Angeles, CA, USA": {"lat": 34.0522, "lon": -118.2437, "zoom": 10},
            "Chicago, IL, USA": {"lat": 41.8781, "lon": -87.6298, "zoom": 10},
            "London, UK": {"lat": 51.5074, "lon": -0.1278, "zoom": 10},
            "Paris, France": {"lat": 48.8566, "lon": 2.3522, "zoom": 10},
            "Tokyo, Japan": {"lat": 35.6762, "lon": 139.6503, "zoom": 10},
            "Sydney, Australia": {"lat": -33.8688, "lon": 151.2093, "zoom": 10},
            "Berlin, Germany": {"lat": 52.5200, "lon": 13.4050, "zoom": 10},
            "Toronto, Canada": {"lat": 43.6511, "lon": -79.3470, "zoom": 10},
            "Miami, FL, USA": {"lat": 25.7617, "lon": -80.1918, "zoom": 10},
            "Seattle, WA, USA": {"lat": 47.6062, "lon": -122.3321, "zoom": 10},
            "Denver, CO, USA": {"lat": 39.7392, "lon": -104.9903, "zoom": 10},
            "San Francisco, CA, USA": {"lat": 37.7749, "lon": -122.4194, "zoom": 10}
        }
        
        # Default to a general view if location not found
        if location in coordinates_db:
            self.location_coordinates = coordinates_db[location]
        else:
            # Try to parse city/country from location string
            if "USA" in location:
                self.location_coordinates = {"lat": 39.8283, "lon": -98.5795, "zoom": 4}  # Center of USA
            elif "UK" in location or "England" in location:
                self.location_coordinates = {"lat": 54.3781, "lon": -3.4360, "zoom": 6}   # Center of UK
            elif "France" in location:
                self.location_coordinates = {"lat": 46.2276, "lon": 2.2137, "zoom": 6}    # Center of France
            elif "Germany" in location:
                self.location_coordinates = {"lat": 51.1657, "lon": 10.4515, "zoom": 6}   # Center of Germany
            elif "Japan" in location:
                self.location_coordinates = {"lat": 36.2048, "lon": 138.2529, "zoom": 5}  # Center of Japan
            elif "Australia" in location:
                self.location_coordinates = {"lat": -25.2744, "lon": 133.7751, "zoom": 4} # Center of Australia
            elif "Canada" in location:
                self.location_coordinates = {"lat": 56.1304, "lon": -106.3468, "zoom": 4} # Center of Canada
            else:
                # World view as ultimate fallback
                self.location_coordinates = {"lat": 20, "lon": 0, "zoom": 2}

def create_location_aware_dashboard():
    """Create the main dashboard with dynamic location support"""
    st.set_page_config(
        page_title="RTACC Crisis Detection System", 
        page_icon="🚨", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state for dashboard
    if 'dashboard' not in st.session_state:
        st.session_state.dashboard = DynamicCrisisDashboard()
    
    dashboard = st.session_state.dashboard
    
    # Sidebar for location selection
    with st.sidebar:
        st.header("🌍 Location Settings")
        
        # Location selector
        location_options = [
            "Washington, DC, USA",
            "New York, NY, USA", 
            "Los Angeles, CA, USA",
            "Chicago, IL, USA",
            "Miami, FL, USA",
            "Seattle, WA, USA",
            "Denver, CO, USA",
            "San Francisco, CA, USA",
            "London, UK",
            "Paris, France",
            "Berlin, Germany",
            "Tokyo, Japan",
            "Sydney, Australia",
            "Toronto, Canada"
        ]
        
        selected_location = st.selectbox(
            "Select Location for Monitoring:",
            location_options,
            index=location_options.index(dashboard.current_location) if dashboard.current_location in location_options else 0
        )
        
        # Custom location input
        custom_location = st.text_input(
            "Or enter custom location:",
            placeholder="e.g., Boston, MA, USA"
        )
        
        if custom_location:
            selected_location = custom_location
        
        # Update location if changed
        if selected_location != dashboard.current_location:
            dashboard.set_location(selected_location)
            st.success(f"✅ Switched to monitoring: {selected_location}")
        
        st.divider()
        
        # Location info
        st.subheader(f"📍 Current Location")
        st.write(f"**{dashboard.current_location}**")
        
        coords = dashboard.location_coordinates
        if coords:
            st.write(f"📐 Lat: {coords['lat']:.4f}")
            st.write(f"📐 Lon: {coords['lon']:.4f}")
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("🔄 Auto-refresh (30s)", value=True)
        
        if st.button("🔄 Manual Refresh"):
            st.rerun()
    
    # Main dashboard header with dynamic location
    st.title(f"🚨 RTACC Crisis Detection System")
    st.subheader(f"📍 Monitoring: **{dashboard.current_location}**")
    
    # Status indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 10px;">
            <h3>🌍 Active Monitoring Location</h3>
            <h2 style="color: #1f77b4;">{dashboard.current_location}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Get current data
    if dashboard.collector:
        try:
            latest_data = dashboard.collector.get_latest_data()
            crisis_result = dashboard.processor.process_crisis_detection(latest_data)
            
            # Crisis level indicator with location
            risk_level = crisis_result['risk_level']
            crisis_score = crisis_result['crisis_score']
            
            # Dynamic risk level display
            risk_colors = {
                'LOW': '#28a745',
                'MEDIUM': '#ffc107', 
                'HIGH': '#fd7e14',
                'CRITICAL': '#dc3545'
            }
            
            risk_color = risk_colors.get(risk_level, '#6c757d')
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background-color: {risk_color}; color: white; border-radius: 15px; margin: 20px 0;">
                <h1>🚨 CRISIS LEVEL: {risk_level}</h1>
                <h2>📊 Score: {crisis_score:.3f} | 📍 {dashboard.current_location}</h2>
                <p>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🗺️ Map View", "📈 Analytics", "⚙️ Resources"])
            
            with tab1:
                create_overview_tab(latest_data, crisis_result, dashboard.current_location)
            
            with tab2:
                create_dynamic_map_tab(latest_data, crisis_result, dashboard)
            
            with tab3:
                create_analytics_tab(latest_data, crisis_result, dashboard.current_location)
            
            with tab4:
                create_resources_tab(crisis_result, dashboard.current_location)
                
        except Exception as e:
            st.error(f"⚠️ Error loading data for {dashboard.current_location}: {str(e)}")
            st.info("Please check your internet connection and try refreshing the page.")
    
    else:
        st.warning(f"⚠️ Data collector not initialized for {dashboard.current_location}")
        if st.button("🔄 Initialize Data Collection"):
            dashboard.set_location(dashboard.current_location)
            st.rerun()
    
    # Auto-refresh logic
    if auto_refresh:
        import time
        time.sleep(30)
        st.rerun()

def create_overview_tab(data, crisis_result, location):
    """Create overview tab with location-specific information"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"🌤️ Weather Risk - {location}")
        weather_data = data.get('weather', [])
        if weather_data:
            latest_weather = weather_data[-1]
            weather_risk = crisis_result['weather_risk']
            
            # Weather gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=weather_risk,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"Weather Risk<br><span style='font-size:0.8em;color:gray'>{location}</span>"},
                delta={'reference': 0.3},
                gauge={
                    'axis': {'range': [None, 1]},
                    'bar': {'color': "lightblue"},
                    'steps': [
                        {'range': [0, 0.3], 'color': "lightgray"},
                        {'range': [0.3, 0.6], 'color': "yellow"},
                        {'range': [0.6, 1], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 0.8
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Weather details for location
            st.write(f"**Current Weather in {location}:**")
            st.write(f"🌡️ Temperature: {latest_weather.get('temperature', 'N/A')}°C")
            st.write(f"💨 Wind Speed: {latest_weather.get('wind_speed', 'N/A')} km/h")
            st.write(f"💧 Humidity: {latest_weather.get('humidity', 'N/A')}%")
        
        else:
            st.warning(f"No weather data available for {location}")
    
    with col2:
        st.subheader(f"🚗 Traffic Risk - {location}")
        traffic_data = data.get('traffic', [])
        if traffic_data:
            traffic_risk = crisis_result['traffic_risk']
            
            # Traffic gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=traffic_risk,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"Traffic Risk<br><span style='font-size:0.8em;color:gray'>{location}</span>"},
                delta={'reference': 0.4},
                gauge={
                    'axis': {'range': [None, 1]},
                    'bar': {'color': "orange"},
                    'steps': [
                        {'range': [0, 0.3], 'color': "lightgray"},
                        {'range': [0.3, 0.6], 'color': "yellow"},
                        {'range': [0.6, 1], 'color': "red"}
                    ]
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Traffic details for location
            recent_traffic = traffic_data[-5:]
            avg_congestion = np.mean([t.get('congestion_level', 0) for t in recent_traffic])
            incidents = sum(t.get('incident_detected', False) for t in recent_traffic)
            
            st.write(f"**Traffic Status in {location}:**")
            st.write(f"🚦 Avg Congestion: {avg_congestion:.1%}")
            st.write(f"🚨 Active Incidents: {incidents}")
            st.write(f"📊 Data Points: {len(traffic_data)}")
        
        else:
            st.warning(f"No traffic data available for {location}")

def create_dynamic_map_tab(data, crisis_result, dashboard):
    """Create map tab with dynamic location centering"""
    st.subheader(f"🗺️ Crisis Map - {dashboard.current_location}")
    
    # Get location coordinates
    coords = dashboard.location_coordinates
    
    if not coords:
        st.error("Unable to get coordinates for the selected location")
        return
    
    # Create base map centered on current location
    fig = go.Figure()
    
    # Add location marker
    fig.add_trace(go.Scattermapbox(
        lat=[coords['lat']],
        lon=[coords['lon']],
        mode='markers+text',
        marker=dict(
            size=20,
            color='red' if crisis_result['risk_level'] in ['HIGH', 'CRITICAL'] else 'green',
            symbol='circle'
        ),
        text=[dashboard.current_location],
        textposition='top center',
        name=f'Monitoring Location',
        hovertemplate=f"""
        <b>{dashboard.current_location}</b><br>
        Risk Level: {crisis_result['risk_level']}<br>
        Crisis Score: {crisis_result['crisis_score']:.3f}<br>
        <extra></extra>
        """
    ))
    
    # Add risk zones around the location
    risk_level = crisis_result['risk_level']
    if risk_level in ['HIGH', 'CRITICAL']:
        # Add risk radius visualization
        radius_km = 10 if risk_level == 'HIGH' else 20
        
        # Create circle approximation
        lats, lons = create_circle_coords(coords['lat'], coords['lon'], radius_km)
        
        fig.add_trace(go.Scattermapbox(
            lat=lats,
            lon=lons,
            mode='lines',
            line=dict(width=3, color='red' if risk_level == 'CRITICAL' else 'orange'),
            name=f'{risk_level} Risk Zone',
            hoverinfo='skip'
        ))
    
    # Add incident markers if available
    traffic_data = data.get('traffic', [])
    incident_locations = []
    for traffic in traffic_data[-10:]:  # Last 10 traffic data points
        if traffic.get('incident_detected', False):
            # Simulate incident locations around the main location
            incident_lat = coords['lat'] + np.random.normal(0, 0.01)
            incident_lon = coords['lon'] + np.random.normal(0, 0.01)
            incident_locations.append((incident_lat, incident_lon))
    
    if incident_locations:
        incident_lats, incident_lons = zip(*incident_locations)
        fig.add_trace(go.Scattermapbox(
            lat=incident_lats,
            lon=incident_lons,
            mode='markers',
            marker=dict(
                size=12,
                color='orange',
                symbol='triangle-up'
            ),
            name='Traffic Incidents',
            hovertemplate='Traffic Incident<extra></extra>'
        ))
    
    # Update map layout with dynamic center
    fig.update_layout(
        mapbox=dict(
            accesstoken='pk.your_mapbox_token_here',  # You'll need a Mapbox token
            style='open-street-map',  # Use OpenStreetMap as free alternative
            center=dict(lat=coords['lat'], lon=coords['lon']),
            zoom=coords['zoom']
        ),
        height=600,
        title=f"Crisis Monitoring Map - {dashboard.current_location}",
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Map legend
    st.markdown(f"""
    **Map Legend for {dashboard.current_location}:**
    - 🔴 Red Circle: {crisis_result['risk_level']} risk area
    - 🟢 Green Marker: Normal monitoring location
    - 🔺 Orange Triangles: Traffic incidents
    - 🗺️ Centered on: {coords['lat']:.4f}, {coords['lon']:.4f}
    """)

def create_circle_coords(center_lat, center_lon, radius_km):
    """Create coordinates for a circle on the map"""
    import math
    
    points = 50
    angles = np.linspace(0, 2*math.pi, points)
    
    # Convert radius from km to degrees (approximate)
    radius_deg = radius_km / 111.0  # 1 degree ≈ 111 km
    
    lats = center_lat + radius_deg * np.cos(angles)
    lons = center_lon + (radius_deg * np.sin(angles)) / math.cos(math.radians(center_lat))
    
    return lats.tolist(), lons.tolist()

def create_analytics_tab(data, crisis_result, location):
    """Create analytics tab with location-specific data"""
    st.subheader(f"📈 Analytics Dashboard - {location}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Risk Breakdown for {location}:**")
        
        # Risk breakdown chart
        risks = {
            'Weather': crisis_result['weather_risk'],
            'Traffic': crisis_result['traffic_risk'], 
            'Social': crisis_result['social_risk'],
            'News': crisis_result['news_risk']
        }
        
        fig = px.bar(
            x=list(risks.keys()),
            y=list(risks.values()),
            title=f"Risk Components - {location}",
            color=list(risks.values()),
            color_continuous_scale=['green', 'yellow', 'red']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write(f"**Data Quality for {location}:**")
        
        # Data availability chart
        data_counts = {
            'Weather': len(data.get('weather', [])),
            'Traffic': len(data.get('traffic', [])),
            'Social': len(data.get('social', [])),
            'News': len(data.get('news', []))
        }
        
        fig = px.pie(
            values=list(data_counts.values()),
            names=list(data_counts.keys()),
            title=f"Data Distribution - {location}"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Time series data
    st.subheader(f"📊 Time Series Analysis - {location}")
    
    # Create sample time series for crisis score
    if len(data.get('weather', [])) > 1:
        times = [datetime.now() - timedelta(minutes=i*5) for i in range(len(data['weather']))]
        scores = [w.get('risk_score', 0) for w in data['weather']]
        
        df = pd.DataFrame({
            'Time': times,
            'Risk Score': scores
        })
        
        fig = px.line(df, x='Time', y='Risk Score', 
                     title=f'Risk Score Trend - {location}')
        st.plotly_chart(fig, use_container_width=True)

def create_resources_tab(crisis_result, location):
    """Create resources tab with location-specific recommendations"""
    st.subheader(f"⚙️ Resource Allocation - {location}")
    
    # Get resource optimization
    available_resources = ['police', 'ambulance', 'fire_department', 'emergency_management']
    resource_plan = crisis_result  # You'd call optimize_resources here
    
    risk_level = crisis_result['risk_level']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Emergency Response Plan for {location}:**")
        
        if risk_level == 'CRITICAL':
            st.error(f"🚨 CRITICAL ALERT - {location}")
            st.write("**Immediate Actions Required:**")
            st.write("• Deploy all emergency services")
            st.write("• Activate emergency operations center")
            st.write("• Issue public safety warnings")
            st.write("• Consider evacuation procedures")
            
        elif risk_level == 'HIGH':
            st.warning(f"⚠️ HIGH ALERT - {location}")
            st.write("**Enhanced Response Actions:**")
            st.write("• Increase patrol presence")
            st.write("• Prepare emergency services") 
            st.write("• Monitor situation closely")
            st.write("• Alert relevant authorities")
            
        elif risk_level == 'MEDIUM':
            st.info(f"ℹ️ MEDIUM ALERT - {location}")
            st.write("**Monitoring Actions:**")
            st.write("• Increase surveillance")
            st.write("• Prepare response teams")
            st.write("• Update stakeholders")
            
        else:
            st.success(f"✅ LOW RISK - {location}")
            st.write("**Standard Operations:**")
            st.write("• Continue routine monitoring")
            st.write("• Maintain normal operations")
            st.write("• Regular status updates")
    
    with col2:
        st.write(f"**Resource Deployment Status:**")
        
        # Resource status
        resources = {
            'Police Units': '🚔' + (' DEPLOYED' if risk_level in ['HIGH', 'CRITICAL'] else ' STANDBY'),
            'Medical Teams': '🚑' + (' DEPLOYED' if risk_level == 'CRITICAL' else ' STANDBY'),
            'Fire Department': '🚒' + (' DEPLOYED' if risk_level == 'CRITICAL' else ' STANDBY'),
            'Emergency Mgmt': '📞' + (' ACTIVE' if risk_level in ['MEDIUM', 'HIGH', 'CRITICAL'] else ' MONITORING')
        }
        
        for resource, status in resources.items():
            if 'DEPLOYED' in status or 'ACTIVE' in status:
                st.success(f"{resource}: {status}")
            elif 'STANDBY' in status:
                st.warning(f"{resource}: {status}")
            else:
                st.info(f"{resource}: {status}")
        
        st.write(f"**Location-Specific Notes:**")
        st.write(f"• Monitoring: {location}")
        st.write(f"• Last Update: {datetime.now().strftime('%H:%M:%S')}")
        st.write(f"• Crisis Score: {crisis_result['crisis_score']:.3f}")

if __name__ == "__main__":
    create_location_aware_dashboard()