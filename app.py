import asyncio

import streamlit as st

from utils.login import Login
from utils.setup_folder import SetupFolder


async def initialize_spreadsheet():
    login = Login()
    credentials = login.authenticate()
    if credentials:
        setup = SetupFolder()
        setup.setup()
        return True
    else:
        print("認証が失敗しました")
        return False


st.title("日報アプリ")

with st.spinner("読み込み中..."):
    auth_success = asyncio.run(initialize_spreadsheet())


if auth_success:
    st.switch_page("pages/top.py")
else:
    st.info("認証を完了してください。")
