import datetime
import logging

from utils.connection import Connection

logger = logging.getLogger(__name__)


class SpreadsheetUpdater:
    def __init__(self):
        self.connection = Connection()
        self.gc = self.connection.gc
        self.service = self.connection.service
        self.parent_folder = self.connection.find_folder_by_name(
            f"日報_{self.connection.user}"
        )
        if not self.parent_folder:
            logger.error(f"日報_{self.connection.user}のファイルが見つかりません")

    def add_work_report(self):
        """作業内容のレコードを追加する。引数に受け取るデータを追加して受け取れるようにする。"""
        return self.add_record(
            str(datetime.datetime.now().month),
            "作業内容",
            [
                str(datetime.datetime.now()),
                str(datetime.datetime.now()),
                "UBIC",
                "なにか",
                "PCセットアップ",
                "2:00",
                "東進会社",
                "深谷",
            ],
        )

    def add_record(self, month: str, sheet_name: str, data: list):
        try:
            folder_id = self.connection.find_folder_by_name(month, self.parent_folder)
            if not folder_id:
                logger.error(f"{month}月のフォルダが見つかりません")
                return False

            spreadsheet_id = self.connection.find_spreadsheet(folder_id, sheet_name)
            if not spreadsheet_id:
                logger.error(f"{sheet_name}のファイルが見つかりません")
                return False

            sheet = self.gc.open_by_key(spreadsheet_id)
            worksheet = sheet.sheet1

            worksheet.append_row(data)
            print("レコードが追加されました")
            return True
        except Exception as error:
            logger.error(f"{sheet_name}でのデータの追加に失敗しました:{error}")
            return False
