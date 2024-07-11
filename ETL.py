import data_utility as du
import data_cleaning as dc


def extract_data_from_file(file):
    return du.get_data_from_files(file)


def transform_data(data):
    data = dc.remove_null_values(data)
    data = dc.remove_duplicates(data)
    data = dc.remove_leading_trailing_whitespace(data)
    return data


# comment: trial