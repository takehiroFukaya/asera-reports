import datetime
import logging
from typing import Dict, List

import pandas as pd

from .connection import Connection
from .functions import calculate_overtime

logger = logging.getLogger(__name__)


class SpreadsheetUpdater:
    def __init__(self):
        self.connection = Connection()
        self.gc = self.connection.gc
        self.service = self.connection.service
        self.parent_folder = self.connection.find_folder_by_name(
            f"日報_{self.connection.user}"
        )
        self.last_status = {"ok": None, "stage": "", "detail": ""}
        if not self.parent_folder:
            logger.error(f"日報_{self.connection.user}のファイルが見つかりません")

    # issue 18
    def add_work_report(
        self,
        start_datetime: datetime.datetime,
        end_datetime: datetime.datetime,
        work_category: str,
        work_content: str,
        work_client: str,
        deliverables: List[Dict] | None = None,
    ) -> bool:

        month = f"{start_datetime.year}年{start_datetime.month}"
        sheet_name = "作業内容"
        data = [
            str(start_datetime),
            str(end_datetime),
            work_category,
            work_content,
            work_client,
        ]


        if deliverables:
            for item in deliverables:
                amount = int(item["deliverable_quantity"]) * item["unit_price"]
                item_data = [
                    str(item["date"]),
                    item["deliverable_item"],
                    item["deliverable_quantity"],
                    item["unit_price"],
                    amount
                ]
                if not self.add_record(month, "納品物", item_data):
                    return False

        return self.add_record(month, sheet_name, data)

    def add_record(self, month: str, sheet_name: str, data: list):
        this_year = datetime.datetime.now().year
        try:
            folder_id = self.connection.find_folder_by_name(f"{this_year}年_{month}", self.parent_folder)
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
            # month folder
            folder_id = self.connection.find_folder_by_name(month, self.parent_folder)
            if not folder_id:
                msg = f"{month}月のフォルダが見つかりません"
                logger.error(msg)
                self.last_status = {"ok": False, "stage": "month_folder", "detail": msg}
                return pd.DataFrame()

            # spreadsheet
            expected_name = f"{self.connection.user}_{month}月_日報"
            spreadsheet_id = self.connection.find_spreadsheet(folder_id, expected_name)
            if not spreadsheet_id:
                msg = f"{expected_name}のファイルが見つかりません"
                logger.error(msg)
                self.last_status = {"ok": False, "stage": "spreadsheet", "detail": msg}
                return pd.DataFrame()

            # data
            sheet = self.gc.open_by_key(spreadsheet_id)
            worksheet = sheet.sheet1
            all_values = worksheet.get_all_values()

            if not all_values or len(all_values) < 2:
                msg = (
                    "シートは見つかりましたが、データ行がありません（ヘッダーのみ/空）"
                )
                logger.info(msg)
                self.last_status = {"ok": False, "stage": "empty", "detail": msg}
                return pd.DataFrame()

            day_report_data = all_values[1:]

            data = []
            headers = [
                "出勤日時",
                "退勤日時",
                "勤務時間",
                "休憩時間",
                "所定外1",
                "所定外2",
                "所定外3",
                "摘要",
            ]

            for row in day_report_data:
                work_time, overtime_1, overtime_2, overtime_3 = calculate_overtime(row)
                data.append(
                    {
                        "出勤日時": row[0],
                        "退勤日時": row[1],
                        "勤務時間": work_time,
                        "休憩時間": row[4],
                        "所定外1": overtime_1,
                        "所定外2": overtime_2,
                        "所定外3": overtime_3,
                        "摘要": row[6],
                    }
                )

            df = pd.DataFrame(data, columns=headers)
            self.last_status = {"ok": True, "stage": "ok", "detail": "Loaded"}
            return df

        except Exception as e:
            msg = f"{self.connection.user}_{month}月_日報でのデータ取得に失敗しました: {e}"
            logger.exception(msg)
            self.last_status = {"ok": False, "stage": "exception", "detail": msg}
            return pd.DataFrame()

    def get_work_logs(self, month: str, sheet_name: str = "作業内容") -> pd.DataFrame:
        try:
            folder_id = self.connection.find_folder_by_name(month, self.parent_folder)
            if not folder_id:
                logger.error(f"{month}月のフォルダが見つかりません")
                return pd.DataFrame()

            spreadsheet_id = self.connection.find_spreadsheet(folder_id, sheet_name)
            if not spreadsheet_id:
                logger.error(f"{sheet_name}のスプレッドシートが見つかりません")
                return pd.DataFrame()

            deliverable_spreadsheet_id = self.connection.find_spreadsheet(folder_id,"納品物")
            if not spreadsheet_id:
                logger.error(f"納品物のスプレッドシートが見つかりません")
                return pd.DataFrame()

            sheet = self.gc.open_by_key(spreadsheet_id)
            worksheet = sheet.sheet1
            work_values = worksheet.get_all_values()

            if not work_values or len(work_values) < 2:
                return pd.DataFrame()

            work_headers = work_values[0]
            work_data = work_values[1:]
            work_df = pd.DataFrame(work_data,columns=work_headers)

            deliverable_sheet = self.gc.open_by_key(deliverable_spreadsheet_id)
            deliverable_worksheet = deliverable_sheet.sheet1
            deliverable_values = deliverable_worksheet.get_all_values()

            if not deliverable_values or len(deliverable_values) < 2:
                deliverable_df = pd.DataFrame()
            else:
                deliverable_headers = deliverable_values[0]
                deliverable_data = deliverable_values[1:]
                deliverable_df = pd.DataFrame(deliverable_data, columns=deliverable_headers)


            if not deliverable_df.empty:
                date_column_work = "作業開始日時"
                date_column_deliverable = "納品日時"

                work_df[date_column_work] = pd.to_datetime(work_df[date_column_work], errors='coerce')
                deliverable_df[date_column_deliverable] = pd.to_datetime(deliverable_df[date_column_deliverable],errors='coerce')

                df = pd.merge(work_df,deliverable_df,left_on=date_column_work,right_on=date_column_deliverable,how='left')
            else:
                df = work_df


            # df = pd.DataFrame(data, columns=headers)
            # df["金額"] = (
            #     pd.to_numeric(df["金額"], errors="coerce").fillna(0).astype(int)
            # )
            return df

        except Exception as e:
            logger.error(f"{sheet_name}のデータ取得に失敗しました: {e}")
            return pd.DataFrame()
