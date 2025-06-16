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

# AI Assistant section
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
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
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
st.caption("🚀 Built with 💙 by Prince using Streamlit, Gemini, and Google Weather Lab")
