import streamlit as st
import google.generativeai as genai

# Configure Gemini API key directly (ONLY do this in private or secure apps!)
genai.configure(api_key="YOUR_API_KEY")

# 🌍 Define system prompt with allowed/blocked topics
system_instruction = """
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

# 🧠 Load Gemini 1.5 Flash model with system rules
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# 💬 Track chat history in session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()

# 🧠 Page layout
st.set_page_config(page_title="🌍 Travelio - AI Travel Assistant_
