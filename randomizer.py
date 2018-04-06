import random

from flask import Flask, render_template
from google.oauth2 import service_account
from googleapiclient import discovery


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'client_secret.json'

app = Flask(__name__)


def connect():
    """ Creates Google spreadsheet service """
    # TODO: Find way to save in Storage like Oauth2
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = discovery.build('sheets', 'v4', credentials=credentials)
    return service


def read_spreadsheet(service, id_, range_):
    """ Reads range from specified worksheet """
    result = service.spreadsheets().values().get(
        spreadsheetId=id_, range=range_).execute()
    return result.get('values', [])


@app.route('/')
def index():
    service = connect()
    spreadsheet_id = '1vh6cKhIPFQMq-F1vdviA5Rud6-fieBG-d8WaIbKW3jY'
    sheet_name = 'Form Responses 1!'
    # Get random row number
    total_range = sheet_name + 'D1:D1'
    total = read_spreadsheet(service, spreadsheet_id, total_range)
    questions_count = int(total[0][0])
    row = random.randrange(2, questions_count+1)
    # Get random row value
    question_range = '{}B{}:B{}'.format(sheet_name, row, row)
    question = read_spreadsheet(service, spreadsheet_id, question_range)
    return render_template('index.html', random_question=question[0][0])
