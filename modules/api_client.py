
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd
from modules.constants import SPREADSHEET_ID
from modules.constants import SCOPES


class ApiClient:

    #constructor empty so far, might add fields
    def __init__(self) -> None:
        pass

    #get the contents of a spreasheet in 'Incasari Centralizator' as a pandas table
    #function takes as parameters the name of the spreadsheet the user specifies and the column cells between which they wamt to store the data
    #TODO: make separate authentication function
    def makePandasTable(self, range_str):
        credentials = None
        if os.path.exists("token.json"):
            credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                credentials = flow.run_local_server(port = 0)
            with open("token.json", "w") as token:
                token.write(credentials.to_json())

        try:
            service = build('sheets', 'v4', credentials = credentials)
            print("Auth succesful")
            sheets = service.spreadsheets()

            result = sheets.values().get(spreadsheetId = SPREADSHEET_ID, range = range_str).execute()

            values = result.get("values", [])

            header = values[0]
            data = values[1:]

            df = pd.DataFrame(data, columns = header)
            
            #returns the table
            print(df)
            return df
        
        except HttpError as error:
            print(error)

