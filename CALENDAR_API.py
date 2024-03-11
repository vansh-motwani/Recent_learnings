import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


start_date= '2024-02-21T17:37:00'
end_date= '2024-02-21T17:39:00'
competition_name="HII"
SCOPES = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())
service = build("calendar", "v3", credentials=creds)
event = {
'summary': competition_name,
'start': {
    'dateTime': start_date,
    'timeZone': 'GMT+05:30',
},
'end': {
    'dateTime': end_date,
    'timeZone': 'GMT+05:30',
},
'attendees': [
    {'email': "vansh.student@gmail.com"},
],
'reminders': {
    'useDefault': False,
    'overrides': [
    {'method': 'email', 'minutes': 5},
    ],
},
}
event = service.events().insert(calendarId='primary', body=event).execute()
print(event.get('htmlLink'))
