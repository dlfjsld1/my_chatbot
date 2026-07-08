import streamlit as st

from auth_db import create_member, init_db


init_db()

st.title("회원가입")

if st.session_state.get("member_id"):
    st.success("이미 로그인되어 있습니다.")
    if st.button("프로필로 이동"):
        st.switch_page("profile.py")
    st.stop()

with st.form("signup_form"):
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    password_confirm = st.text_input("비밀번호 확인", type="password")
    name = st.text_input("이름")
    email = st.text_input("이메일")
    phone = st.text_input("전화번호")
    submitted = st.form_submit_button("가입하기")

if submitted:
    member_id, error_message = create_member(
        username,
        password,
        password_confirm,
        name,
        email,
        phone,
    )
    if member_id is None:
        st.error(error_message)
    else:
        st.session_state.member_id = member_id
        st.session_state.member_username = username.strip().lower()
        st.switch_page("profile.py")

if st.button("로그인으로 이동"):
    st.switch_page("login.py")
