import datetime
import logging

from .connection import Connection

logger = logging.getLogger(__name__)

class SpreadsheetUpdater:
    def __init__(self):
        self.connection = Connection()
        self.gc = self.connection.gc
        self.service = self.connection.service
        self.parent_folder = self.connection.find_folder_by_name(f"日報_{self.connection.user}")
        if not self.parent_folder:
            logger.error(f"日報_{self.connection.user}のファイルが見つかりません")

    def add_work_report(self, start_datetime: datetime.datetime, end_datetime: datetime.datetime, work_category: str, work_content: str, work_client: str, deliverable_item: str, deliverable_quantity: int, amount: int) -> bool:

        month = str(start_datetime.month)
        sheet_name = "作業内容"
        data = [
            str(start_datetime),
            str(end_datetime),
            work_category,
            work_content,
            work_client,
            deliverable_item,
            str(deliverable_quantity),
            str(amount)
        ]
        return self.add_record(month, sheet_name, data)


    def add_record(self, month: str, sheet_name: str, data: list ):
        try:
            folder_id = self.connection.find_folder_by_name(month,self.parent_folder)
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





