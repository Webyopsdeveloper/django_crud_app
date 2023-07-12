import csv
import os
import psycopg2
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import logging
import datetime

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GmailExtractor:
    def __init__(self, credentials_path, token_path):
        self.credentials_path = credentials_path
        self.token_path = token_path

    def authenticate_gmail_api(self):
        creds = None

        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            if not os.path.exists(self.token_path):
                with open(self.token_path, 'w') as token:
                    token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def extract_gmail_data(self, service, email):
        logging.info(f"Starting Gmail data extraction for {email}...")
        start_time = datetime.datetime.now()

        results = service.users().messages().list(userId=email, labelIds=['INBOX'], maxResults=20).execute()
        messages = results.get('messages', [])

        with open('gmail_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Label', 'Sender', 'Recipient', 'Header', 'Date'])

            for i, message in enumerate(messages, 1):
                logging.info(f"Processing message {i}/{len(messages)}")
                msg = service.users().messages().get(userId=email, id=message['id']).execute()
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

        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        logging.info(f"Gmail data extraction completed for {email}. Time elapsed: {elapsed_time}")


def main():
    logging.info("----- Starting the program -----")

    email = input("Enter your email address: ")

    credentials_path = input("Enter the path to the credentials file (credentials.json): ")

    answer = input("Running the code for the first time? (yes/no): ")
    if answer.lower() == "yes":
        token_path = input("Enter the path to save the token file (token.json): ")
        token_path = token_path + '\\token.json'
    elif answer.lower() == "no":
        token_path = input("Enter the path to the existing token file (token.json): ")

    print("**********Now, let's set up your SQL database**********")
    host_input = input("Enter the SQL host: ")
    database_input = input("Enter the SQL database name: ")
    user_input = input("Enter the SQL username: ")
    password_input = input("Enter the SQL password: ")

    extractor = GmailExtractor(credentials_path, token_path)
    service = extractor.authenticate_gmail_api()
    extractor.extract_gmail_data(service, email)

    logging.info("Loading data into PostgreSQL database...")
    start_time = datetime.datetime.now()

    connection = psycopg2.connect(
        host=host_input,
        database=database_input,
        user=user_input,
        password=password_input
    )
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails
        (Label TEXT, Sender TEXT, Recipient TEXT, Header TEXT, Date TEXT)
    ''')

    with open('gmail_data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        cursor.executemany('INSERT INTO emails VALUES (%s, %s, %s, %s, %s)', reader)

    connection.commit()
    connection.close()

    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    logging.info(f"Data loaded into PostgreSQL database. Time elapsed: {elapsed_time}")

    logging.info("----- Program execution completed -----")


if __name__ == '__main__':
    main()
