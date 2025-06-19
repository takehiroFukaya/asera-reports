import datetime
import os

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

load_dotenv()


folder_id = os.environ.get('DEFALUT_FOLDER_ID')

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    '../asera-dayreport-15c05cf58a1f.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)
service = build("drive","v3", credentials=credentials)

now_month = str(datetime.datetime.now().month)



result = service.files().list(q=f"name='{now_month}' and '{folder_id}' in parents").execute()

print(result.get('files',[]))


""" その月のファイルがあるかどうかを確認する。なかった場合ファイルを作成して作成したファイルの中にスプレッドシートを作成する """
if not result.get('files',[]):
    print("ファイルないよー")
    folder_metadata = {
        'name': now_month,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id]
    }
    create_folder = service.files().create(body=folder_metadata).execute()
    month_folder_id = create_folder['id']
    permission = {
        'type': 'user',
        'role': 'writer',  # 'reader', 'writer', 'owner'から選択
        'emailAddress': 'aseratkyn@gmail.com'
    }
    service.permissions().create(
        fileId=month_folder_id,
        body=permission,
        sendNotificationEmail=False
    ).execute()
    print(f"フォルダ '{now_month}' が作成されました。ID: {create_folder['id']}")



else:
    for file in result.get("files", []):
        month_folder_id = file.get("id")
    print("ファイルあるよー")
    print(month_folder_id)



