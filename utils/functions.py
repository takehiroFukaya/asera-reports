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
        overtime_1 = 0.0
        overtime_2 = 0.0
        overtime_3 = 0.0
        work_time_str = row[5] or "0:00"
        work_hours = time_to_hours(work_time_str)

        standard_hours = 8.0

        start_time_str = row[0]
        end_time_str = row[1]

        start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

        print(start_time)
        print(end_time)
        if start_time.date() == end_time.date():

            if start_time.weekday() == 5 or start_time.weekday() == 6:
                overtime_2 = work_hours
                return "", "", hours_to_time(overtime_2), ""

            start_hour = start_time.hour + start_time.minute / 60
            end_hour = end_time.hour + end_time.minute / 60

            nighttime_hours = 0.0

            # 22:00-24:00の範囲
            if start_hour < 24 and end_hour > 22:
                night_start = max(start_hour, 22)
                night_end = min(end_hour, 24)
                if night_end > night_start:
                    nighttime_hours += night_end - night_start
                    print(f"nighttime_hours:{nighttime_hours}")

            # 0:00-5:00の範囲
            if start_hour < 5 and end_hour > 0:
                night_start = max(start_hour, 0)
                night_end = min(end_hour, 5)
                if night_end > night_start:
                    nighttime_hours += night_end - night_start
                    print(f"nighttime_hours:{nighttime_hours}")

            overtime_3 = nighttime_hours

        total_overtime = max(0, work_hours - standard_hours)
        if total_overtime != 0:
            overtime_1 = total_overtime - overtime_3

        return (
            hours_to_time(work_hours),
            hours_to_time(overtime_1),
            hours_to_time(overtime_2),
            hours_to_time(overtime_3),
        )

    except:
        return "", "", "", ""
