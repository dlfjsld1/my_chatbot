import streamlit as st
import pandas as pd

st.title("엑셀 데이터 뷰어")

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx", "xls"])

if uploaded_file is not None:
    # 모든 시트 읽기
    xls = pd.read_excel(uploaded_file, sheet_name=None)
    
    # 시트가 여러 개면 선택할 수 있도록
    sheet_names = list(xls.keys())
    selected_sheet = st.selectbox("시트를 선택하세요", sheet_names)
    
    df = xls[selected_sheet]
    
    st.write(f"**{selected_sheet}** 시트 데이터 ({df.shape[0]}행 × {df.shape[1]}열)")
    st.dataframe(df, use_container_width=True)