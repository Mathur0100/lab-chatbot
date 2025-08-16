import streamlit as st
import json
import random
import openai

# Load equipment data
with open("equipment_data.json", "r") as f:
    equipment_data = json.load(f)

st.set_page_config(page_title="Lab Equipment Maintenance Bot", page_icon="🤖")

st.title("🤖 Predictive Maintenance Chatbot for Lab Equipment")
st.write("Ask me about lab equipment, maintenance schedules, or troubleshooting!")

# Input for user query
user_query = st.text_input("💬 Ask your question:")

# Load API key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_equipment_response(query):
    # Simple rule-based search in dataset
    for item in equipment_data:
        if item["name"].lower() in query.lower():
            return f"**{item['name']}**:\n\n- Last serviced: {item['last_service']}\n- Next due: {item['next_service']}\n- Common issue: {item['common_issue']}"
    
    # If not found in dataset → use AI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant for predictive maintenance of lab equipment."},
                  {"role": "user", "content": query}]
    )
    return response.choices[0].message["content"]

if st.button("Get Answer"):
    if user_query:
        with st.spinner("Thinking..."):
            answer = get_equipment_response(user_query)
        st.success(answer)
