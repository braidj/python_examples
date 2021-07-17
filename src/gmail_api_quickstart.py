from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import asyncio  # experimenting

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    all_msgs = get_all_messages(service)
    print(f"You have a total of {len(all_msgs)} email messages")

    ids = [x['id'] for x in all_msgs]

    chunks = len(ids) // 100 + 1 

    limit = 0
    for i in range(chunks):
        batch = ids[i*100:(i+1)*100]
        # if limit > 7:
        #     break
        extract_senders(batch, service)
        limit += 1


def get_all_messages(service, user_id='me'):

    try:
        response = service.users().messages().list(userId='me').execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId = 'me',pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except Exception as e:
        print(e)


def print_sender(request_id, response, exception):

    if exception is not None:

        print(f"Something bad happened {str(exception)}")
    else:
        # Do something with the response
        header_items = response['payload']['headers']

        for item in header_items:
            if item['name'] == 'From':
                #print(item['value'])
                all_senders.append(item['value'])


def extract_senders(msg_ids, service, user_id='me'):

    batch = service.new_batch_http_request()

    for item in msg_ids:
        batch.add(service.users().messages().get(userId=user_id, id=item), callback=print_sender)
        # response = service.users().messages().get(userId=user_id, id=item).execute()

    batch.execute()

def get_unique_senders(records):

    for item in records:
        senders[item] = senders.get(item, 0) + 1


if __name__ == '__main__':

    # ToDo save results to file

    all_senders = []
    senders = {}

    main()
    print(f"{len(all_senders)}")

    get_unique_senders(all_senders)

    for k in sorted(senders, key=senders.get, reverse=True):
        print(f"{k}: {senders[k]}")
