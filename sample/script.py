import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """
    Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('path_to_pickle_file'):
        with open('path_to_pickle_file', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'path_to_credentials_file', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('path_to_pickle_file', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me', q='label:inbox is:unread').execute()
    id = results.get('messages')[0].get('id')
    number_of_mails = len(results.get('messages'))
    results = service.users().messages().get(userId='me', id=id).execute()
    sender = results.get('payload').get('headers')[4].get('value')
    for element in results.get('payload').get('headers'):
        if element.get('name') == 'From':
            sender = element.get('value')
    import re
    sender = re.search(r'<(.*)>', str(sender)).group(1)

    if number_of_mails > 0:
        query = f"{number_of_mails} unread email;Last mail from {sender}."
    else:
        query = "No new emails."
    sys.stdout.write(query)

if __name__ == '__main__':
    main()
