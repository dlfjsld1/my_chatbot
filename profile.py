import streamlit as st

from auth_db import get_member_by_id, init_db


init_db()

if not st.session_state.get("member_id"):
    st.switch_page("login.py")

member = get_member_by_id(st.session_state.member_id)

if member is None:
    st.session_state.pop("member_id", None)
    st.session_state.pop("member_username", None)
    st.switch_page("login.py")

st.title("프로필")

st.subheader(member["name"])
st.write(f"아이디: {member['username']}")
st.write(f"이메일: {member['email']}")
st.write(f"전화번호: {member['phone'] or '-'}")
st.write(f"회원등급: {member['role']}")
st.write(f"가입일: {member['created_at']}")

if st.button("로그아웃"):
    st.session_state.pop("member_id", None)
    st.session_state.pop("member_username", None)
    st.switch_page("login.py")
