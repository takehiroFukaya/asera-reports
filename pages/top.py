import streamlit as st

st.set_page_config(
    page_title="日報アプリ", layout="centered", initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap'
    );
    .stApp{
        background-color: #E5F2F0;
    }

    div.stHeading > div > div > h1 {
        display: flex;
        justify-content: center;
        color: #194352;
        font-size: 40px;
        font-family: "Inter", sans-serif;
        font-weight: 600;
    }

    div.stButton > button {
        width: 345px;
        height: 95px;
        color: #349AA6;
        border-radius: 20px;
        box-shadow: 0px 4px 4px rgba(0,0,0,0.25);
    }
    div.stButton > button > div{
    }
    div.stButton > button > div > p{
        font-size: 32px;
        font-family: "Inter", sans-serif;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background-color: #00000;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.title("課内日報")
    if st.button("作業登録"):
        st.switch_page("pages/workReport.py")
    if st.button("勤怠登録"):
        st.switch_page("pages/dayReport.py")
    if st.button("出勤簿作成"):
        st.switch_page("pages/workRecord.py")
