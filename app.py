import time

import streamlit as st
import openai
import pandas as pd
import data_function as fun
from streamlit_ydata_profiling import st_profile_report
import data_ai  # Ensure this module provides the necessary functionality


def profile_report(data):
    return fun.get_data_profile_report(data)


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

# Sidebar for navigation with blue buttons
with st.sidebar:
    if st.button("Upload Data", key="upload_data_button"):
        st.session_state.page = "Upload Data"

    if st.button("Chat", key="chat_button"):
        st.session_state.page = "Chat"

    if st.button("View Report", key="report_button"):
        st.session_state.page = "View Report"

    if st.button("View Data", key="view_data_button"):
        st.session_state.page = "View Data"

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

elif st.session_state.page == "Chat":
    st.title("Chat with Assistant")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    with st.chat_message("assistant"):
        st.write("Welcome to TabAI")

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