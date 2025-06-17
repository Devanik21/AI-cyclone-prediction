import streamlit as st
import requests
import json

# --- Page Configuration (should be the first Streamlit command) ---
st.set_page_config(page_title="Cyclone & Weather Viewer", page_icon="🌀", layout="wide")

# --- API Configuration ---
WEATHERAPI_BASE_URL = "http://api.weatherapi.com/v1/current.json"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# --- Sidebar ---
st.sidebar.title("🔐 API Keys")
st.sidebar.markdown("Enter your API keys below to enable all features.")
st.sidebar.markdown("""
    - **WeatherAPI Key**: For current weather data. Get one from [WeatherAPI.com](https://www.weatherapi.com/).
    - **Gemini API Key**: For AI-powered insights. Get one from [Google AI Studio](https://aistudio.google.com/app/apikey).
""")
gemini_api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
weatherapi_key = st.sidebar.text_input("Enter your WeatherAPI Key:", type="password")  # Added WeatherAPI key input

# App title
st.title("🌀 Cyclone & Weather Viewer – Powered by AI + Google Weather Lab")  # Updated title slightly
st.markdown("""
Welcome to your interactive cyclone dashboard 🌧️  
View and compare AI-based cyclone forecasts in real-time using Google's Weather Lab.
---
Make sure you’ve entered your Gemini API key to enable AI assistance below!
""")

# Weather Lab Info
st.header("🌍 Live Cyclone Predictions – Google Weather Lab")
st.markdown("""
Google’s **Weather Lab** showcases AI cyclone predictions vs traditional models.  
Click below to open the live dashboard ⬇️
""")

st.markdown("[🔗 Open Weather Lab](https://goo.gle/4l9hsiJ)")

# Optional preview image (updated parameter)
st.image(
    "https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Weather-Lab-Launch-Screenshot-1.max-1000x1000.png",
    caption="Preview of Google Weather Lab",
    use_container_width=True
)

# --- Helper Functions ---
def display_weather_data(location_input, api_key):
    """Fetches and displays weather data from WeatherAPI."""
    if not api_key:
        st.warning("🔑 Please enter your WeatherAPI key in the sidebar to get weather data.")
        return
    if not location_input:
        st.warning("📍 Please enter a location.")
        return

    params = {"key": api_key, "q": location_input, "aqi": "no"}
    try:
        with st.spinner(f"Fetching weather for {location_input}..."):
            response = requests.get(WEATHERAPI_BASE_URL, params=params, timeout=10)
            response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)
            weather_data = response.json()

        if "error" in weather_data:
            st.error(f"❌ Error from WeatherAPI: {weather_data['error'].get('message', 'Unknown error')}")
            return

        current = weather_data.get("current", {})
        location_data = weather_data.get("location", {})

        st.success(f"Current weather in {location_data.get('name', location_input)}, {location_data.get('country', '')}:")
        
        col1, col2 = st.columns([3, 1]) # For text and icon

        with col1:
            st.write(f"**Description:** {current.get('condition', {}).get('text', 'N/A')}")
            st.write(f"**Temperature:** {current.get('temp_c', 'N/A')}°C ({current.get('temp_f', 'N/A')}°F)")
            st.write(f"**Feels like:** {current.get('feelslike_c', 'N/A')}°C ({current.get('feelslike_f', 'N/A')}°F)")
            st.write(f"**Humidity:** {current.get('humidity', 'N/A')}%")
            st.write(f"**Wind:** {current.get('wind_kph', 'N/A')} kph ({current.get('wind_mph', 'N/A')} mph) from {current.get('wind_dir', '')}")
            st.write(f"**Pressure:** {current.get('pressure_mb', 'N/A')} mb")
            st.write(f"**Precipitation:** {current.get('precip_mm', 'N/A')} mm")
            st.write(f"**Visibility:** {current.get('vis_km', 'N/A')} km ({current.get('vis_miles', 'N/A')} miles)")
            st.write(f"**UV Index:** {current.get('uv', 'N/A')}")
            st.write(f"**Last Updated:** {current.get('last_updated', 'N/A')}")

        with col2:
            icon_url_path = current.get("condition", {}).get("icon")
            if icon_url_path:
                # Ensure URL starts with https:
                full_icon_url = icon_url_path if icon_url_path.startswith("http") else f"https:{icon_url_path}"
                st.image(full_icon_url, caption=current.get('condition', {}).get('text', ''), width=100)

    except requests.exceptions.HTTPError as http_err:
        st.error(f"❌ HTTP error occurred: {http_err}")
        if response is not None and response.text:
             st.error(f"Response content: {response.text[:500]}...") # Show partial response
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request error fetching weather: {e}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")

