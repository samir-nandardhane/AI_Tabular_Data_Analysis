import pandas as pd


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
