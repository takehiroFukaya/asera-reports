import datetime
import logging

from utils.connection import Connection
from utils.spreadsheet_updater import SpreadsheetUpdater

logger = logging.getLogger(__name__)


class RegisterShift:
    def __init__(self):
        self.connection = Connection()
        self.gc = self.connection.gc
        self.service = self.connection.service
        self.parent_folder = self.connection.find_folder_by_name(
            f"日報_{self.connection.user}"
        )
        if not self.parent_folder:
            logger.error(f"日報_{self.connection.user}のファイルが見つかりません")

    @staticmethod
    def add_shift(
        work_date,
        start_time,
        end_time,
        rest_start_time,
        rest_end_time,
        remarks: str,
    ):
        updater = SpreadsheetUpdater()

        start_date_time = datetime.datetime.combine(work_date, start_time)
        end_date_time = datetime.datetime.combine(work_date, end_time)
        rest_start_date_time = datetime.datetime.combine(work_date, rest_start_time)
        rest_end_date_time = datetime.datetime.combine(work_date, rest_end_time)

        rest_time = rest_end_date_time - rest_start_date_time
        work_time = end_date_time - start_date_time - rest_time

        """作業内容のレコードを追加する。引数に受け取るデータを追加して受け取れるようにする。"""
        return updater.add_record(
            str(datetime.datetime.now().month),
            "日報",
            [
                str(start_date_time),
                str(end_date_time),
                str(rest_start_time),
                str(rest_end_time),
                str(rest_time),
                str(work_time),
                remarks,
            ],
        )
