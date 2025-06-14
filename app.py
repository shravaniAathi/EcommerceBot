import streamlit as st
import google.generativeai as genai

# 🔐 API key directly in code (if not using st.secrets)
genai.configure(api_key="PASTE_YOUR_API_KEY_HERE")  # Replace with your Gemini API key

# 💬 System prompt to guide Gemini
SYSTEM_PROMPT = """You are an ecommerce assistant.
You ONLY respond to questions related to online shopping, products, orders, shipping, returns, or customer service.
If the user asks something unrelated, politely reply:
"Sorry, I can only help with ecommerce-related questions." Be clear, concise, and helpful."""

# 🔁 Store chat history in session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "user", "parts": [SYSTEM_PROMPT]}]

# 🌐 Page settings
st.set_page_config(page_title="🛍️ EcommerceBot", page_icon="🛒")
st.title("🛍️ EcommerceBot")
st.caption("Your smart assistant for shopping questions")

# 💬 Show chat history
for message in st.session_state.chat_history[1:]:  # Skip system prompt
    with st.chat_message("user" if message["role"] == "user" else "assistant"):
        st.markdown(message["parts"][0])

# ✍️ Chat input
user_prompt = st.chat_input("Ask me about products, orders, delivery...")

# 🚀 Get and display response
if user_prompt:
    st.session_state.chat_history.append({"role": "user", "parts": [user_prompt]})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(st.session_state.chat_history)
        reply = response.text

        st.session_state.chat_history.append({"role": "model", "parts": [reply]})
        with st.chat_message("assistant"):
            st.markdown(reply)

    except Exception as e:
        st.error("❌ Failed to connect to Gemini. Please check your API key or try again.")
        st.exception(e)
