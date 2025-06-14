import streamlit as st
import google.generativeai as genai

# 🔑 Direct API Key (replace with your own Gemini API Key)
API_KEY = "your-gemini-api-key-here"  # 👈 Replace this!

# 🔧 Configure Gemini
genai.configure(api_key=API_KEY)

# ✅ Load Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# 💬 Session history
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "user", "text": (
            "You are a helpful AI assistant. ONLY answer questions related to ecommerce, "
            "product recommendations, online shopping, customer service, returns, and orders. "
            "If the user asks about anything else, respond with: "
            "'I'm only able to assist with ecommerce-related questions.'"
        )},
        {"role": "model", "text": "Hi! I'm here to help you with your ecommerce queries."}
    ]

# 🌍
