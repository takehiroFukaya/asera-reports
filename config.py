import os

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

class Config:
    folder_id = os.environ.get('DEFALUT_FOLDER_ID')
    account_file = '../desktop.json'
    scopes = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/userinfo.profile"
    ]
    share_email = ['aseratkyn@gmail.com']

