import csv
import os
import sqlite3
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail_api():
    creds = None

    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    
    return build('gmail', 'v1', credentials=creds)

def extract_gmail_data():
    service = authenticate_gmail_api()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=20).execute()
    messages = results.get('messages', [])

    
    with open('gmail_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Subject', 'Sender', 'Snippet'])

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            subject = None
            sender = None
            snippet = None

            
            payload = msg['payload']
            headers = payload['headers']
            for header in headers:
                name = header['name']
                if name == 'Subject':
                    subject = header['value']
                elif name == 'From':
                    sender = header['value']
            
            snippet = msg['snippet']
            
            writer.writerow([subject, sender, snippet])

    print("Data extracted and saved to 'gmail_data.csv'.")



def load_csv_to_sql():
    connection = sqlite3.connect('gmail_data.db')
    cursor = connection.cursor()

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails
        (subject TEXT, sender TEXT, snippet TEXT)
    ''')

    
    with open('gmail_data.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        cursor.executemany('INSERT INTO emails VALUES (?, ?, ?)', reader)

    connection.commit()
    connection.close()

    print("Data loaded into SQL database.")



def main():
    extract_gmail_data()
    load_csv_to_sql()

if __name__ == '__main__':
    main()
