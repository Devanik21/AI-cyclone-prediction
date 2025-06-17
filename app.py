import streamlit as st
import requests
import json
from PIL import Image

# --- Sidebar ---
st.sidebar.title("🔐 API Keys")
gemini_api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
owm_api_key = st.sidebar.text_input("Enter your OpenWeatherMap API Key:", type="password") # Added OWM key input

# App title
st.title("🌀 Cyclone & Weather Viewer – Powered by AI + Google Weather Lab") # Updated title slightly
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
    if not owm_api_key:
        st.warning("🔑 Please enter your OpenWeatherMap API key to get weather data.")
    elif not location:
        st.warning("📍 Please enter a location.")
    else:
        # OpenWeatherMap API endpoint for current weather
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={owm_api_key}&units=metric" # Using metric units

        try:
            weather_response = requests.get(weather_url, timeout=10)
            if weather_response.ok:
                weather_data = weather_response.json()
                if weather_data and weather_data.get("cod") != "404": # Check for valid response and not city not found
                    main_data = weather_data.get("main", {})
                    weather_desc = weather_data.get("weather", [{}])[0].get("description", "N/A")
                    temp = main_data.get("temp", "N/A")
                    feels_like = main_data.get("feels_like", "N/A")
                    humidity = main_data.get("humidity", "N/A")
                    wind_speed = weather_data.get("wind", {}).get("speed", "N/A") # Wind speed in m/s with units=metric

                    st.success(f"Current weather in {weather_data.get('name', location)}:")
                    st.write(f"**Description:** {weather_desc.capitalize()}")
                    st.write(f"**Temperature:** {temp}°C")
                    st.write(f"**Feels like:** {feels_like}°C")
                    st.write(f"**Humidity:** {humidity}%")
                    st.write(f"**Wind Speed:** {wind_speed} m/s")

                    # Optional: Display weather icon if available
                    icon_code = weather_data.get("weather", [{}])[0].get("icon")
                    if icon_code:
                         icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                         st.image(icon_url, width=50)

                else:
                     st.error(f"❌ Location not found or invalid response.")

            else:
                st.error(f"❌ Failed to fetch weather data: {weather_response.status_code} {weather_response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request error fetching weather: {e}")

# AI Assistant section
if gemini_api_key: # Use the updated variable name
    st.header("🤖 AI Assistant – Gemini")
    user_prompt = st.text_area("Ask Gemini about cyclone risks, patterns, or predictions:", key="gemini_prompt") # Added key to avoid potential conflicts
    if st.button("🔍 Get Insight from Gemini", key="gemini_button"): # Added key
        headers = {
            "Authorization": f"Bearer {gemini_api_key}", # Use updated variable name
            "Content-Type": "application/json"
        }
        data = {
            "contents": [{"role": "user", "parts": [user_prompt]}],
            "generationConfig": {"temperature": 0.7},
            "safetySettings": []
        }

        try:
            response = requests.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
                headers=headers,
                data=json.dumps(data),
                timeout=15
            )
            if response.ok:
                result = response.json()
                # Adjust path based on actual Gemini API response:
                # Added checks for nested keys
                ai_reply = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Could not parse Gemini response.')
                st.success("✨ Gemini's Response:")
                st.markdown(ai_reply)
            else:
                st.error(f"❌ Failed: {response.status_code} {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request error: {e}")
else:
    st.warning("🔑 Please enter your Gemini API key to use the AI assistant.")

# Footer
st.markdown("---")
st.caption("Built with 💙 using Streamlit, Gemini, and OpenWeatherMap") # Updated footer
