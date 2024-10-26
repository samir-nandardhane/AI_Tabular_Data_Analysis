import streamlit as st
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from googleapiclient.discovery import build

# Define scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


# Function to get access token and authenticate
def get_token():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


# Main function for the app
def main():
    st.title("Google Drive Integration with Streamlit")

    # Button to connect to Google Drive
    if st.button("Connect to Google Drive"):
        creds = get_token()
        if creds:
            st.success("Connected to Google Drive!")
            service = build('drive', 'v3', credentials=creds)

            # List files from Google Drive
            results = service.files().list(pageSize=10).execute()
            files = results.get('files', [])

            # Display the files in a selectbox for selection
            if files:
                file_names = {file['name']: file['id'] for file in files}
                selected_file = st.selectbox("Select a file from Google Drive", options=list(file_names.keys()))

                if selected_file:
                    st.write(f"**You selected:** {selected_file}")
                    file_id = file_names[selected_file]

                    # Display file ID or other details
                    st.write(f"**File ID:** {file_id}")

        else:
            st.error("Failed to connect to Google Drive.")
    else:
        st.info("Click the button to connect to Google Drive.")


if __name__ == '__main__':
    main()
