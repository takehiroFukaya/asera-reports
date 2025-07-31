import streamlit as st
from utils.functions import *
from utils.spreadsheet_updater import SpreadsheetUpdater

st.set_page_config(
    page_title="Work Log",
    page_icon="📋",
    layout="wide"
)


def load_css():
    css = """
    <style>
        .stApp {
            background-color: #f0faf7;
            min-height: 100vh;
            display: flex;
            flex-direction: row;
        }
        .back-button-link {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 42px;
            width: 42px; 
            border-radius: 12px;
            text-decoration: none;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
        }
        .back-button-link:hover {
            background: rgba(255, 255, 255, 0.8); /* Slightly more opaque on hover */
        }
        .back-button-link svg {
            stroke: #263238; /* Icon color */
            stroke-width: 2.5;
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
        [data-testid="column"] {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
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
            background-color: #26A69A; 
        }

        [data-testid="stDownloadButton"] > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            cursor: pointer;
            text-decoration: none;
            color: white !important;
            background-image: linear-gradient(to right, #009688, #00897B) !important;
        }

        @media (max-width: 680px) {
        
        [data-testid="column"] {

        }
        
        [data-testid="stSelectbox"]  {
           max-width: 350px;
        }
           
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


load_css()
# #
# # data = {
# #     "日付": ["2025-06-01", "2025-06-04", "2025-06-06", ],
# #     "勤務時間": ["9:00~18:00", "9:00~12:00", "9:00~12:00"],
# #     "業務内容": ["コード修正", "コード修正", "コード修正"],
# #     "請求先": ["株式会社A", "株式会社B", "株式会社A"],
# #     "納品物": ["仕様書", "テスト結果", "仕様書"],
# #     "金額": [50000, 20000, 20000],
# # }
# # df = pd.DataFrame(data)
# # total_hours = 12
# total_amount = df["金額"].sum()



month_options, default_month_index = generate_month_options()
col1, col2 = st.columns([0.4, 0.6])

with col1:
    st.markdown("""
        <a href="/" target="_self" class="back-button-link">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
        </a>
    """, unsafe_allow_html=True)

with col2:
    selected_month = st.selectbox(
        label="Select Month",
        options=month_options,
        index=default_month_index,
        label_visibility="collapsed"
    )

st.write("")  # Spacer
updater = SpreadsheetUpdater()
month = selected_month.replace("月", "")
df = updater.get_work_logs(month)
total_hours = len(df) * 3
total_amount = df["金額"].sum()

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