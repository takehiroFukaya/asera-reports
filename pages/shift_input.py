import streamlit as st
import datetime

st.set_page_config(
    page_title="作業登録",
    layout="centered",
)

st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
   background-color: #f0faf7;
}

[data-testid="stBlockContainer"],
[data-testid="stHorizontalBlock"] {
    background: transparent;
}

[data-testid="stForm"] input,
[data-testid="stForm"] textarea,
[data-testid="stForm"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #333 !important; 
}


[data-testid="stDateInput"] input {
    background-color: #FFFFFF !important;
    border: 1px solid #ccc;
    border-radius: 10px;
}

[data-testid="stForm"] {
    background-color: #E0F2F1;
    border-radius: 10px;
    padding: 25px;
    border: 1px solid #B2DFDB;
}

/* Calendar icon styling (no change) */
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
    width: 50%;
    margin-top: 10px;
    color: white;
    font-weight: bold;
    border: none;
    padding: 10px 0px;
    border-radius: 8px;
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
    height: 38px; 
    padding-top: 8px;
    font-weight: bold;
    font-size: 40px; 
}
</style> 
""", unsafe_allow_html=True)


col1, col2 = st.columns([3, 1])
with col1:
    work_date = st.date_input("Date", datetime.date.today(), label_visibility="collapsed")


with st.form(key="shift_form"):
    t_col1, t_col2, t_col3 = st.columns([2, 0.5, 2])
    with t_col1:
        start_time = st.time_input("開始時間", label_visibility="collapsed")
    with t_col2:
        st.markdown("<p class='time-separator'>~</p>", unsafe_allow_html=True)
    with t_col3:
        end_time = st.time_input( "終了時間", label_visibility="collapsed")

    work_content = st.text_area("**作業内容**")
    submit_button = st.form_submit_button(label="登録")

if submit_button:
    st.success("作業記録を登録しました！")
    st.write("---")
    st.write("### 登録内容")
    st.write(f"**日付:** {work_date}")
    st.write(f"**作業時間:** {start_time} ~ {end_time}")
    st.write(f"**作業内容:**")
    st.info(work_content)