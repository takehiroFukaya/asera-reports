import datetime
import logging
import time

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

folder_id = Config.folder_id

scopes = Config.scopes

credentials = Credentials.from_service_account_file(
    Config.service_account_file,
    scopes=scopes,
)

def main():
    connect_gspread()


def connect_gspread():
    gc = gspread.authorize(credentials)
    service = build("drive", "v3", credentials=credentials)

    now_month = str(datetime.datetime.now().month)

    try:
        result = service.files().list(q=f"name='{now_month}' and '{folder_id}' in parents").execute()

        print(result.get('files', []))

        """ その月のファイルがあるかどうかを確認する。なかった場合ファイルを作成して作成したファイルの中にスプレッドシートを作成する """
        if not result.get('files', []):
            print("ファイルないよー")
            folder_metadata = {
                'name': now_month,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [folder_id]
            }
            create_folder = service.files().create(body=folder_metadata).execute()
            month_folder_id = create_folder['id']
            permission = {
                'type': 'user',
                'role': 'writer',  # 'reader', 'writer', 'owner'から選択
                'emailAddress': 'aseratkyn@gmail.com'
            }
            service.permissions().create(
                fileId=month_folder_id,
                body=permission,
                sendNotificationEmail=False
            ).execute()
            set_permission(service,month_folder_id,"フォルダ")
            print(f"フォルダ '{now_month}' が作成されました。ID: {create_folder['id']}")

            time.sleep(3)
            create_daily_report_spreadsheet(gc, service, month_folder_id, now_month)
            create_work_report_spreadsheet(gc, service, month_folder_id, now_month)

        else:
            for file in result.get("files", []):
                month_folder_id = file.get("id")
            print("ファイルあるよー")
            print(month_folder_id)
    except HttpError as error:
        logger.error(f"Google Drive API エラー: {error}")
    except Exception as error:
        logger.error(f"予期しないエラー: {error}")

def set_permission(service, file_id, file_type):
    """パーミッション設定"""
    try:
        permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': 'aseratkyn@gmail.com'
        }


        service.permissions().create(
            fileId=file_id,
            body=permission,
            sendNotificationEmail=False,
            supportsAllDrives=True
        ).execute()

        logger.info(f"{file_type}の権限設定が完了しました")

    except HttpError as error:
        logger.error(f"権限設定エラー: {error}")





def create_work_report_spreadsheet(gc, service, folder_id, month_name):
    """作業内容用スプレッドシートを作成する"""
    try:
        """ スプレッドシートのメタデータ"""
        spreadsheet_metadata = {
            'name': f'TTTTT_{month_name}月_作業内容',
            'parents': [folder_id],
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'description': f'{month_name}月の日報管理用スプレッドシート'
        }
        """スプレッドシートを作成"""
        spreadsheet = service.files().create(body=spreadsheet_metadata).execute()
        spreadsheet_id = spreadsheet['id']
        """権限設定"""
        set_permission(service, spreadsheet_id, "作業内容ファイル")

        """スプレッドシートを開いてヘッダーを設定"""
        sheet = gc.open_by_key(spreadsheet_id)
        worksheet = sheet.sheet1
        # ヘッダー行を設定
        headers = [
            "作業開始日時",
            "作業終了日時",
            "作業場所",
            "作業種別",
            "作業内容",
            "作業時間",
            "請求先",
            "登録者"
        ]

        """項目を一行目に追加"""
        worksheet.update(values=[headers], range_name='A1:H1')
        """ヘッダー行のフォーマット設定"""
        worksheet.format('A1:H1', {
            "backgroundColor": {
                "red": 0.8,
                "green": 0.8,
                "blue": 0.8
            },
            "textFormat": {
                "bold": True
            }
        })

        print(f"スプレッドシート '{month_name}月_作業内容' が作成されました。ID: {spreadsheet_id}")
        return spreadsheet_id
    except HttpError as error:
        logger.error(f"スプレッドシート作成エラー: {error}")
        return None
    except Exception as error:
        logger.error(f"予期しないエラー: {error}")
        return None

def create_daily_report_spreadsheet(gc, service, folder_id, month_name):
    """日報用スプレッドシートを作成する"""
    try:
        """ スプレッドシートのメタデータ"""
        spreadsheet_metadata = {
            'name': f'TTTTT_{month_name}月_日報',
            'parents': [folder_id],
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'description': f'{month_name}月の日報管理用スプレッドシート'
        }
        """スプレッドシートを作成"""
        spreadsheet = service.files().create(body=spreadsheet_metadata).execute()
        spreadsheet_id = spreadsheet['id']
        """権限設定"""
        set_permission(service, spreadsheet_id, "日報ファイル")

        """スプレッドシートを開いてヘッダーを設定"""
        sheet = gc.open_by_key(spreadsheet_id)
        worksheet = sheet.sheet1
        # ヘッダー行を設定
        headers = [
            "出勤日時",
            "退勤日時",
            "休憩開始時間",
            "休憩終了時間",
            "休憩時間",
            "勤務時間",
            "備考欄"
        ]

        """項目を一行目に追加"""
        worksheet.update(values=[headers], range_name='A1:H1')
        """ヘッダー行のフォーマット設定"""
        worksheet.format('A1:G1', {
            "backgroundColor": {
                "red": 0.8,
                "green": 0.8,
                "blue": 0.8
            },
            "textFormat": {
                "bold": True
            }
        })

        print(f"スプレッドシート '{month_name}月_日報' が作成されました。ID: {spreadsheet_id}")
        return spreadsheet_id
    except HttpError as error:
        logger.error(f"スプレッドシート作成エラー: {error}")
        return None
    except Exception as error:
        logger.error(f"予期しないエラー: {error}")
        return None

def create_daily_report_spreadsheet(gc, service, folder_id, month_name):
    """出勤簿用スプレッドシートを作成する"""
    try:
        """ スプレッドシートのメタデータ"""
        spreadsheet_metadata = {
            'name': f'TTTTT_{month_name}月_出勤簿',
            'parents': [folder_id],
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'description': f'{month_name}月の日報管理用スプレッドシート'
        }
        """スプレッドシートを作成"""
        spreadsheet = service.files().create(body=spreadsheet_metadata).execute()
        spreadsheet_id = spreadsheet['id']
        """権限設定"""
        set_permission(service, spreadsheet_id, "出勤簿ファイル")

        """スプレッドシートを開いてヘッダーを設定"""
        sheet = gc.open_by_key(spreadsheet_id)
        worksheet = sheet.sheet1
        # ヘッダー行を設定
        headers = [
            "出勤日時",
            "退勤日時",
            "休憩開始時間",
            "休憩終了時間",
            "休憩時間",
            "勤務時間",
            "備考欄"
        ]

        """項目を一行目に追加"""
        worksheet.update(values=[headers], range_name='A1:H1')
        """ヘッダー行のフォーマット設定"""
        worksheet.format('A1:G1', {
            "backgroundColor": {
                "red": 0.8,
                "green": 0.8,
                "blue": 0.8
            },
            "textFormat": {
                "bold": True
            }
        })

        print(f"スプレッドシート '{month_name}月_日報' が作成されました。ID: {spreadsheet_id}")
        return spreadsheet_id
    except HttpError as error:
        logger.error(f"スプレッドシート作成エラー: {error}")
        return None
    except Exception as error:
        logger.error(f"予期しないエラー: {error}")
        return None




if __name__ == "__main__":
    main()



