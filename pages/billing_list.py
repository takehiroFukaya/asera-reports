import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="Work Log",
    page_icon="📋",
    layout="centered"
)


def load_css():
    css = """
    <style>
        .stApp {
            background-color: #f0faf7;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        [data-testid="stSelectbox"] {
            border-radius: 16px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px); /* For Safari compatibility */
            background: rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        }
        [data-testid="stSelectbox"] > div[data-baseweb="select"] > div {
            background-color: transparent;
            border: none;
        }

        [data-testid="stDataFrame"] {
            background-color: transparent; 
            border: none;
            overflow-x: auto;
            overflow-y: auto;
            max-height: 60vh;
            width: 100%;
            -webkit-overflow-scrolling: touch;
            touch-action: pan-x pan-y;
        }
        [data-testid="stDataFrame"] thead {
            display: inline-block;
        }

        [data-testid="stDataFrame"] tbody td {
            display: inline-block;
            border: none;
            padding: 10px 5px;
            color: #37474F;
        }
        [data-testid="stDataFrame"] tbody tr:nth-child(even) {
            background-color: transparent;
        }

        .total-card {
            border-radius: 16px; 
            padding: 15px 20px;
            display: flex;
            margin-bottom: 40px;
            justify-content: space-between;
            font-weight: bold;
            color: #263238; 
            font-size: 1.1em;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px); /* For Safari compatibility */
            background: rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        }


        [data-testid="stDownloadButton"] {
            display: flex;
            justify-content: center;
        }

        [data-testid="stDownloadButton"] > button {
            width: 50%;
            margin-top: auto;
            margin-bottom: 2rem;
            font-weight: bold;
            border: none;
            padding: 10px 0px;
            border-radius: 8px;
            transition: all 0.3s ease-in-out;
            text-decoration: none;
            text-align: center;
            display: flex;
            color: white !important;
            background-image: linear-gradient(to right, #00897B, #00695C) !important;
        }

        [data-testid="stDownloadButton"] > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            cursor: pointer;
            text-decoration: none;
            color: white !important;
            background-image: linear-gradient(to right, #009688, #00897B) !important;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


import datetime


def generate_month_options():
    options = []
    today = datetime.date.today()
    current_year = today.year
    current_month = today.month

    for year in range(current_year, current_year - 6, -1):
        start_month = current_month if year == current_year else 12

        for month in range(start_month, 0, -1):
            month_str = f"{year}年{month}月"
            options.append(month_str)

    default_value = f"{current_year}年{current_month}月"
    default_index = options.index(default_value)

    return (options, default_index)

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='WorkLog')
    processed_data = output.getvalue()
    return processed_data

load_css()

data = {
    "日付":      ["2025-06-01", "2025-06-04", "2025-06-06", ],
    "勤務時間":  ["9:00~18:00", "9:00~12:00", "9:00~12:00"],
    "業務内容":  ["コード修正",     "コード修正",     "コード修正"],
    "請求先":    ["株式会社A",     "株式会社B",     "株式会社A"],
    "納品物":    ["仕様書",         "テスト結果",     "仕様書"],
    "金額":      [50000,           20000,           20000],
}
df = pd.DataFrame(data)
total_hours = 12
total_amount = df["金額"].sum()

month_options, default_month_index = generate_month_options()

selected_month = st.selectbox(
    label="Select Month",
    options=month_options,
    index=default_month_index,
    label_visibility="collapsed"
)
st.write("")  # Spacer

st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown(f"""
<div class="total-card">
    <span>合計</span>
    <span>{total_hours} 時間</span>
</div>
""", unsafe_allow_html=True)

excel_data = to_excel(df)

st.download_button(
    label="出力",
    data=excel_data,
    file_name="work_log.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