def get_gemini_insight(prompt, api_key):
    """Gets insights from Gemini AI."""
    if not api_key:
        st.warning("🔑 Please enter your Gemini API key in the sidebar to use the AI assistant.")
        return
    if not prompt.strip():
        st.info("🤖 Please enter a prompt for Gemini.")
        return

    headers = {
        # Corrected header for Gemini API using API Key
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "topP": 0.9, "topK": 40},
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
    }

    try:
        with st.spinner("🤖 Gemini is thinking..."):
            response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(data), timeout=30) # Increased timeout
            response.raise_for_status()
            result = response.json()

        candidates = result.get('candidates')
        if candidates and isinstance(candidates, list) and len(candidates) > 0:
            content = candidates[0].get('content')
            if content and isinstance(content, dict):
                parts = content.get('parts')
                if parts and isinstance(parts, list) and len(parts) > 0:
                    ai_reply = parts[0].get('text')
                    if ai_reply:
                        st.success("✨ Gemini's Response:")
                        st.markdown(ai_reply)
                        return
        st.error("❌ Could not parse Gemini response or response was empty.")
        st.json(result) # Show raw response for debugging

    except requests.exceptions.HTTPError as http_err:
        st.error(f"❌ Gemini API error: {http_err}")
        try:
            st.json(response.json()) # Try to show error details from API
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request error with Gemini API: {e}")
        except Exception as e: # Catch all other errors during Gemini interaction
            st.error(f"❌ An unexpected error occurred with Gemini: {e}")

# --- Current Weather Section ---
st.header("☁️ Current Location Weather")
st.markdown("Get current weather data for any city using WeatherAPI.")
location_input = st.text_input("Enter city name (e.g., London, New York, Tokyo):", key="weather_location")
if st.button("🔍 Get Weather", key="get_weather_button"):
    display_weather_data(location_input, weatherapi_key)

# --- AI Assistant Section ---
st.header("🤖 AI Assistant – Powered by Gemini")
st.markdown("""
Ask Gemini about cyclone risks, weather patterns, climate predictions, or other related topics. 
Select an example below or type your own question.
""")

example_questions = [
    "What are the typical cyclone risks for coastal regions in Southeast Asia during monsoon season?",
    "Explain the El Niño effect on global weather patterns.",
    "Based on current trends, what are the long-term climate change predictions for the Arctic region?",
    "How can AI be used to improve early warnings for hurricanes?",
    "What are the main factors contributing to the intensity of a tropical cyclone?",
    "Summarize recent research on ocean temperature rise and its impact on weather."
]

selected_example = st.selectbox(
    "Select an example question (optional):",
    options=[""] + example_questions,  # Add an empty option for custom input
    index=0,
    key="gemini_example_select"
)
kkkkkkkk
user_prompt_value = selected_example if selected_example else ""
user_prompt = st.text_area("Your question for Gemini:", value=user_prompt_value, key="gemini_prompt", height=120)

if st.button("🔍 Get Insight from Gemini", key="gemini_button"):
    get_gemini_insight(user_prompt.strip(), gemini_api_key) # Ensure we pass a stripped prompt

# --- Footer ---
st.markdown("---")
st.caption("Built with 💙 using Streamlit, WeatherAPI, and Google Gemini AI.")
