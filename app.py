import streamlit as st
import google.generativeai as genai

# 🔐 Configure Gemini with API Key directly
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # Replace with your real API key

# 📌 System-level instructions (Topic: Travel only + Negative Prompt)
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

# 🧠 Load Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# 🧠 Session state to store conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "user", "parts": [system_prompt]}  # Start with system instructions
    ]

# 📤 Function to get AI reply
def get_response(user_prompt):
    # Create a new chat each time using stored history
    chat = model.start_chat(history=st.session_state.chat_history)
    response = chat.send_message(user_prompt)
    return response.text

# 🖼️ App layout
st.set_page_config(page_title="🌍 Travelio - AI Travel Assistant")
st.title("🌍 Travelio - Your AI Travel Assistant")
st.caption("Ask me about destinations, flights, visas, cultural tips, and more!")

# 💬 Display previous messages (skip system prompt)
for message in st.session_state.chat_history[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"][0])

# 📝 User input
user_input = st.chat_input("Where are you planning to go?")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get Gemini's response
    with st.spinner("Travelio is preparing your travel guidance..."):
        reply = get_response(user_input)

    # Show assistant reply
    with st.chat_message("model"):
        st.markdown(reply)

    # Save messages
    st.session_state.chat_history.append({"role": "user", "parts": [user_input]})
    st.session_state.chat_history.append({"role": "model", "parts": [reply]})

# 📌 Footer
st.markdown("---")
st.markdown("✈️ **Travelio is powered by Gemini 1.5 Flash — for travel questions only!**", unsafe_allow_html=True)
