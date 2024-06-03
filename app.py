import re
import streamlit as st
from sumy.utils import get_stop_words
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import base64
from googleapiclient.discovery import build
import os
import json

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_emails(service):
    # Call the Gmail API
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    emails = []
    if not messages:
        st.warning('No messages found.')
    else:
        for message in messages:
            msg = service.users().messages().get(
                userId='me', id=message['id']).execute()
            email_data = {}
            headers = msg['payload']['headers']
            for header in headers:
                if header['name'] == 'Subject':
                    email_data['subject'] = header['value']
                if header['name'] == 'From':
                    email_data['from'] = header['value']
            parts = msg['payload'].get('parts')
            if parts:
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        email_body = base64.urlsafe_b64decode(
                            part['body']['data'].encode('ASCII')).decode('utf-8')
                        email_data['body'] = email_body
            else:
                email_body = base64.urlsafe_b64decode(
                    msg['payload']['body']['data'].encode('ASCII')).decode('utf-8')
                email_data['body'] = email_body
            emails.append(email_data)

    return emails


def extract_salutation(text):
    salutation_pattern = r'^(Hi|Hello|Dear|Greetings|Regards|Hi there|Hey|Good [mM]orning|Good [aA]fternoon|Good [eE]vening),?[\s\r\n]'
    match = re.search(salutation_pattern, text, re.MULTILINE)
    if match:
        return match.group(0).strip(',')
    return ''


def extract_signature(text):
    signature_pattern = r'(?:\n\r?(?:--\r?\n|__\r?\n)|[-\*\s][-\*\s]+\r?\n)(\r?\n\r?[-\w\s,\.@]+(?:\r?\n[-\w\s,\.@]+)*)'
    match = re.search(signature_pattern, text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ''


def preprocess_text(text):
    salutation = extract_salutation(text)
    text = text.replace(salutation, '', 1) if salutation else text

    signature = extract_signature(text)
    text = text.replace(signature, '')

    return text


def summarizing(message):
    LANGUAGE = "english"
    SENTENCES_COUNT = 3

    parser = PlaintextParser.from_string(message, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    string = ''

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        string += str(sentence) + '\n'

    return string


def main():
    st.title("Email Summarizer")

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        if st.button("Authenticate with Gmail"):
            creds = authenticate_gmail()
            service = build('gmail', 'v1', credentials=creds)
            st.session_state.service = service
            st.session_state.authenticated = True
            st.success("Authenticated successfully")
    else:
        service = st.session_state.service
        emails = get_emails(service)

        if emails:
            email_options = [
                f"{email['subject']} - {email['from']}" for email in emails]
            selected_email = st.selectbox(
                "Select an email to summarize", email_options)

            if selected_email:
                selected_email_index = email_options.index(selected_email)
                email_text = emails[selected_email_index]['body']
                text = preprocess_text(email_text)
                summary = summarizing(text)
                st.subheader("Original Email")
                st.write(email_text)
                st.subheader("Summary")
                st.write(summary)
        else:
            st.warning("No emails found.")


if __name__ == "__main__":
    main()
