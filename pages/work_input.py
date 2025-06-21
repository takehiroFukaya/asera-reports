import streamlit as st
import datetime

st.set_page_config(
    page_title="作業登録",
    layout="centered",
)

st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background-color: #f0f2f6;
    background-image: linear-gradient(to right bottom, #c3d4e3, #dbe4ee, #f3f5f9, #ffffff, #ffffff);
}
[data-testid="stBlockContainer"] {
    background: transparent;
}
[data-testid="stHorizontalBlock"] {
    background: transparent;
}
[data-testid="stDateInput"] input {
    background: rgba(255, 255, 255, 0.25);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 10px;
    color: #333;
    padding-right: 35px !important;
}
[data-testid="stForm"] {
    background-color: #E0F2F1;
    border-radius: 10px;
    padding: 25px;
    border: 1px solid #B2DFDB;
}
[data-testid="stDateInput"] {
    position: relative;
}
[data-testid="stDateInput"]::after {
    content: ' ';
    display: block;
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    width: 20px;
    height: 20px;
    pointer-events: none;
    background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="%23555555" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>');
    background-repeat: no-repeat;
    background-position: center;
}
[data-testid="stFormSubmitButton"] {
    display: flex;
    justify-content: center;
}
[data-testid="stFormSubmitButton"] button {
    width: 60%;
    color: white;
    font-weight: bold;
    border: none;
    padding: 10px 0px;
    border-radius: 5px;
    background-image: linear-gradient(to right, #00897B, #00695C);
    transition: all 0.3s ease-in-out;
}
[data-testid="stFormSubmitButton"] button:hover {
    background-image: linear-gradient(to right, #009688, #00897B);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    cursor: pointer;
}
.time-separator {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 5px;
    padding-top: 28px;
    font-weight: bold;
    font-size: 100px;
}
</style> 
""", unsafe_allow_html=True)


col1, col2 = st.columns([3, 1])
with col1:
    work_date = st.date_input("<UNK>",datetime.date.today(), label_visibility="collapsed")

st.markdown("<h3>作業実績入力</h3>", unsafe_allow_html=True)

with st.form(key="work_form"):
    t_col1, t_col2, t_col3 = st.columns([2, 0.5, 2])
    with t_col1:
        start_time = st.time_input("開始時間", label_visibility="collapsed")
    with t_col2:
        st.markdown("<p class='time-separator'>~</p>", unsafe_allow_html=True)
    with t_col3:
        end_time = st.time_input( "終了時間", label_visibility="collapsed")
    work_category = st.selectbox(
        "**作業カテゴリー**", options=["開発", "ミーティング", "資料作成", "その他"],
    )
    work_client = st.selectbox(
        "**請求先**", options=["A社", "B社", "自社"],
    )
    work_content = st.text_area("**作業内容**")
    st.write("**納品物**")
    d_col1, d_col2 = st.columns([3, 1])
    with d_col1:
        deliverable_item = st.text_input("納品物名", label_visibility="collapsed")
    with d_col2:
        deliverable_quantity = st.number_input("数量", value=1, min_value=1, step=1, label_visibility="collapsed")
    amount = st.number_input("**金額**", min_value=0, step=1000)
    submit_button = st.form_submit_button(label="登録")

if submit_button:
    st.success("作業記録を登録しました！")
    st.write("---")
    st.write("### 登録内容")
    st.write(f"**日付:** {work_date}")
    st.write(f"**作業時間:** {start_time} ~ {end_time}")
    st.write(f"**カテゴリー:** {work_category}")
    st.write(f"**請求先:** {work_client}")
    st.write(f"**作業内容:**")
    st.info(work_content)
    st.write(f"**納品物:** {deliverable_item} (数量: {deliverable_quantity})")
    st.write(f"**金額:** ¥{amount:,}")