
import streamlit as st
import google.generativeai as genai

# 🔐 Set up Gemini with API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 🔧 System-level rules and strict negative prompt
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

# 🧠 Initialize Gemini model with the prompt
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[
    {"role": "user", "parts": [system_prompt]}
])

# 🔁 Chat response function
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# 🧠 Session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 🌐 Streamlit page config
st.set_page_config(
    page_title="Travelio - AI Travel Assistant",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Travelio - Your AI Travel Assistant")
st.caption("Ask me anything about travel, destinations, visas, tips, and more!")

# 💬 Display chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(f"**{role.capitalize()}:** {msg}")

# 📝 Chat input
if prompt := st.chat_input("Where are you planning to go?"):
    with st.chat_message("user"):
        st.markdown(f"**You:** {prompt}")

    # 💡 Get Gemini response
    with st.spinner("Travelio is preparing your travel guidance..."):
        response_stream = get_gemini_response(prompt)
        assistant_reply = ""
        for chunk in response_stream:
            assistant_reply += chunk.text

    with st.chat_message("assistant"):
        st.markdown(f"**Travelio:** {assistant_reply}")

    # 💾 Update session state
    st.session_state.chat_history.append(("user", prompt))
    st.session_state.chat_history.append(("assistant", assistant_reply))
