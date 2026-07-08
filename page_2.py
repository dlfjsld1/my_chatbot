import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
# from dotenv import load_dotenv

st.header("기본 AI 챗봇")
st.title("page2")

openai_api_key = st.sidebar.text_input("OpenAI API 키", type="password")

def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    st.info(model.invoke(input_text).content)

with st.form("my_form"):
    text = st.text_area("텍스트 입력:", "코딩을 배우는 세 가지 핵심 조언은?")
    submitted = st.form_submit_button("제출")
    if not openai_api_key.startswith("sk-"):
        st.warning("OpenAI API 키를 입력해주세요!", icon="⚠")
    if submitted and openai_api_key.startswith("sk-"):
        generate_response(text)