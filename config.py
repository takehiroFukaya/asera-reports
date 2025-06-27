import os

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

class Config:
    folder_id = os.environ.get('DEFALUT_FOLDER_ID')
    service_account_file = '../asera-dayreport-15c05cf58a1f.json'
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    share_email = ['aseratkyn@gmail.com']

