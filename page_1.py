import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

st.title("My Chatbot")



if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input("무엇이든 물어보세요.")
if prompt:
    
    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "ai", "content": response.output_text})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
