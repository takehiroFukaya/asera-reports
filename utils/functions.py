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
    except ValueError:
        return "0:00"


WORK_START, WORK_END = 9, 18
NIGHT_START, NIGHT_END = 22, 5  # 22:00–05:00


def _overlap_hours(
    a_start: datetime.datetime,
    a_end: datetime.datetime,
    b_start: datetime.datetime,
    b_end: datetime.datetime,
) -> float:
    start = max(a_start, b_start)
    end = min(a_end, b_end)
    if end <= start:
        return 0.0
    return (end - start).total_seconds() / 3600.0


def _mk(d: datetime.date, h: int, m: int = 0) -> datetime.datetime:
    return datetime.datetime(d.year, d.month, d.day, h, m, 0)


def calculate_overtime(row) -> Tuple[str, str, str, str]:
    """
    row:
      0 出勤日時, 1 退勤日時, 2 休憩開始時間, 3 休憩終了時間,
      4 休憩時間(H:MM), 5 勤務時間(H:MM), 6 備考
    returns: (勤務時間, 所定外1, 所定外2, 所定外3) as "H:MM"
    """
    try:
        start = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        if end <= start:
            return "", "", "", ""

        # Build worked intervals and subtract explicit break if valid
        intervals = [(start, end)]
        try:
            if len(row) > 3 and row[2] and row[3]:
                # bs = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
                # be = datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
                bs = datetime.datetime.strptime(row[2], "%H:%M:%S")
                be = datetime.datetime.strptime(row[3], "%H:%M:%S")
                bs = datetime.datetime.combine(start.date(), bs.time())
                be = datetime.datetime.combine(start.date(), be.time())
                print(bs)
                print(be)
                if be > bs:
                    bs = max(bs, start)
                    be = min(be, end)
                    if be > bs:
                        left = (start, bs) if bs > start else None
                        right = (be, end) if be < end else None
                        intervals = [x for x in (left, right) if x and x[1] > x[0]]

        except Exception as e:
            print(f"エラーが発生しました: {e}")

        # If no explicit break, shave 休憩時間 from the end if provided
        if (
            len(row) > 4
            and row[4]
            and ":" in str(row[4])
            and not (len(row) > 3 and row[2] and row[3])
        ):
            try:
                h, m, *_ = map(int, str(row[4]).split(":"))
                shave = h + m / 60
                if shave > 0 and intervals:
                    total = sum((b - a).total_seconds() for a, b in intervals) / 3600.0
                    shave = min(shave, total)
                    a, b = intervals[-1]
                    new_end = b - datetime.timedelta(hours=shave)
                    if new_end > a:
                        intervals[-1] = (a, new_end)
                    else:
                        intervals.pop()
            except Exception as e:
                print(f"エラーが発生しました: {e}")

        # Totals
        total_work = sum((b - a).total_seconds() for a, b in intervals) / 3600.0

        # Weekend: 所定外2 = all hours
        if start.weekday() in (5, 6):
            return (
                hours_to_time(max(0.0, total_work)),
                "",  # 所定外1
                hours_to_time(max(0.0, total_work)),  # 所定外2
                "",  # 所定外3 (keep empty to match current rule)
            )

        # Weekday windows per date
        def day_windows(day: datetime.date):
            d0 = _mk(day, 0, 0)
            end_of_day = _mk(day, 0) + datetime.timedelta(days=1)
            return {
                "early": (_mk(day, 5), _mk(day, WORK_START)),  # 05:00–09:00
                "late": (_mk(day, WORK_END), _mk(day, NIGHT_START)),  # 18:00–22:00
                "n1": (_mk(day, NIGHT_START), end_of_day),  # 22:00–24:00
                "n2": (_mk(day, 0), _mk(day, NIGHT_END)),  # 00:00–05:00
                "dayseg": (d0, end_of_day),  # whole day
            }

        ns1 = 0.0  # 所定外1
        ns3 = 0.0  # 所定外3

        for a, b in intervals:
            cur = a.date()
            while cur <= b.date():
                wd = day_windows(cur)
                seg_s = max(a, wd["dayseg"][0])
                seg_e = min(b, wd["dayseg"][1])

                ns3 += _overlap_hours(seg_s, seg_e, *wd["n1"])
                ns3 += _overlap_hours(seg_s, seg_e, *wd["n2"])
                ns1 += _overlap_hours(seg_s, seg_e, *wd["early"])
                ns1 += _overlap_hours(seg_s, seg_e, *wd["late"])

                cur += datetime.timedelta(days=1)

        # Clamp non-negative
        ns1 = max(0.0, ns1)
        ns3 = max(0.0, ns3)

        return (
            hours_to_time(max(0.0, total_work)),  # 勤務時間
            hours_to_time(ns1),  # 所定外1
            "",  # 所定外2 (weekday)
            hours_to_time(ns3),  # 所定外3
        )
    except Exception:
        return "", "", "", ""


def timedelta_to_hhmm(td: datetime.timedelta) -> str:
    total_time_seconds = int(td.total_seconds())
    hours = total_time_seconds // 3600
    minutes = (total_time_seconds % 3600) // 60

    return f"{hours:02}:{minutes:02}"
