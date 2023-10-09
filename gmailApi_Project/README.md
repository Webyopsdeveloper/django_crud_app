# Steps to get credentials.json file

1. Set up google cloud project: <br>
Open this link with the gmail account you want to extract, accept the terms   and conditions and click on agree and continue .

https://console.cloud.google.com/welcome?project=gmailapi-391416 


Create a new project or select an existing project from 'select a project' option on the top where you want to enable the Gmail API and set up the necessary credentials.<br>
Enter project name and click on create. <br>
The project will be created and now select it. 

2. enable gmail api:<br>

In the Google Cloud Console, navigate to "APIs & Services" > "Library".<br>
Search for "Gmail API" and click on it.<br>
Click the "Enable" button to enable the Gmail API for your project.

3. set up credentials:

In the Google Cloud Console, navigate to "APIs & Services" > "Credentials".<br>
Click on "Create credentials" and select "OAuth client ID".<br>
Configure the OAuth consent screen, click external and click create. Give the app name and select your email in the user support email from which you wish to extract emails.Give your email as developer contact information and click on 'save and continue'.

Click save and continue for edit app registration, add email id you want to extract in test users and save, click 'back to dashboard'.<br>
Now go to credentials and select "Desktop app" as the application type and click on download json to download the credentials(JSON file).

# Run the code
1. pip install psycopg2 google-api-python-client google-auth-httplib2 google-auth-oauthlib
2. Give all neccessary information as asked in the code. After that you will be directed to a link of google. Accept and continue every option, then you will be directed to a page with this message on it
"The authentication flow has completed. You may close this window." 

Wait for some seconds until the code stops running and all the mails would have been extracted. 
You may now check app.log file and your SQL database.



# To get coverage report 
1. pip install coverage
2. coverage run --source=. -m unittest unit_test.py























