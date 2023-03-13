import pandas as pd


class DataFormatter:

    def __init__(self):
        try:
            self.df = pd.read_csv('data/raw_data.csv')
        except Exception as e:
            print(e)

    def get_dataframe(self):
        """
        Return the DataFrame object.
        """
        print('Dataframe: \n', self.df.head())

    def get_datatypes(self):
        # Return the table with datatypes and their number of occurrences
        print('Datatypes: \n', self.df.dtypes.value_counts())

    def drop_missing_values(self):
        """
        Drop the rows with missing values in the DataFrame.
        """
        # try to drop the rows with missing values
        try:
            print("Dropping rows with missing values...")
            self.df = self.df.dropna()
            print("Rows with missing values dropped successfully!")
        # if there are no missing values, print a message
        except ValueError:
            print("No missing values!")

    def save_cleared_data(self, new_filename):
        """
        Save the cleared DataFrame to a CSV file with the given filename.

        Args:
            new_filename (str): Name of the CSV file to save the cleared DataFrame to.

        Raises:
            ValueError: If the file with the given filename is not a valid CSV file.
        """
        try:
            print("Saving cleared data to CSV file...")
            self.df.to_csv(new_filename, index=False)
            print("Cleared data saved successfully!")
        except ValueError:
            print("Invalid CSV file!")


