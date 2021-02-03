import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleSheetsWriter:

    def __init__(self, credential_path, spreadsheet_id):
        self.credential_path = credential_path
        self.spreadsheet_id = spreadsheet_id
        self.sheet_service = self.build_api_sheets_service()

    def write(self, sheet_name, values: list):
        body = {'values': [values]}
        range_end_char = self._calculate_range(values)
        request = self.sheet_service.values().append(
            spreadsheetId=self.spreadsheet_id,
            valueInputOption='RAW',
            range=f'{sheet_name}!A:{range_end_char}',
            body=body)
        response = request.execute()
        return response

    def _calculate_range(self, values):
        range_end_char = chr(ord('@') + len(values))
        return range_end_char

    def build_api_sheets_service(self):
        credentials = self.retrieve_google_api_credentials()
        service = build('sheets', 'v4', credentials=credentials)
        sheets = service.spreadsheets()
        return sheets

    def retrieve_google_api_credentials(self):
        credentials = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credential_path, SCOPES)
                credentials = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)
        return credentials
