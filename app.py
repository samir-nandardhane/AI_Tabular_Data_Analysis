import streamlit as st
import openai
import pandas as pd
from googleapiclient.http import MediaIoBaseDownload

from utility import data_function as fun
from streamlit_ydata_profiling import st_profile_report
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def profile_report(data):
    return fun.get_data_profile_report(data)

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


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

def list_drive_files():
    creds = get_token()
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(pageSize=50).execute()
    return {file['name']: file['id'] for file in results.get('files', [])}
# Initialize the OpenAI API key
# Add your open ai key here Statement here

conversation_history = []

# Initialize session state for messages, data, and page selection
if "messages" not in st.session_state:
    st.session_state.messages = []
if "data" not in st.session_state:
    st.session_state.data = None
if "page" not in st.session_state:
    st.session_state.page = "Upload Data"
if "selected_file_id" not in st.session_state:
    st.session_state.selected_file_id = None
if "selected_file_name" not in st.session_state:
    st.session_state.selected_file_name = None
if "file_confirmed" not in st.session_state:
    st.session_state.file_confirmed = False


st.title("AI Tabular Data Analysis")

# Sidebar for navigation with blue buttons
with st.sidebar:
    if st.button("Upload Data", key="upload_data_button"):
        st.session_state.page = "Upload Data"

    if st.button("Start Chat", key="chat_button"):
        st.session_state.page = "Start Chat"

    if st.button("View Report", key="report_button"):
        st.session_state.page = "View Report"

    if st.button("View Data", key="view_data_button"):
        st.session_state.page = "View Data"
    if st.sidebar.button("Drive File Selection", key="drive_file_button"):
        st.session_state.page = "Drive File Selection"

# Display content based on the selected page
if st.session_state.page == "Upload Data":
    # File uploader for CSV or Excel files
    uploaded_file = st.file_uploader("Attach a file (CSV or Excel)", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format.")
            st.stop()

        st.session_state.data = fun.clean_data(df)  # Store the DataFrame in session state
        st.write("File uploaded successfully.")

elif st.session_state.page == "Drive File Selection":
    st.title("Drive File Selection")

    if st.button("Connect to Google Drive"):
        files = list_drive_files()
        if files:
            st.session_state.drive_files = files
            st.title("Connected to Google Drive")
        else:
            st.error("No files found or connection failed.")

    if "drive_files" in st.session_state:
        selected_file = st.selectbox("Choose a file from Google Drive:",
                                     options=list(st.session_state.drive_files.keys()))
        st.session_state.selected_file_name = selected_file
        st.session_state.selected_file_id = st.session_state.drive_files[selected_file]

    if st.session_state.selected_file_name and st.button("Use This File"):
        st.session_state.file_confirmed = True
        st.write(f"File selected: {st.session_state.selected_file_name}")

        creds = get_token()
        service = build('drive', 'v3', credentials=creds)
        file_id = st.session_state.selected_file_id

        file_request = service.files().get_media(fileId=file_id)
        file_path = f"{st.session_state.selected_file_name}"
        with open(file_path, "wb") as f:
            downloader = MediaIoBaseDownload(f, file_request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            st.write(f"Downloaded {st.session_state.selected_file_name}.")

        if file_path.endswith(".csv"):
            st.session_state.data = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            st.session_state.data = pd.read_excel(file_path)


elif st.session_state.page == "Start Chat":
    st.title("Chat with Assistant")

    with st.chat_message("assistant"):
        st.write("Welcome to TabAI")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for user prompts
    prompt = st.chat_input("Ask a question about the attached file or anything else")
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add a spinner for processing
        with st.spinner("Processing..."):
            # Check if data is uploaded
            if st.session_state.data is not None:
                df = st.session_state.data
                try:
                    # Get the response from df.ask(prompt)
                    result = df.ask(prompt)

                    response_text = result

                    # Format the response using OpenAI
                    openai_response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user",
                             "content": f"Given the user's input: '{prompt}' and the data's response: '{response_text}', please generate a well-structured and informative response."}
                        ]
                    )
                    response_text = openai_response.choices[0].message.content

                    # Display assistant text response
                    with st.chat_message("assistant"):
                        st.markdown(response_text)

                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    conversation_history.append(response_text)

                except AttributeError:
                    response_text = "The data_ai module does not provide the 'ask' method."
                    with st.chat_message("assistant"):
                        st.markdown(response_text)

                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    conversation_history.append(response_text)

            else:
                # If no data is uploaded, handle general prompts using OpenAI API
                try:
                    openai_response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    response_text = openai_response.choices[0].message.content
                    with st.chat_message("assistant"):
                        st.markdown(response_text)

                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    conversation_history.append(response_text)
                except Exception as e:
                    response_text = f"Error with OpenAI API: {e}"
                    with st.chat_message("assistant"):
                        st.markdown(response_text)

                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    conversation_history.append(response_text)

elif st.session_state.page == "View Report":
    st.title('Profile Report')
    st_profile_report(profile_report(st.session_state.data))

elif st.session_state.page == "View Data":
    st.dataframe(st.session_state.data)