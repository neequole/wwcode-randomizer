import json
import os
import random

from flask import Flask, render_template, jsonify
from google.oauth2 import service_account
from googleapiclient import discovery


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'client_secret.json'

app = Flask(__name__)


def connect():
    """ Creates Google spreadsheet service """
    # Get first from environment variable before attempting json file
    environ_credential = os.environ.get('GOOGLE_CREDENTIALS')
    if environ_credential:
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(environ_credential), scopes=SCOPES)
    else:
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
    return render_template('index.html')


@app.route('/quote')
def generate_quote():
    service = connect()
    spreadsheet_id = '1vh6cKhIPFQMq-F1vdviA5Rud6-fieBG-d8WaIbKW3jY'
    sheet_name = 'Form Responses 1!'
    # Get random row number
    total_range = sheet_name + 'D1:D1'
    total = read_spreadsheet(service, spreadsheet_id, total_range)
    questions_count = int(total[0][0])
    row = random.randrange(2, questions_count + 2)  # 2: header + stop
    # Get random row value
    question_range = '{}B{}:B{}'.format(sheet_name, row, row)
    question = read_spreadsheet(service, spreadsheet_id, question_range)
    return jsonify(question[0][0])
