# checking null values
# checking duplicate values
# for text data remove leading and trailing whitespace

def check_null_values(data):
    null_columns = data[data.isnull().any()].tolist()
    null_columns_count = len(null_columns)
    return null_columns_count, null_columns, data[null_columns].isnull().sum()


def remove_null_values(data):
    return data.dropna()


def remove_leading_trailing_whitespace(data):
    data = data.apply(lambda col: col.str.strip() if col.dtype == 'object' else col)
    return data


def remove_duplicates(data):
    return data.drop_duplicates()