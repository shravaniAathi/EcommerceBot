import streamlit as st
import google.generativeai as genai

# ✅ Replace with your actual Gemini API Key
genai.configure(api_key="YOUR_API_KEY")

# ✅ System prompt to limit scope to travel
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

# Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")

# Session state history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "user", "parts": [system_prompt]}
    ]

# Function to get response
def get_response(user_prompt):
    chat = model.start_chat(history=st.session_state.chat_history)
    response = chat.send_message(user_prompt)
    return response.text

# App layout
st.set_page_config(page_title="🌍 Travelio")
st.title("🌍 Travelio - Your AI Travel Assistant")
st.caption("Ask me about destinations, flights, visas, cultural tips, and more!")

# Display past chat
for message in st.session_state.chat_history[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"][0])

# ✅ Always show chat_input — must be at root level!
user_input = st.chat_input("Where are you planning to go?")

# Process new input
if user_input:
    # Show user's message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot reply
    with st.spinner("Travelio is thinking..."):
        response = get_response(user_input)

    # Show assistant reply
    with st.chat_message("model"):
        st.markdown(response)

    # Save chat history
    st.session_state.chat_history.append({"role": "user", "parts": [user_input]})
    st.session_state.chat_history.append({"role": "model", "parts": [response]})
