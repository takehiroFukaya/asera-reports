import datetime
import logging
import time

from connection import Connection
from spreadsheet_creator import SpreadsheetCreator
from streamlit import connection

logger = logging.getLogger(__name__)


class SetupFolder:
    def __init__(self):
        self.connection = Connection()
        self.spread = SpreadsheetCreator(self.connection)


    def setup(self):
        """指定された月のセットアップを行う,成功したらtrueを返す"""
        current_month = str(datetime.datetime.now().month)
        try:
            folder_id = self.connection.find_monthly_folder(current_month)
            if not folder_id:
                folder_id = self.connection.create_folder(current_month)
                # 少し待機（API制限対策）
                time.sleep(2)
                print(f"フォルダ{current_month}を作成しました")

                # スプレッドシートを作成
                success = self.create_all_spreadsheets(folder_id, current_month)

                return success
            else:
                print(f"すでにフォルダ{current_month}は存在します")
                return True

        except Exception as error:
            logger.error(f"セットアップ中にエラーが発生しました: {error}")
            return False

    def create_all_spreadsheets(self, folder_id: str, month: str) -> bool:
        """すべてのスプレッドシートを作成する"""
        spreadsheets_to_create = [
            ("日報", self.spread.create_daily_report_spreadsheet),
            ("作業内容", self.spread.create_work_report_spreadsheet),
            ("出勤簿", self.spread.create_workrecord_spreadsheet),
            ("納品物", self.spread.create_deliverable_spreadsheet),
        ]

        success_count = 0
        total_count = len(spreadsheets_to_create)

        for name, create_func in spreadsheets_to_create:
            try:
                print(f"{name}スプレッドシートを作成中...")
                spreadsheet_id = create_func(folder_id, month)

                if spreadsheet_id:
                    success_count += 1
                    print(f"{name}スプレッドシートの作成が完了しました")
                else:
                    print(f"{name}スプレッドシートの作成に失敗しました")

                # API制限対策で少し待機
                time.sleep(1)

            except Exception as error:
                logger.error(f"{name}スプレッドシート作成中にエラー: {error}")

        return success_count == total_count

