import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

st.title("My Chatbot")


def llm_stream(prompt):
    with client.responses.stream(
        model="gpt-5.5",
        input=prompt
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta


if "messages" not in st.session_state:
    st.session_state.messages = []


# 기존 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# 사용자 입력
prompt = st.chat_input("무엇이든 물어보세요.")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("답변 생성 중...", show_time=True):
            response = st.write_stream(llm_stream(prompt))

    # AI 응답 저장
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })