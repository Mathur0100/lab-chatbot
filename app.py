import os
import streamlit as st

# Show the file path
st.write("📂 Current file location:", os.path.abspath(__file__))

# --- your existing code starts below ---

import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from .env file (recommended)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit page config
st.set_page_config(page_title="College Chatbot", page_icon="🎓")
st.title("🎓 College Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful college assistant. Answer questions about academics, events, and campus life in a friendly way."}
    ]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] != "system":  # don't show system messages
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything about college life..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate bot response
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
