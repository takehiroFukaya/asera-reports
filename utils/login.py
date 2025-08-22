# streamlit_auth.py
import streamlit as st
import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from config import Config


class Login:
    def __init__(self):
        self.scopes = Config.scopes

    def get_credentials(self):
        """セッション状態から認証情報を取得または新規認証"""

        if 'credentials' not in st.session_state:
            st.session_state.credentials = None

        # 既存の認証情報をチェック
        if st.session_state.credentials:
            creds = Credentials.from_authorized_user_info(
                st.session_state.credentials, self.scopes
            )

            if creds.valid:
                return creds

            # 期限切れの場合、リフレッシュ
            if creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    # 更新された認証情報をセッションに保存
                    st.session_state.credentials = json.loads(creds.to_json())
                    return creds
                except Exception as e:
                    st.error(f"トークンの更新に失敗しました: {e}")
                    st.session_state.credentials = None

        # 新規認証が必要
        return None

    def authenticate(self):
        """認証フローを実行"""
        st.subheader("🔐アカウント認証")

        # コールバック処理
        query_params = st.query_params
        if 'code' in query_params:
            return self.handle_callback()

        creds = self.get_credentials()


        if creds:
            # 認証済み
            try:
                service = build("drive", "v3", credentials=creds)
                user_info = service.about().get(fields="user").execute()
                user_name = user_info["user"]["displayName"]

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.success(f"✅ ログイン中: {user_name}")
                with col2:
                    if st.button("ログアウト"):
                        st.session_state.credentials = None
                        st.rerun()
                print("4")
                return creds

            except Exception as e:
                st.error(f"認証情報の検証に失敗しました: {e}")
                st.session_state.credentials = None
                return None

        else:
            # 未認証
            st.warning("Googleアカウントでの認証が必要です")

            if st.button("🚀 Googleでログイン"):
                try:
                    flow = Flow.from_client_config(
                        Config.account_file, self.scopes
                    )


                    # 認証URLを生成
                    auth_url, state = flow.authorization_url(
                        access_type='offline',
                        include_granted_scopes='true',
                        prompt='consent'
                    )
                    st.session_state.flow = flow
                    st.session_state.oauth_state = state

                    # 認証URLを表示
                    st.markdown(f"### 🔗 [こちらをクリックして認証してください]({auth_url})")
                    st.info("認証後、このページに自動的に戻ります")


                except Exception as e:
                    st.error(f"認証フローの初期化に失敗しました: {e}")
                    return None
            print("8")


            return None

    def handle_callback(self):
        """認証コールバックを処理"""
        # URLパラメータから認証コードを取得
        query_params = st.query_params

        if 'code' in query_params:
            auth_code = query_params['code']
            state = query_params.get('state')


            # CSRF チェック
            if state != st.session_state.get('oauth_state'):
                st.error("認証エラー: 無効な状態パラメータ")
                return None

            try:
                # 新しいフローを作成してトークンを取得
                flow = Flow.from_client_config(
                    Config.account_file,
                    self.scopes,
                    redirect_uri= Config.redirect_uri
                )

                # 認証コードでトークンを取得
                flow.fetch_token(code=auth_code)

                # 認証情報を保存
                st.session_state.credentials = json.loads(flow.credentials.to_json())

                # URLパラメータをクリア
                st.query_params.clear()
                st.success("🎉 認証が完了しました！")
                st.rerun()

            except Exception as e:
                st.error(f"認証に失敗しました: {e}")
