import datetime
import io
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
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='WorkLog')
    processed_data = output.getvalue()
    return processed_data