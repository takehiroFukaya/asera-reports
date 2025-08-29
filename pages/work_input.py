import streamlit as st
import datetime
import pytz
from utils.functions import round_time_to_fifteen_min

from utils.spreadsheet_updater import SpreadsheetUpdater

st.set_page_config(
    page_title="作業登録",
    layout="centered",
)


def add_deliverable():
    new_id = max(item["id"] for item in st.session_state["deliverables"]) + 1
    st.session_state["deliverables"].append(
        {"id": new_id, "deliverable_item": "", "deliverable_quantity": 0, "amount": 0}
    )


def delete_deliverable(target):
    st.session_state["deliverables"] = [
        item for item in st.session_state["deliverables"] if item["id"] != target
    ]


st.markdown(
    """
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

[data-testid="stForm"] {
    background-color: #E0F2F1;
    border-radius: 10px;
    padding: 25px;
    border: 1px solid #B2DFDB;
}

[data-testid="stDateInput"] input {
    background-color: #FFFFFF !important;
    border: 1px solid #ccc; 
    border-radius: 10px;
}

[data-testid="stDateInput"] {
    background: none !important;
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
    background-color: #26A69A; 
    transition: all 0.3s ease-in-out;
}
[data-testid="stFormSubmitButton"] button:hover {
    background-image: linear-gradient(to right, #009688, #00897B);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    cursor: pointer;
    color: white;
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
""",
    unsafe_allow_html=True,
)


col1, col2 = st.columns([3, 1])
with col1:
    work_date = st.date_input(
        "Date", datetime.date.today(), label_visibility="collapsed"
    )

st.markdown("<h3>作業実績入力</h3>", unsafe_allow_html=True)

if "updater" not in st.session_state:
    st.session_state["updater"] = SpreadsheetUpdater()

updater = st.session_state["updater"]

if "deliverables" not in st.session_state:
    st.session_state["deliverables"] = [
        {"id": 0, "deliverable_item": "", "deliverable_quantity": 0, "amount": 0}
    ]


delete_button = {}
deliverable_data = []
now_time = round_time_to_fifteen_min(datetime.datetime.now(pytz.timezone('Asia/Tokyo')))
with st.form(key="work_form"):
    t_col1, t_col2, t_col3 = st.columns([2, 0.5, 2])
    with t_col1:
        start_time = st.time_input("開始時間", now_time, label_visibility="collapsed")
    with t_col2:
        st.markdown("<p class='time-separator'>~</p>", unsafe_allow_html=True)
    with t_col3:
        end_time = st.time_input("終了時間", now_time ,label_visibility="collapsed")
    work_category = st.selectbox(
        "**作業カテゴリー**",
        options=["社内業務","セットアップ","備品設置","保守","システム開発","その他"],
    )
    work_client = st.selectbox(
        "**請求先**",
        options=["東信","明誠","ナマコン","石産"],
    )
    work_content = st.text_area("**作業内容**")
    for item in st.session_state["deliverables"]:
        item_id = item["id"]
        st.write("**納品物**")
        d_col1, d_col2 = st.columns([3, 1])
        with d_col1:
            deliverable_item = st.text_input(
                "納品物名",
                label_visibility="collapsed",
                key=f"deliverable_item_{item_id}",
            )
        with d_col2:
            deliverable_quantity = st.number_input(
                "数量",
                value=1,
                min_value=1,
                step=1,
                label_visibility="collapsed",
                key=f"deliverable_quantity_{item_id}",
            )
        unit_price = st.number_input(
            "**単価**", min_value=0, step=1000, key=f"unit_price_{item_id}"
        )

        deliverable_data.append(
            {
                "date": datetime.datetime.combine(work_date, start_time),
                "deliverable_item": deliverable_item,
                "deliverable_quantity": deliverable_quantity,
                "unit_price": unit_price
            }
        )

    col_add, col_delete = st.columns([1, 1])

    with col_add:
        add_button = st.form_submit_button("追加", type="secondary")

    with col_delete:
        if len(st.session_state["deliverables"]) > 1:
            delete_button = st.form_submit_button("削除", type="secondary")
        else:
            delete_button = False

    submit_button = st.form_submit_button(label="登録")


if add_button:
    add_deliverable()
    st.rerun()
elif delete_button:
    delete_deliverable(max(item["id"] for item in st.session_state["deliverables"]))
    st.rerun()
elif submit_button:
    start_datetime = datetime.datetime.combine(work_date, start_time)
    end_datetime = datetime.datetime.combine(work_date, end_time)

    duration = end_datetime - start_datetime
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    time_spent_display = f"{hours:02d}:{minutes:02d}"

    if not all([work_date, start_time, end_time, work_content]):
        st.error(
            "全ての必須項目（日付、時間、カテゴリー、請求先、作業内容）を入力してください。"
        )
    elif start_time >= end_time:
        st.error("終了時間は開始時間より遅い時間を選択してください。")
    else:
        if not deliverable_item:
            success = updater.add_work_report(
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                work_category=work_category,
                work_content=work_content,
                work_client=work_client,
            )
        else:
            success = updater.add_work_report(
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                work_category=work_category,
                work_content=work_content,
                work_client=work_client,
                deliverables=deliverable_data,
            )

        if success:
            st.success("✅ 作業記録を正常に登録しました！")
            st.write("---")
            st.write("### 登録内容")
            st.write(f"**日付:** {work_date}")
            st.write(
                f"**作業時間:** {start_time.strftime('%H:%M')} ~ {end_time.strftime('%H:%M')} (合計: {time_spent_display})"
            )
            st.write(f"**カテゴリー:** {work_category if work_category else '未選択'}")
            st.write(f"**請求先:** {work_client if work_client else '未選択'}")
            st.write(f"**作業内容:**")
            st.info(work_content)
            for item in deliverable_data:
                st.write(
                    f"**納品物:** {item["deliverable_item"]} (数量: {item["deliverable_quantity"]})"
                )
                st.write(f"**単価:** ¥{item["unit_price"]}")
        else:
            st.error(
                "❌ 作業記録の登録に失敗しました。詳細はアプリケーションのログを確認してください。"
            )
