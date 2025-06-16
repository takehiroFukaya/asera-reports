import streamlit as st

st.set_page_config(
    page_title="日報アプリ", layout="centered", initial_sidebar_state="collapsed"
)
st.title("日報アプリ")


if st.button("作業登録"):
    st.switch_page("pages/workReport.py")
if st.button("勤怠登録"):
    st.switch_page("pages/dayReport.py")
if st.button("出勤簿作成"):
    st.switch_page("pages/workRecord.py")
