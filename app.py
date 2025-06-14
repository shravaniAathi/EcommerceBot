import streamlit as st
import google.generativeai as genai

# 🧠 Configure Gemini with API key (Set it directly here for Streamlit Cloud)
genai.configure(api_key="PASTE_YOUR_API_KEY_HERE")  # Replace this with your real key

# 💬 System prompt: Set the assistant's behavior
SYSTEM_PROMPT = """You are an ecommerce assistant. 
Only answer questions related to online shopping, products, delivery, returns, and customer support. 
Politely reject unrelated topics like programming, history, politics, etc."""

# 🧠 Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")

# 🗂️ Store conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "user", "parts": [SYSTEM_PROMPT]}]

# 📄 Page settings
st.set_page_config(page_title="🛒 EcommerceBot", page_icon="🛍️")
st.title("🛒 EcommerceBot")
st.caption("Your smart assistant for online shopping help!")

# 💬 Display chat history
for message in st.session_state.chat_history[1:]:  # Skip system prompt in UI
    with st.chat_message("user" if message["role"] == "user" else "assistant"):
        st.markdown(message["parts"][0])

# 🧾 Chat input
user_prompt = st.chat_input("Ask about products, orders, or delivery...")

# 🤖 Get response from Gemini
if user_prompt:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "parts": [user_prompt]})
    with st.chat_message("user"):
