# login.py
import streamlit as st
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from config import Config


class Login:
    def __init__(self):
        self.scopes = Config.scopes

        # セッション初期化
        if "credentials" not in st.session_state:
            st.session_state.credentials = None
        if "oauth_state" not in st.session_state:
            st.session_state.oauth_state = None
        if "oauth_states" not in st.session_state:   # ▼ 直近のstateを複数保持して古いリンク対策
            st.session_state.oauth_states = []
        if "flow" not in st.session_state:
            st.session_state.flow = None
        if "login_in_progress" not in st.session_state:  # ▼ 多重押下ガード
            st.session_state.login_in_progress = False

    def get_credentials(self):
        """セッション状態から認証情報を取得または新規認証"""
        if 'credentials' not in st.session_state:
            st.session_state.credentials = None

        if st.session_state.credentials:
            creds = Credentials.from_authorized_user_info(
                st.session_state.credentials, self.scopes
            )

            if creds.valid:
                return creds

            if creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    st.session_state.credentials = json.loads(creds.to_json())
                    return creds
                except Exception as e:
                    st.error(f"トークンの更新に失敗しました: {e}")
                    st.session_state.credentials = None
        return None

    def authenticate(self):
        """認証フローを実行"""
        st.subheader("🔐 アカウント認証")
        query_params = st.query_params

        # コールバック処理
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
                        st.session_state.oauth_state = None  # ★ログアウト時にstateも破棄
                        st.session_state.oauth_states = []    # ▼ 複数state履歴も破棄
                        st.session_state.flow = None          # ★ログアウト時にflowも破棄
                        st.session_state.login_in_progress = False
                        st.rerun()
                return creds

            except Exception as e:
                st.error(f"認証情報の検証に失敗しました: {e}")
                st.session_state.credentials = None
                return None

        else:
            # 未認証
            st.warning("Googleアカウントでの認証が必要です")

            if st.button("🚀 Googleでログイン", disabled=st.session_state.login_in_progress):
                try:
                    st.session_state.login_in_progress = True  # ▼ 多重押下ガードON

                    # フロー生成
                    flow = Flow.from_client_config(
                        Config.account_file,
                        self.scopes,
                        redirect_uri=Config.redirect_uri
                    )

                    # 認証URL生成
                    auth_url, state = flow.authorization_url(
                        access_type='offline',
                        include_granted_scopes='true',
                        prompt='consent'
                    )

                    # ★state をセッションに先に保存
                    st.session_state.oauth_state = state
                    st.session_state.flow = flow

                    # ▼ 直近stateを履歴に（古いリンク踏み対策：最大3件）
                    states = st.session_state.oauth_states
                    states.append(state)
                    st.session_state.oauth_states = states[-3:]

                    st.markdown(f"### 🔗 [こちらをクリックして認証してください]({auth_url})")
                    st.info("認証後、このページに自動的に戻ります")

                except Exception as e:
                    st.error(f"認証フローの初期化に失敗しました: {e}")
                    st.session_state.login_in_progress = False
            return None

    def handle_callback(self):
        """認証コールバックを処理"""
        query_params = st.query_params

        if 'code' in query_params:
            # ▼ list / str 混在対策: 最初の要素を使う
            def _first(v):
                if isinstance(v, list):
                    return v[0]
                return v

            auth_code = _first(query_params.get('code'))
            state = _first(query_params.get('state'))

            # ★state 比較
            expected_state = st.session_state.get('oauth_state')
            recent_states = st.session_state.get('oauth_states', [])
            if not expected_state or (state != expected_state and state not in recent_states):
                exp_len = len(expected_state) if expected_state else 0  # ▼ デバッグ補助（長さのみ）
                got_len = len(state) if state else 0
                st.error(f"認証エラー: 無効な状態パラメータ（expected:{exp_len} chars / got:{got_len} chars）")
                st.session_state.login_in_progress = False
                return None

            try:
                # ★セッションの flow を使う
                flow = st.session_state.get('flow')
                if not flow:
                    st.error("認証フローが見つかりません。再度ログインしてください。")
                    st.session_state.login_in_progress = False
                    return None

                flow.fetch_token(code=auth_code)
                st.session_state.credentials = json.loads(flow.credentials.to_json())

                # 一時情報を破棄
                st.session_state.oauth_state = None
                st.session_state.oauth_states = []
                st.session_state.flow = None
                st.session_state.login_in_progress = False

                # URL パラメータをクリアしてリロード
                st.query_params.clear()
                st.success("🎉 認証が完了しました！")
                st.rerun()

            except Exception as e:
                st.session_state.login_in_progress = False
                st.error(f"認証に失敗しました: {e}")
