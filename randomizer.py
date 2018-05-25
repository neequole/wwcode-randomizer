import json
import os
import random
import pathlib
import csv

from flask import Flask, render_template, jsonify, Response, session
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseDownload


CSV_NAME = 'questions.csv'
FILE_ID = '1vh6cKhIPFQMq-F1vdviA5Rud6-fieBG-d8WaIbKW3jY'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'client_secret.json'

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.default')
app.config.from_envvar('APP_CONFIG_FILE')


def connect():
    """ Creates Google drive service """
    # Get first from environment variable before attempting json file
    environ_credential = os.environ.get('GOOGLE_CREDENTIALS')
    if environ_credential:
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(environ_credential), scopes=SCOPES)
    else:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = discovery.build('drive', 'v3', credentials=credentials)
    return service


def download_spreadsheet():
    """ Downloads Google spreadsheet as CSV file """
    service = connect()
    request = service.files().export_media(fileId=FILE_ID, mimeType='text/csv')
    with open(CSV_NAME, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))


def read_csv():
    """ Gets questions from CSV file """
    with open(CSV_NAME, newline='') as fh:
        reader = csv.DictReader(fh)
        return list(reader)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quote')
def generate_quote():
    # Download spreadsheet if not yet exists
    path = pathlib.Path(CSV_NAME)
    if not path.exists():
        download_spreadsheet()
    questions = read_csv()
    # Generate new random row number
    row = random.randrange(0, len(questions))
    random_rows = session.get('random_rows', [])
    # Free up rows to avoid infinite loop
    if len(random_rows) == len(questions):
        random_rows = []
    while row in random_rows:
        row = random.randrange(0, len(questions))
    random_rows.append(row)
    session['random_rows'] = random_rows
    return jsonify(questions[row]['Your question'])


@app.route('/download')
def download():
    download_spreadsheet()
    return Response(status=200)


@app.route('/refresh', methods=['POST'])
def refresh_session():
    session.pop('random_rows', None)
    return Response(status=200)
