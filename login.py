import streamlit as st

from auth_db import authenticate, init_db


init_db()

st.title("로그인")

if st.session_state.get("member_id"):
    st.success("이미 로그인되어 있습니다.")
    if st.button("프로필로 이동"):
        st.switch_page("profile.py")
    st.stop()

with st.form("login_form"):
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    submitted = st.form_submit_button("로그인")

if submitted:
    member = authenticate(username.strip(), password)
    if member is None:
        st.error("아이디 또는 비밀번호가 올바르지 않습니다.")
    else:
        st.session_state.member_id = member["id"]
        st.session_state.member_username = member["username"]
        st.switch_page("profile.py")

if st.button("회원가입"):
    st.switch_page("signup.py")
