# mypy: ignore-errors
# flake8: noqa
import datetime
import logging
import time

import gspread
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import Config

logger = logging.getLogger(__name__)


class Connection:
    def __init__(self):
        self.credentials = Credentials.from_authorized_user_file(
            "utils/token.json", Config.scopes
        )
        # self.credentials = service_account.Credentials.from_service_account_file("../asera-dayreport-15c05cf58a1f.json", scopes=Config.scopes)
        # self.folder_id = Config.folder_id
        self.gc = gspread.authorize(self.credentials)
        self.service = build("drive", "v3", credentials=self.credentials)
        try:
            self.user = (
                self.service.about().get(fields="user").execute()["user"]["displayName"]
            )
        except Exception as e:
            print(f"ユーザ名の取得に失敗しました{e}")
            self.user = "unknown"

    def find_folder_by_name(self, name, folder_id=None):
        """現在の月のフォルダを探し存在した場合そのフォルダのidを返す"""
        try:
            if folder_id:
                result = (
                    self.service.files()
                    .list(
                        q=f"name='{name}' and '{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'",
                        fields="files(id,name)",
                    )
                    .execute()
                )
            else:
                result = (
                    self.service.files()
                    .list(
                        q=f"name='{name}' and mimeType='application/vnd.google-apps.folder'",
                        fields="files(id,name)",
                    )
                    .execute()
                )
            print(result.get("files", []))
            files = result.get("files", [])
            if files:
                print(f"ファイル{name}を発見しました")
                return files[0]["id"]
            else:
                print(f"ファイル{name}を発見できませんでした")
                return None

        except HttpError as error:
            logger.error(f"{name}のフォルダの検索に失敗しました: {error}")
            return None

    def find_spreadsheet(self, folder_id: str, name: str) -> str | None:
        """名前からその月のフォルダ内のスプレッドシートを取得"""
        try:
            query = f"name contains '{name}' and '{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet'"
            result = self.service.files().list(q=query).execute()
            file = result.get("files", [])
            if file:
                return file[0]["id"]
            return None
        except HttpError as error:
            logger.error(f"スプレッドシートが検索できません:{error}")
            return None

    def create_folder(self, name: str, parent_folder=None):
        """月のフォルダを作成、作成が成功したら作成したフォルダのidを返す"""
        try:
            if not parent_folder:
                folder_metadata = {
                    "name": name,
                    "mimeType": "application/vnd.google-apps.folder",
                }
            else:
                folder_metadata = {
                    "name": name,
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [parent_folder],
                }
            create_folder = (
                self.service.files()
                .create(body=folder_metadata, supportsAllDrives=True)
                .execute()
            )
            created_folder_id = create_folder["id"]
            # self.set_permission(month_folder_id,"月のフォルダ")

            print(f"フォルダ'{name}'が作成されました")
            return created_folder_id
        except HttpError as error:
            logger.error(f"フォルダ作成エラー: {error}")
            return None

    """始めはサービスアカウントを使用していたので権限設定をしていましたが今はoauth使ってるので不要"""
    # def set_permission(self, file_id: str, file_type: str):
    #     """フォルダ、ファイルのパーミッション設定"""
    #     try:
    #         permission = {
    #             'type': 'user',
    #             'role': 'owner',  # 'reader', 'writer', 'owner'から選択
    #             'emailAddress': Config.share_email
    #         }
    #         self.service.permissions().create(
    #             fileId=file_id,
    #             body=permission,
    #             sendNotificationEmail=False,
    #             supportsAllDrives=True,
    #             transferOwnership=True
    #         ).execute()
    #         print(f"{file_type}のパーミッション設定が完了しました。")
    #         return True
    #     except HttpError as error:
    #         logger.error(f"権限設定エラー: {error}")
    #         return False
