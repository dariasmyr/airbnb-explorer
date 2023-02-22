from modules.cleaner import DataFormatter

filename = 'data/raw_data.csv'
new_filename = 'data/cleared_data.csv'


def clean_data():
    data_formatter = DataFormatter(filename)
    data_formatter.get_dataframe()
    data_formatter.get_datatypes()
    data_formatter.check_missing_values()
    data_formatter.drop_missing_values()
    data_formatter.get_missing_values_after_drop()
    data_formatter.save_cleared_data(new_filename)
