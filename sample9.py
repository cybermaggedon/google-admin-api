
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
    
def main():

    service = get_service()

    # Call the Admin SDK Directory API
    print('Search for user')

    user = get_user(service, "user07@workshop.pivotlabs.io")

    print(u'{0} ({1}) - {2}'.format(
        user['primaryEmail'],
        user['name']['fullName'],
        user['isEnrolledIn2Sv']
    ))
                              
    userKey = user['id']
    print(userKey)

    user["password"] = "bunches9876"

    results = update_user(service, userKey, user)

    print(results)

if __name__ == '__main__':
    main()

