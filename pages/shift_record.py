import pandas as pd
import streamlit as st

from utils.functions import generate_month_options, time_to_hours
from utils.spreadsheet_updater import SpreadsheetUpdater

st.set_page_config(layout="centered")

st.markdown(
    """
<style>
    .stApp {
        background-color: #f0faf7;
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    .glass-effect {
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px); /* For Safari support */
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }

    .main .block-container {
        padding: 1.5rem 1rem 2rem 1rem;
        border-radius: 15px; 
        background: rgba(230, 242, 241, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    div[data-baseweb="select"] > div {
        border-radius: 10px;
        color: #859e99;
        font-size: 16px; 
        font-weight: 600;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .hour-box {
        display: flex;
        align-items: center;
        justify-content: center; 
        padding: 8px 12px;
        border-radius: 10px;
        height: 42px;
        font-size: 16px;
        font-weight: 600;
        color: #859e99;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .hour-box .divider {
        border-left: 1px solid #BDBDBD;
        height: 20px;
        margin: 0px 20px;
    }
    
    .summary-box {
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 12px;
        border-radius: 10px;
        margin: 1.5rem 0;
        font-size: 16px;
        font-weight: 600;
        color: #859e99;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .summary-item {
        display: flex;
        align-items: center;
        gap: 10px; 
    }
    .summary-item .value {
        color: #36a38c;
        font-weight: 600;
    }
    .summary-divider {
        border-left: 1px solid #E0E0E0;
        height: 24px;
    }

    .date-card {
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 1rem;
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .date-card .date {
        font-size: 16px;
        color: #85b4af;
        font-weight: 600;   
    }
    .date-card .time {
        font-size: 14px;
        color: #85b4af;
        font-weight: 600; 
        margin-top: 4px;
    }
    
    [data-testid="stDownloadButton"] {
        display: flex;
        justify-content: center;
    }
    [data-testid="stDownloadButton"] > button {
        width: 100%;
        background-color: #4DB6AC;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 14px 0;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-top: 1rem;
        transition: background-color 0.3s ease;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background-color: #26A69A;
        color: white;
        border: none;
    }
</style>
""",
    unsafe_allow_html=True,
)


# --- App Layout ---

updater = SpreadsheetUpdater()

# Row 1: Controls
col1, col2 = st.columns([1.5, 1])
month_options, default_index = generate_month_options()

with col1:
    selected_month = st.selectbox(
        "Month",
        options=month_options,
        index=default_index,
        label_visibility="collapsed",
    )


year, month = selected_month.replace("月", "").split("年")
df = updater.get_shift_record(f"{year}年{int(month)}")
status = getattr(updater, "last_status", {"ok": None})

over_cols = ["所定外1", "所定外2", "所定外3"]
if not df.empty and all(c in df.columns for c in over_cols):
    over_time = df[over_cols].applymap(time_to_hours).sum().sum()
else:
    over_time = 0.0
with col2:
    st.markdown(
        f"""
        <div class="hour-box">
            <span>所定外時間</span>
            <span class="divider"></span>
            <span>{over_time} h</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

if status.get("ok") is False:
    stage = status.get("stage")
    msg = status.get("detail", "")
    if stage in ("month_folder", "spreadsheet"):
        st.error(msg)
    elif stage == "empty":
        st.info(msg)
    else:
        st.warning(msg)

if df.empty:
    st.info("出勤簿の内容はなにもありません")

else:
    ## change
    numeric_cols = ["勤務時間"]

    total_time = df[numeric_cols].applymap(time_to_hours).sum().sum()  # '07:30' → 7.5
    total_days = len(df)

    # 2. summary card ------------------------------------------
    st.markdown(
        f"""
        <div class="summary-box">
            <div class="summary-item">
                <span>合計就労日</span>
                <span class="value">{total_days}日</span>
            </div>
            <div class="summary-divider"></div>
            <div class="summary-item">
                <span>合計時間</span>
                <span class="value">{total_time:.1f} h</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    ## change
    for _, row in df[["出勤日時", "退勤日時"]].iterrows():
        start_date, start_time = row["出勤日時"].split(" ")
        _, end_time = row["退勤日時"].split(" ")
        st.markdown(
            f"""
            <div class="date-card">
                <div class="date">{start_date}</div>
                <div class="time">{start_time}~{end_time}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
csv_bytes = df.to_csv(index=False).encode("utf-8-sig")  # Excel-friendly

downloaded = st.download_button(
    label="出力",  # same UI label
    data=csv_bytes,
    file_name=f"{updater.connection.user}_{year}年{int(month)}月_日報.csv",
    mime="text/csv",
)

# If the user clicked the download button, then navigate
if downloaded:
    st.switch_page("pages/billing_list.py")
