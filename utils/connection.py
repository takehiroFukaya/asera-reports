import datetime
import logging
import time

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import Config

logger = logging.getLogger(__name__)



class Connection:
    def __init__(self):
        self.credentials = Credentials.from_service_account_file(
            Config.service_account_file,scopes=Config.scopes
        )
        self.folder_id = Config.folder_id
        self.gc = gspread.authorize(self.credentials)
        self.service = build("drive", "v3", credentials=self.credentials)


    def find_monthly_folder(self,now_month):
        """現在の月のフォルダを探し存在した場合そのフォルダのidを返す"""
        try:
            result = self.service.files().list(q=f"name='{now_month}' and '{self.folder_id}' in parents").execute()
            print(result.get('files', []))
            files = result.get('files', [])
            if files:
                return files[0]['id']
            else:
                return None

        except HttpError as error:
            logger.error(f"今月のフォルダの検索に失敗しました: {error}")
            return None

    def create_folder(self,now_month:str):
        """月のフォルダを作成、作成が成功したら作成したフォルダのidを返す"""
        try:
            folder_metadata = {
                'name': now_month,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [self.folder_id]
            }
            create_folder = self.service.files().create(body=folder_metadata).execute()
            month_folder_id = create_folder['id']
            self.set_permission(month_folder_id,"月のフォルダ")

            print(f"フォルダ'{now_month}'が作成されました")
            return month_folder_id
        except HttpError as error:
            logger.error(f"フォルダ作成エラー: {error}")
            return None

    def update_file(self, file_id: str):
        return file_id


    def set_permission(self, file_id: str, file_type: str):
        """フォルダ、ファイルのパーミッション設定"""
        try:
            permission = {
                'type': 'user',
                'role': 'writer',  # 'reader', 'writer', 'owner'から選択
                'emailAddress': Config.share_email
            }
            self.service.permissions().create(
                fileId=file_id,
                body=permission,
                sendNotificationEmail=False,
                supportsAllDrives=True
            ).execute()
            print(f"{file_type}のパーミッション設定が完了しました。")
            return True
        except HttpError as error:
            logger.error(f"権限設定エラー: {error}")
            return False



