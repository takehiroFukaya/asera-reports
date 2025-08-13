import asyncio

import streamlit as st

from utils.login import Login
from utils.setup_folder import SetupFolder


async def initialize_spreadsheet():
    Login()
    setup = SetupFolder()
    setup.setup()


st.title("日報アプリ")

with st.spinner("読み込み中..."):
    asyncio.run(initialize_spreadsheet())


st.switch_page("pages/top.py")
