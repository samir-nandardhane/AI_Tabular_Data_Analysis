import pandas as pd
import data_cleaning as dc
from ydata_profiling import ProfileReport


def get_data_from_files(filename, **kwargs):
    if filename.name.endswith('.csv'):
        return pd.read_csv(filename, **kwargs)
    elif filename.name.endswith('.json'):
        return pd.read_json(filename, **kwargs)
    elif filename.name.endswith('.xlsx'):
        return pd.read_excel(filename, **kwargs)
    elif filename.name.endswith('.parquet'):
        return pd.read_parquet(filename, **kwargs)
    else:
        return print("Sorry!! Current Given File Format Not Accepted")


def get_data_profile_report(data):
    data = dc.remove_null_values(data)
    data = dc.remove_duplicates(data)
    data = dc.remove_leading_trailing_whitespace(data)
    return ProfileReport(data)
