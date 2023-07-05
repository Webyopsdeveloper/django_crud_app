import csv
import os
import psycopg2
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
        writer.writerow(['Label', 'Sender', 'Recipient', 'Header', 'Date'])

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            label = ', '.join(msg['labelIds'])
            sender = None
            recipient = None
            header = None
            date = None

           
            payload = msg['payload']
            headers = payload['headers']
            for header in headers:
                name = header['name']
                if name == 'From':
                    sender = header['value']
                elif name == 'To':
                    recipient = header['value']
                elif name == 'Subject':
                    header = header['value']
                elif name == 'Date':
                    date = header['value']
            
          
            writer.writerow([label, sender, recipient, header, date])

    print("Data extracted and saved to 'gmail_data.csv'.")


def load_csv_to_sql():
    connection = psycopg2.connect(
        host="::1",
        database="gmailApi",
        user="postgres",
        password="postgres"
    )
    cursor = connection.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails
        (Label TEXT, Sender TEXT, Recipient TEXT, Header TEXT, Date TEXT)
    ''')

    
    with open('gmail_data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        cursor.executemany('INSERT INTO emails VALUES (%s, %s, %s, %s, %s)', reader)

    connection.commit()
    connection.close()

    print("Data loaded into PostgreSQL database.")


def main():
    extract_gmail_data()
    load_csv_to_sql()

if __name__ == '__main__':
    main()
