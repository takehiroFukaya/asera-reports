import streamlit as st

st.set_page_config(
    page_title="日報アプリ", layout="centered", initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    .stApp{
        background-color: #E5F2F0;
    }

    div[data-testid="stToolbar"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
    }
    div[data-testid="stDecoration"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
    }
    #MainMenu {
        visibility: hidden;
        height: 0%;
    }
    header {
        visibility: hidden;
        height: 0%;
    }
    footer {
        visibility: hidden;
        height: 0%;
    }
    .appview-container .main .block-container{
        padding-top: 1rem;
        padding-right: 3rem;
        padding-left: 3rem;
        padding-bottom: 1rem;
    }
    .reportview-container {
        padding-top: 0rem;
        padding-right: 3rem;
        padding-left: 3rem;
        padding-bottom: 0rem;
    }
    header[data-testid="stHeader"] {
        z-index: -1;
    }
    div[data-testid="stToolbar"] {
    z-index: 100;
    }
    div[data-testid="stDecoration"] {
    z-index: 100;
    }
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap'
    );
    [data-testid="stMainBlockContainer"] {
        display: flex;
        justify-content: center;
    }
    div.stHeading > div > div > h1 {
        display: flex;
        justify-content: center;
        font-size: 40px;
        font-family: "Inter", sans-serif;
        font-weight: 600;
        background-color: #194352;
        color: transparent;
        text-shadow: 2px 2px 3px rgba(255,255,255,0.3);
        -webkit-background-clip: text;
           -moz-background-clip: text;
                background-clip: text;
    }
    [data-testid="stColumn"] {
        display: flex;
        justify-content: center;
    }
    div.stButton > button {
        display: flex;
        justify-content: center;
        width: 345px;
        height: 95px;
        color: #349AA6;
        border-radius: 20px;
        box-shadow: 0px 4px 4px rgba(0,0,0,0.25);
    }
    div.stButton > button:hover {
        border-color: #349AA6;
        color: #349AA6;
    }
    div.stButton > button:active {
        border-color: #1a4d53;
        color: #1a4d53;
        background-color: #1a4d53;
    }
    div.stButton > button > div > p{
        font-size: 32px;
        font-family: "Inter", sans-serif;
        font-weight: 600;
        background-color: #349AA6;
        color: transparent;
        text-shadow: 2px 2px 3px rgba(255,255,255,0.3);
        -webkit-background-clip: text;
           -moz-background-clip: text;
                background-clip: text;
    }
    [data-testid="stButton"]::after {
        background-color: #67b3bc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.title("課内日報")
    if st.button("作業登録"):
        st.switch_page("pages/work_input.py")
    if st.button("勤怠登録"):
        st.switch_page("pages/shift_input.py")
    if st.button("出勤簿作成"):
        st.switch_page("pages/shift_record.py")
