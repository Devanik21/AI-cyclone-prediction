import streamlit as st
import requests
import json
from PIL import Image

# Sidebar — Gemini API Key input
st.sidebar.title("🔐 Gemini API Key")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

# App title
st.title("🌀 Cyclone Prediction Viewer – Powered by AI + Google Weather Lab")
st.markdown("""
Welcome to your interactive cyclone dashboard 🌧️  
View and compare AI-based cyclone forecasts in real-time using Google's **Weather Lab**.

> _Make sure you’ve entered your Gemini API key to enable AI assistance below!_
""")

# Weather Lab preview
st.header("🌍 Live Cyclone Predictions")
st.markdown("[🔗 Open Weather Lab](https://goo.gle/4l9hsiJ) – Real-time AI forecasts by Google")

st.components.v1.iframe("https://weather.google/intl/en/weather-lab/", height=700)

# Gemini interaction
if api_key:
    st.header("🤖 AI Assistant – Gemini")
    user_prompt = st.text_area("Ask Gemini about cyclone risks, patterns, or predictions:")

    if st.button("🔍 Get Insight from Gemini"):
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "contents": [{"role": "user", "parts": [user_prompt]}],
            "generationConfig": {"temperature": 0.7},
            "safetySettings": []
        }

        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            headers=headers,
            data=json.dumps(data)
        )

        if response.ok:
            result = response.json()
            ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            st.success("✨ Gemini's Response:")
            st.markdown(ai_reply)
        else:
            st.error("❌ Failed to fetch response. Check your API key or try again later.")
else:
    st.warning("🔑 Please enter your Gemini API key to use the AI assistant.")

# Footer
st.markdown("---")
st.caption("🚀 Built with 💙 by Prince using Streamlit, Gemini, and Google Weather Lab")
