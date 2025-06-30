import streamlit as st
from utils.functions import generate_month_options

st.set_page_config(layout="centered")

st.markdown("""
<style>
    
    .stApp {
            background-color: #f0faf7;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
    }

    .main .block-container {
        padding: 1.5rem 1rem 2rem 1rem;
        background-color: #E0F2F1;
        border-radius: 10px; /* This is to ensure consistency if background is different */
    }
    /* Hide Streamlit's default header and footer */
    #MainMenu, footer {
        visibility: hidden;
    }

    /* --- Top Row Controls --- */
    /* Select box styling */
    div[data-baseweb="select"] > div {
        background-color: white;
        border-radius: 10px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 16px; /* Match text size */
    }
    /* Custom box for the "12 h" display */
    .hour-box {
        display: flex;
        align-items: center;
        justify-content: flex-end; /* Aligns content to the right */
        background-color: white;
        padding: 8px 12px;
        border-radius: 10px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        height: 42px; /* Manually match selectbox height */
        font-size: 16px;
        color: #555;
    }
    .hour-box .divider {
        border-left: 1px solid #BDBDBD;
        height: 20px;
        margin-right: 12px;
    }

    /* --- Summary Box --- */
    .summary-box {
        display: flex;
        justify-content: space-around;
        align-items: center;
        background-color: white;
        padding: 12px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin: 1.5rem 0;
        font-size: 16px;
        color: #5f6368;
    }
    .summary-item {
        display: flex;
        align-items: center;
        gap: 10px; /* Space between label and value */
    }
    .summary-item .value {
        color: #36a28b; /* Specific green from screenshot */
        font-weight: 600;
    }
    .summary-divider {
        border-left: 1px solid #E0E0E0;
        height: 24px;
    }

    /* --- Date Entry Cards --- */
    .date-card {
        background-color: white;
        padding: 16px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
    }
    .date-card .date {
        font-size: 16px;
        color: #333;
        font-weight: 500;
    }
    .date-card .time {
        font-size: 14px;
        color: #757575;
        margin-top: 4px;
    }

    /* --- Output Button --- */
    div.stButton > button {
        width: 100%;
        background-color: #4DB6AC; /* Teal button color from screenshot */
        color: white;
        border: none;
        border-radius: 10px;
        padding: 14px 0;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    div.stButton > button:hover {
        background-color: #26A69A; /* A slightly darker shade for hover */
        color: white;
        border: none;
    }

</style>
""", unsafe_allow_html=True)



col1, col2 = st.columns([1.5, 1])
month_options, default_index = generate_month_options()

with col1:
    st.selectbox(
        "Month",
        options=month_options,
        index=default_index,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("""
        <div class="hour-box">
            <span class="divider"></span>
            <span>12 h</span>
        </div>
    """, unsafe_allow_html=True)


# Row 2: Summary Statistics Box
st.markdown("""
    <div class="summary-box">
        <div class="summary-item">
            <span>合計就労日</span>
            <span class="value">12日</span>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-item">
            <span>合計時間</span>
            <span class="value">36 h</span>
        </div>
    </div>
""", unsafe_allow_html=True)


# List of Work Day Entries
work_days = [
    {"date": "5月1日 (水)", "time": "9:00~18:00"},
    {"date": "5月4日 (水)", "time": "9:00~18:00"},
    {"date": "5月6日 (水)", "time": "9:00~18:00"},
]

for day in work_days:
    st.markdown(f"""
        <div class="date-card">
            <div class="date">{day['date']}</div>
            <div class="time">{day['time']}</div>
        </div>
    """, unsafe_allow_html=True)


# Final Button
st.button("出力")