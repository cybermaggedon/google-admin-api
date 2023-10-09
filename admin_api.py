
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

def get_service():

    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('admin', 'directory_v1', credentials=creds)

    return service

def get_user(service, email):

    results = service.users().list(
        customer='my_customer',
        maxResults=1,
        query=f"email={email}"
    ).execute()

    users = results.get('users', [])

    if not users:
        raise RuntimeError('No such user in the domain.')

    user = users[0]

    return user

def update_user(service, userKey, user):

    results = service.users().update(
        body=user,
        userKey=userKey
    ).execute()

    return results

def insert_user(service, user):

    results = service.users().insert(
        body=user,
    ).execute()

    return results

def do_delete_user(service, userKey):

    results = service.users().delete(
        userKey=userKey
    ).execute()

    return results

def change_password(email, password):

    service = get_service()

    # Call the Admin SDK Directory API
    print('Search for user')

    user = get_user(service, email)
                              
    userKey = user['id']

    user["password"] = password

    results = update_user(service, userKey, user)

    print(results)

def create_user(email, first, last, password):

    service = get_service()

    user = {
        "primaryEmail": email,
        "password": password,
        "name": {
            "givenName": first,
            "familyName": last,
        }
        
    }

    results = insert_user(service, user)

    print(results)

def suspend_user(email):

    service = get_service()

    # Call the Admin SDK Directory API
    print('Search for user')

    user = get_user(service, email)
                              
    userKey = user['id']

    user["suspended"] = True

    results = update_user(service, userKey, user)

    print(results)
    
def delete_user(email):

    service = get_service()

    # Call the Admin SDK Directory API
    print('Search for user')

    user = get_user(service, email)
                              
    userKey = user['id']

    results = do_delete_user(service, userKey)

    print(results)
    
def unsuspend_user(email):

    service = get_service()

    # Call the Admin SDK Directory API
    print('Search for user')

    user = get_user(service, email)
                              
    userKey = user['id']

    user["suspended"] = False

    results = update_user(service, userKey, user)

    print(results)

