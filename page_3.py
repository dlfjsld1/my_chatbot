import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from chat_loader import stream_with_thinking_loader

st.title("page3")

openai_api_key = st.sidebar.text_input("OpenAI API 키", type="password")

def llm_stream(prompt):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key, streaming=True, model="gpt-3.5-turbo")
    for chunk in model.stream(prompt):
        yield chunk.content

def save_feedback(index):
    st.session_state.history[index]["feedback"] = st.session_state[f"feedback_{index}"]

if "history" not in st.session_state:
    st.session_state.history = []

# 채팅 히스토리 표시
for i, message in enumerate(st.session_state.history):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant":
            feedback = message.get("feedback", None)
            st.session_state[f"feedback_{i}"] = feedback
            st.feedback(
                "thumbs",
                key=f"feedback_{i}",
                disabled=feedback is not None,
                on_change=save_feedback,
                args=[i],
            )

# 채팅 입력 처리
if prompt := st.chat_input("메시지를 입력하세요"):
    if not openai_api_key.startswith("sk-"):
        st.warning("사이드바에 OpenAI API 키를 입력해주세요!", icon="⚠")
    else:
        # 사용자 메시지 표시 및 저장
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.history.append({"role": "user", "content": prompt})

        # 어시스턴트 응답 스트리밍
        with st.chat_message("assistant"):
            loader = st.empty()
            response = st.write_stream(stream_with_thinking_loader(llm_stream(prompt), loader))
            st.feedback(
                "thumbs",
                key=f"feedback_{len(st.session_state.history)}",
                on_change=save_feedback,
                args=[len(st.session_state.history)],
            )
        st.session_state.history.append({"role": "assistant", "content": response})
