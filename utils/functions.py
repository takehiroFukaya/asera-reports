import datetime
import io
from typing import Tuple

import pandas as pd


def generate_month_options():
    options = []
    today = datetime.date.today()
    current_year = today.year
    current_month = today.month

    for year in range(current_year, current_year - 6, -1):
        start_month = current_month if year == current_year else 12

        for month in range(start_month, 0, -1):
            month_str = f"{year}年{month}月"
            options.append(month_str)

    default_value = f"{current_year}年{current_month}月"
    default_index = options.index(default_value)

    return (options, default_index)


def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="WorkLog")
    processed_data = output.getvalue()
    return processed_data


def time_to_hours(time_string: str | pd.Timedelta) -> float:
    if isinstance(time_string, pd.Timedelta):
        return time_string.total_seconds() / 3600

    try:
        h, m, *_ = map(int, str(time_string).split(":"))
        return h + m / 60
    except ValueError:
        return 0.0


def hours_to_time(hours: float) -> str:
    try:
        h = int(hours)
        m = int((hours - h) * 60)
        return f"{h}:{m:02d}"
    except:
        return "0:00"


def calculate_overtime(row) -> Tuple[str, str, str, str]:
    try:
        work_time_str = row.get("勤務時間", "0:00") or "0:00"
        work_hours = time_to_hours(work_time_str)

        standard_hours = 8.0

        total_overtime = max(0, work_hours - standard_hours)
        if total_overtime <= 0:
            return "", "", "", ""

        start_time_str = row.get("出勤日時", "")
        end_time_str = row.get("退勤日時", "")

        return "", "", "", ""

    except:
        return "", "", "", ""
