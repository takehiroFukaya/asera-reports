import datetime
import logging

import pandas as pd

from .connection import Connection
from .functions import calculate_overtime
from .connection import Connection

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
    # issue 18
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

    def get_shift_record(self, month: str) -> pd.DataFrame:
        try:
            folder_id = self.connection.find_folder_by_name(month, self.parent_folder)
            if not folder_id:
                logger.error(f"{month}月のフォルダが見つかりません")
                return pd.DataFrame()  # <-- change

            spreadsheet_id = self.connection.find_spreadsheet(
                folder_id, f"{self.connection.user}_{month}月_日報"
            )
            if not spreadsheet_id:
                logger.error(
                    f"{self.connection.user}_{month}月_日報のファイルが見つかりません"
                )
                return pd.DataFrame()  # <-- change

            sheet = self.gc.open_by_key(spreadsheet_id)
            worksheet = sheet.sheet1
            all_values = worksheet.get_all_values()

            if not all_values or len(all_values) < 2:
                return pd.DataFrame()  # <-- empty sheet guard

            headers, day_report_data = all_values[0], all_values[1:]

            for _, row in day_report_data.iterrows():
                work_time, overtime_1, overtime_2, overtime_3 = calculate_overtime(row)
                shift_recor_row = {
                    "出勤日時": row.get("出勤日時", ""),
                    "退勤日時": row.get("退勤日時", ""),
                    "勤務時間": calculate_overtime(row, 0),
                    "休憩時間": row.get("休憩時間", ""),
                    "所定外1": calculate_overtime(row, 1),  # 所定外時間の計算
                    "所定外2": calculate_overtime(row, 2),
                    "所定外3": calculate_overtime(row, 3),
                    "摘要": row.get("備考欄", ""),
                }

            return pd.DataFrame(data, columns=headers)

        except Exception as e:
            logger.error(
                f"{self.connection.user}_{month}月_出勤簿でのデータ取得に失敗しました: {e}"
            )
            return pd.DataFrame()  # <-- change
