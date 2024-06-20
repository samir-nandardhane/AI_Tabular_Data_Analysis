import ETL as etl

filepath = "D:\\Datasets\\test.csv"

data = etl.extract_data_from_file(filepath)

data = etl.transform_data(data)

print(data.head())