import streamlit as st
import requests
import json
from PIL import Image

# --- Sidebar ---
st.sidebar.title("🔐 API Keys")
gemini_api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
weatherapi_key = st.sidebar.text_input("Enter your WeatherAPI Key:", type="password")  # Added WeatherAPI key input

# App title
st.title("🌀 Cyclone & Weather Viewer – Powered by AI + Google Weather Lab")  # Updated title slightly
st.markdown("""
Welcome to your interactive cyclone dashboard 🌧️  
View and compare AI-based cyclone forecasts in real-time using Google's Weather Lab.

Make sure you’ve entered your Gemini API key to enable AI assistance below!
""")

# Weather Lab Info
st.header("🌍 Live Cyclone Predictions – Google Weather Lab")
st.markdown("""
Google’s **Weather Lab** showcases AI cyclone predictions vs traditional models.  
Click below to open the live dashboard ⬇️
""")

# Use a clickable link styled as a button or simple link
# Option 1: Simple link
st.markdown("[🔗 Open Weather Lab](https://goo.gle/4l9hsiJ)")

# Option 2: HTML-styled button (if you like a button look; may need allow HTML)
# st.markdown(
#     "<a href='https://goo.gle/4l9hsiJ' target='_blank'><button style='padding:0.5em 1em; border-radius:0.5em; background-color:#1f77b4; color:white; border:none;'>🔗 Open Weather Lab</button></a>",
#     unsafe_allow_html=True
# )

# Optional preview image (updated parameter)
st.image(
    "https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Weather-Lab-Launch-Screenshot-1.max-1000x1000.png",
    caption="Preview of Google Weather Lab",
    use_container_width=True
)

# --- Current Weather Section (Added) ---
st.header("☁️ Current Location Weather")
st.markdown("Get current weather data for any city.")

location = st.text_input("Enter city name (e.g., London, Tokyo):")

if st.button("🔍 Get Weather"):
    if not weatherapi_key:
        st.warning("🔑 Please enter your WeatherAPI key to get weather data.")
    elif not location:
        st.warning("📍 Please enter a location.")
    else:
        # WeatherAPI endpoint for current weather
        weather_url = f"http://api.weatherapi.com/v1/current.json?key={weatherapi_key}&q={location}&aqi=no"

        try:
            weather_response = requests.get(weather_url, timeout=10)
            if weather_response.ok:
                weather_data = weather_response.json()
                if weather_data and "error" not in weather_data:  # Check for valid response (no error)
                    current = weather_data.get("current", {})
                    location_data = weather_data.get("location", {})

                    st.success(f"Current weather in {location_data.get('name', location)}, {location_data.get('country', '')}:")
                    st.write(f"**Description:** {current.get('condition', {}).get('text', 'N/A')}")
                    st.write(f"**Temperature:** {current.get('temp_c', 'N/A')}°C")
                    st.write(f"**Feels like:** {current.get('feelslike_c', 'N/A')}°C")
                    st.write(f"**Humidity:** {current.get('humidity', 'N/A')}%")
                    st.write(f"**Wind Speed:** {current.get('wind_kph', 'N/A')} kph")

                    # Display weather icon
                    icon_url = "https:" + current.get("condition", {}).get("icon", "")  # Ensure https
                    st.image(icon_url, width=100)

                else:
                    st.error(f"❌ Location not found or invalid response: {weather_data.get('error', {}).get('message', 'Unknown error')}")
            else:
                st.error(f"❌ Failed to fetch weather data: {weather_response.status_code} {weather_response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request error fetching weather: {e}")

# ... (rest of your AI assistant code and footer remains the same)
