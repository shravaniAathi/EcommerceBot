import streamlit as st
import google.generativeai as genai

# 🔐 Gemini API Key (enter directly if not using st.secrets)
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=API_KEY)

# 🧠 Travel-specific system behavior prompt
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

# 🧠 Initialize Gemini model with system-level prompt
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[
    {"role": "user", "parts": [system_prompt]}
])

# 📄 Page setup
st.set_page_config(page_title="🌍 Travelio - Your Travel Assistant")
st.title("🌍 Travelio - Your AI Travel Assistant")
st.caption("Ask me about travel destinations, tips, visas, itineraries, and more!")

# 💬 Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 💾 Display chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

# 📝 Chat input
user_input = st.chat_input("Where are you planning to go?")

# 🔁 Chat interaction
if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    # Get Gemini response
    with st.spinner("Travelio is preparing your travel guidance..."):
        response_text = ""
        response_stream = chat.send_message(user_input, stream=True)
        for chunk in response_stream:
            response_text += chunk.text
