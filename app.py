import streamlit as st
import data_function as fun
from streamlit_ydata_profiling import st_profile_report

st.set_page_config(layout="wide")

if 'uploaded' not in st.session_state:
    st.session_state.uploaded = False

if 'data' not in st.session_state:
    st.session_state.data = None


def show_data(data):
    return data.head(10)


def profile_report(data):
    return fun.get_data_profile_report(data)


def get_chart(data, chart_type, measure, dimension):
    try:
        if chart_type == 'Bar Chart':
            return st.bar_chart(data, x=dimension[0], y=measure[0])
        elif chart_type == 'Scatter Chart':
            return st.scatter_chart(data, x=measure[0], y=measure[1])
        elif chart_type == 'Line Chart':
            return st.line_chart(data, x=measure[0], y=measure[1])
        elif chart_type == 'Select Chart type':
            return st.warning('Select chart type')
        else:
            return st.error(f'Chart type {chart_type} not supported')
    except Exception as e:
        return st.error(f'Error:  Choose Correct Measure, Dimension and Corresponding Chat Type')


st.title('Welcome to TabAI')

st.sidebar.button(label='Data Source')

uploaded_file = st.file_uploader('Choose a CSV file', type=['csv', 'xlsx'])

if uploaded_file is not None and not st.session_state.uploaded:
    try:
        if uploaded_file.name.endswith('.csv'):
            data = fun.read_data(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            data = fun.read_data(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a CSV or Excel file.")

        st.session_state.data = data
        st.session_state.uploaded = True

    except Exception as e:
        st.error(f"An error occurred: {e}")

if st.sidebar.button(label='View Data'):
    st.session_state.button_clicked = False
    st.write('Here is 10 Rows of Your data')
    st.dataframe(show_data(st.session_state.data))

if st.sidebar.button(label='View Profile'):
    st.session_state.button_clicked = False
    st.write('Here Your Data Profile Report')
    st_profile_report(profile_report(st.session_state.data))

if st.sidebar.button(label='Ask Question'):
    st.session_state.button_clicked = False
    with st.chat_message("User"):
        st.write("Welcome to TabAI")
        st.write("This functionality Under Development")

    st.chat_input("Say Something")


if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

if st.sidebar.button(label='VizAI'):
    st.session_state.button_clicked = True

if st.session_state.button_clicked:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader('Measure')
        measure_columns = st.multiselect('Select Measure', fun.get_measure_columns(st.session_state.data))

    with col2:
        st.subheader('Dimension')
        dimension_columns = st.multiselect('Select Dimension', fun.get_dimension_columns(st.session_state.data))

    with col3:
        st.subheader('Chart Type')
        chart_type = st.selectbox('Select Chart Type', ['Select Chart type','Bar Chart', 'Line Chart', 'Scatter Plot'])

    with st.container():
        get_chart(st.session_state.data, chart_type, measure_columns, dimension_columns)