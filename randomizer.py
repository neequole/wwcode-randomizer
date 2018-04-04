import random

from flask import Flask, render_template
from google.oauth2 import service_account
from googleapiclient import discovery


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'client_secret.json'

app = Flask(__name__)


def read_spreadsheet():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = discovery.build('sheets', 'v4', credentials=credentials)
    spreadsheet_id = '1vh6cKhIPFQMq-F1vdviA5Rud6-fieBG-d8WaIbKW3jY'
    range_name = 'Form Responses 1!A2:B'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result.get('values', [])


@app.route('/')
def index():
    # TODO: Find row count of sheet to avoid reading whole sheet
    questions = read_spreadsheet()
    row = random.randrange(0, len(questions))
    return render_template('index.html', random_question=questions[row][1])
