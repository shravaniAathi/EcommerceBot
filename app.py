import streamlit as st
import google.generativeai as genai

# 🔐 API key directly (replace with your key from Google AI Studio)
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# 💬 Topic restriction (Travel only)
system_prompt = """
You are Travelio, an AI travel assistant. Your ONLY task is to help users with travel and tourism-related information.

✅ Allowed topics include:
- Destinations and attractions
- Flights, hotels, itineraries
- Travel tips, visa requirements
- Cultural advice, packing, safety, budgeting

🚫 Strictly avoid and do NOT respond to:
- Programming, math, tech, history, sports, health, or any non-travel topic

If the user asks something unrelated to travel, ALWAYS reply:
"Sorry, I can only answer travel and tourism-related questions."

Be polite, professional, helpful, and concise.
"""

# 🧠 Initialize Gemini Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# 🧠 Store chat history in session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "user", "parts": [system_prompt]}  # Set system prompt
    ]

# 📤 Function to send and get Gemini response
def get_response(prompt):
    chat = model.start_chat(history=st.session_state.chat_history)
    response = chat.send_message(prompt)
    return response.text

# 🖼️ Streamlit UI
st.set_page_config(page_title="🌍 Travelio - AI Travel Assistant")
st.title("🌍 Travelio - Your AI Travel Assistant")
st.caption("Ask me about destinations, visas, flights, hotels, safety tips, and more!")

# 💬 Display past chat (skip sy
