import pandas as pd

from modules.database_repository import Database


class DataFormatter:

    def __init__(self):
        try:
            self.db = Database("sqlite+pysqlite:///:/../data/data.sqlite3")
            self.db.connect()
            self.df = self.db.get_dataframe()
        except Exception as e:
            print(e)

    def get_dataframe(self):
        """
        Return the DataFrame object.
        """
        print('Dataframe: ', self.df)
        return self.df

    def get_datatypes(self):
        """
        Return the data types of the columns in the DataFrame.
        """
        print('Data types: ', self.df.dtypes)
        return self.df.dtypes

    def check_missing_values(self):
        """
        Return a boolean DataFrame indicating which values in the DataFrame are missing.
        """
        print('Number of rows with missing values: ', self.df.isnull().sum())
        return self.df.isnull()

    def drop_missing_values(self):
        """
        Drop the rows with missing values in the DataFrame.
        """
        # try to drop the rows with missing values
        try:
            self.df = self.df.dropna()
        # if there are no missing values, print a message
        except ValueError:
            print("No missing values!")

    def get_missing_values_after_drop(self):
        """
        Return a boolean DataFrame indicating the presence of missing values after the rows with missing values have been dropped.
        """
        print('Number of rows with missing values after drop: ', self.df.isnull().sum())
        return self.df.isnull()

    def save_cleared_data(self, new_filename):
        """
        Save the cleared DataFrame to a CSV file with the given filename.

        Args:
            new_filename (str): Name of the CSV file to save the cleared DataFrame to.

        Raises:
            ValueError: If the file with the given filename is not a valid CSV file.
        """
        try:
            self.df.to_csv(new_filename, index=False)
        except ValueError:
            raise ValueError("Invalid CSV file!")
