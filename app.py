#main entry point in app

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd
from modules.api_client import ApiClient


#this function gets me the information from a spreadsheet
#TODO: create a function that reads data from a spredsheet and return it as a pandas table
def main():
    api_man = ApiClient()
    rangeName = 'Tr!A1:F10'
    res = api_man.makePandasTable(rangeName)
    print(res)  

if __name__ == "__main__":
    main()

    