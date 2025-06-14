import streamlit as st
import google.generativeai as genai

# ✅ HARDCODE API KEY (Replace with yours)
GOOGLE_API_KEY = "PASTE-YOUR-API-KEY-HERE"

# ✅ Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Use Gemini 1.5 Flash
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction="""
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
)

# ✅ Page layout
st.set_page_config(page_title="🌍 Travelio - AI Travel Assistant", layout="centered")
st.title("🌍 Travelio - Your AI Travel Assistant")
st.caption("Ask about destinations, visas, attractions, tips & more!")

# ✅ History (for multi-turn context)
if "history" not in st.session_state:
    st.session_state.history = []

# ✅ Display previous messages
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# ✅ User input
user_input = st.chat_input("Where do you want to go?")

if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.history.append({"role": "user", "text": user_input})

    # Get Gemini response
    with st.spinner("Travelio is planning your trip..."):
        response = model.generate_content(
            st.session_state.history[-10:]  # Last 10 messages
        )
        reply = response.text

    # Display Gemini response
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Store assistant reply in history
    st.session_state.history.append({"role": "model", "text": reply})
