import streamlit as st
import data_utility as du
from streamlit_ydata_profiling import st_profile_report

st.set_page_config(layout="wide")

if 'uploaded' not in st.session_state:
    st.session_state.uploaded = False

if 'data' not in st.session_state:
    st.session_state.data = None


def show_data(data):
    return data.head(10)


def profile_report(data):
    return du.get_data_profile_report(data)


st.title('Welcome to TabAI')

uploaded_file = st.file_uploader('Choose a CSV file', type=['csv', 'xlsx'])

if uploaded_file is not None and not st.session_state.uploaded:
    try:
        if uploaded_file.name.endswith('.csv'):
            data = du.get_data_from_files(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            data = du.get_data_from_files(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a CSV or Excel file.")

        st.session_state.data = data
        st.session_state.uploaded = True

    except Exception as e:
        st.error(f"An error occurred: {e}")

if st.sidebar.button(label='View Data'):
    st.write('Here is 10 Rows of Your data')
    st.dataframe(show_data(st.session_state.data))

if st.sidebar.button(label='View Profile'):
    st.write('Here Your Data Profile Report')
    st_profile_report(profile_report(st.session_state.data))

if st.sidebar.button(label='Ask Question'):
    with st.chat_message("User"):
        st.write("Welcome to TabAI")
        st.write("This functionality Under Development")

    st.chat_input("Say Something")

if st.sidebar.button(label='VizAI'):
    st.write('This functionality Under Development')