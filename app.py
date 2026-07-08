import streamlit as st

# st.title("강남구청")

# st.write("Hello World")



page_1 = st.Page("page_1.py", icon="😂")
page_2 = st.Page("page_2.py")
page_3 = st.Page("page_3.py")
page_4 = st.Page("page_4.py")



# load_dotenv()
st.header("AI agent 강남구청")
st.title("🦜🔗 빠른 시작 앱")
pages = st.navigation([page_1, page_2, page_3, page_4], position="top")

pages.run()

