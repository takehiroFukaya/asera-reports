import streamlit as st

class Config:
    # Streamlit Secrets から OAuth 情報を取得
    google_oauth = st.secrets["google_oauth"]

    account_file = {
        "web": {
            "client_id": google_oauth["client_id"],
            "client_secret": google_oauth["client_secret"],
            "auth_uri": google_oauth["auth_uri"],
            "token_uri": google_oauth["token_uri"],
            "redirect_uris": google_oauth["redirect_uris"],
        }
    }

    scopes = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]

    # Flow 初期化時に使うリダイレクトURI
    redirect_uri = google_oauth["redirect_uris"][0]  # 配列の最初の URI を使用
