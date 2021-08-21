#!/usr/bin/env python
# coding:utf-8
from googleapiclient.discovery import build
from oauth2client import file, client, tools
import httplib2
import argparse
import csv
import sys
 
SPREADSHEET_ID = ''
RANGE_NAME = 'sheet1!A1'
MAJOR_DIMENSION = 'ROWS'
 
CLIENT_SECRET_FILE = '/home/pi/client_secret.json'
CREDENTIAL_FILE = "/home/pi/credential-oauth.json"
APPLICATION_NAME = ''
 
store = file.Storage(CREDENTIAL_FILE)
credentials = store.get()
if not credentials or credentials.invalid:
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    args = '--auth_host_name localhost --logging_level INFO --noauth_local_webserver'
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args(args.split())
    credentials = tools.run_flow(flow, store, flags)
 
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?' 'version=v4')
service = build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
resource = service.spreadsheets().values()

# read data from stdin / file as CSV
parser = argparse.ArgumentParser()
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin)
args = parser.parse_args(sys.argv[1:])
r = csv.reader(args.infile, delimiter='\t')
data = list(r)
 
body = {
    "range": RANGE_NAME,
    "majorDimension": MAJOR_DIMENSION,
    "values": data
}
resource.append(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                valueInputOption='USER_ENTERED', body=body).execute()

