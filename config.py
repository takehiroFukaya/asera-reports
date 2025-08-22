import os
import streamlit as st

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()


class Config:
    # folder_id = os.environ.get('DEFALUT_FOLDER_ID')
    account_file = {
                        "web": {
                            "client_id": st.secrets["google_oauth"]["client_id"],
                            "client_secret": st.secrets["google_oauth"]["client_secret"],
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "redirect_uris": st.secrets["google_oauth"]["redirect_uris"]
                        }
                    }

    scopes = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]
    share_email = ["aseratkyn@gmail.com"]
    redirect_uri = st.secrets["redirect_uri"]
