from utility import data_cleaning as dc, data_utility as du
from ydata_profiling import ProfileReport


def read_data(file):
    return du.get_data_from_files(file)


def clean_data(data):
    data = dc.remove_null_values(data)
    data = dc.remove_duplicates(data)
    #data = dc.remove_leading_trailing_whitespace(data)
    return data


def get_data_profile_report(data):
    data = clean_data(data)
    return ProfileReport(data)


def get_measure_columns(data):
    return data.select_dtypes(exclude='object').columns.tolist()


def get_dimension_columns(data):
    return data.select_dtypes(include='object').columns.tolist()