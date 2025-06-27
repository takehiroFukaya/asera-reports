import logging
from typing import Optional

from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class SpreadsheetCreator:
    def __init__(self, connection):
        self.connection = connection
        self.gc = connection.gc
        self.service = connection.service

    def create_work_report_spreadsheet(self, folder_id: str, month_name: str) -> str | None:
        """作業内容"""
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

        return self.create_spreadsheet(
            folder_id=folder_id,
            name=f'TTTTT_{month_name}月_作業内容',
            description=f'{month_name}月の作業内容用スプレッドシート',
            headers=headers,
            sheet_type="作業内容ファイル"
        )

    def create_daily_report_spreadsheet(self, folder_id: str, month_name: str) -> str | None:
        """日報用スプレッドシートを作成する"""
        headers = [
            "出勤日時",
            "退勤日時",
            "休憩開始時間",
            "休憩終了時間",
            "休憩時間",
            "勤務時間",
            "備考欄"
        ]

        return self.create_spreadsheet(
            folder_id=folder_id,
            name=f'TTTTT_{month_name}月_日報',
            description=f'{month_name}月の日報用スプレッドシート',
            headers=headers,
            sheet_type="日報ファイル"
        )

    def create_workrecord_spreadsheet(self, folder_id: str, month_name: str) -> Optional[str]:
        """出勤簿用スプレッドシートを作成する"""
        headers = [
            "出勤日時",
            "退勤日時",
            "休憩開始時間",
            "休憩終了時間",
            "休憩時間",
            "勤務時間",
            "備考欄"
        ]

        return self.create_spreadsheet(
            folder_id=folder_id,
            name=f'TTTTT_{month_name}月_出勤簿',
            description=f'{month_name}月の出勤簿用スプレッドシート',
            headers=headers,
            sheet_type="出勤簿ファイル"
        )


    def create_deliverable_spreadsheet(self, folder_id: str, month_name: str) -> str | None:
        """納品物スプレッドシートを作成する"""
        headers = [
            "納品日時",
            "納品物名",
            "単価",
            "金額",
        ]

        return self.create_spreadsheet(
            folder_id=folder_id,
            name=f'TTTTT_{month_name}月_日報',
            description=f'{month_name}月の日報用スプレッドシート',
            headers=headers,
            sheet_type="日報ファイル"
        )

    def create_spreadsheet(self, folder_id: str, name: str, description: str,
                            headers: list[str], sheet_type: str) -> Optional[str]:
        """スプレッドシートを作成する関数"""
        try:
            # スプレッドシートのメタデータ
            spreadsheet_metadata = {
                'name': name,
                'parents': [folder_id],
                'mimeType': 'application/vnd.google-apps.spreadsheet',
                'description': description
            }

            # スプレッドシートを作成
            spreadsheet = self.service.files().create(body=spreadsheet_metadata).execute()
            spreadsheet_id = spreadsheet['id']

            # 権限設定
            self.connection.set_permission(spreadsheet_id, sheet_type)

            # ヘッダーを設定
            self.setup_headers(spreadsheet_id, headers)

            print(f"スプレッドシート '{name}' が作成されました。ID: {spreadsheet_id}")
            return spreadsheet_id

        except HttpError as error:
            logger.error(f"スプレッドシート作成エラー: {error}")
            return None
        except Exception as error:
            logger.error(f"予期しないエラー: {error}")
            return None

    def setup_headers(self, spreadsheet_id: str, headers: list[str]):
        """ヘッダーを設定する"""
        try:
            sheet = self.gc.open_by_key(spreadsheet_id)
            worksheet = sheet.sheet1

            # ヘッダー行を設定
            header_range = f'A1:{chr(ord("A") + len(headers) - 1)}1'
            worksheet.update(values=[headers], range_name=header_range)

            # ヘッダー行のフォーマット設定
            worksheet.format(header_range, {
                "backgroundColor": {
                    "red": 0.8,
                    "green": 0.8,
                    "blue": 0.8
                },
                "textFormat": {
                    "bold": True
                }
            })

        except Exception as error:
            logger.error(f"ヘッダー設定エラー: {error}")