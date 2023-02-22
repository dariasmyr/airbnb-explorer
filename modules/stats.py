import pandas as pd
import statistics
import matplotlib.pyplot as plt
import seaborn as sns


class DescriptiveStatistics:

    def __init__(self, filename):
        try:
            self.df = pd.read_csv(filename).select_dtypes(include=['int64', 'float64'])
        except FileNotFoundError:
            raise FileNotFoundError("CSV file not found!")
        except ValueError:
            raise ValueError("Invalid CSV file!")

    def set_data_type(self):
        """
        Change the data type of the columns in the DataFrame.
        """
        self.df['id'] = self.df['id'].astype('int64')
        self.df['host_id'] = self.df['host_id'].astype('int64')
        self.df['latitude'] = self.df['latitude'].astype('float64')
        self.df['longitude'] = self.df['longitude'].astype('float64')
        self.df['price'] = self.df['price'].astype('int64')
        self.df['minimum_nights'] = self.df['minimum_nights'].astype('int64')
        self.df['number_of_reviews'] = self.df['number_of_reviews'].astype('int64')
        self.df['reviews_per_month'] = self.df['reviews_per_month'].astype('float64')
        self.df['calculated_host_listings_count'] = self.df['calculated_host_listings_count'].astype('int64')
        self.df['availability_365'] = self.df['availability_365'].astype('int64')
        print('Dataframe after changing data types: ', self.df)
        return self.df

    # calculate mean for columns of a proper data type
    def mean(self):
        try:
            # explain what is mean and how it is calculated
            print(
                'Mean is the average of all the values in a column. It is calculated by adding all the values in a column and dividing the sum by the number of values in the column.')
            return self.df.apply(statistics.mean).apply(lambda x: '%.2f' % x)
        except statistics.StatisticsError:
            print('No numeric columns found!')
            pass

    def median(self):
        try:
            # explain what is median and how it is calculated
            print(
                'Median is the middle value of a column. It is calculated by sorting the values in a column and taking the middle value.')
            return self.df.apply(statistics.median).apply(lambda x: '%.2f' % x)
        except statistics.StatisticsError:
            print('No numeric columns found!')
            pass

    def mode(self):
        try:
            # explain what is mode and how it is calculated
            print('Mode is the most common value in a column. It is calculated by sorting the values in a column and '
                  'taking the most common value.')
            return self.df.apply(statistics.mode).apply(lambda x: '%.2f' % x)
        except statistics.StatisticsError:
            print('No numeric columns found!')
            pass

    def range(self):
        try:
            # explain what is range and how it is calculated
            print('Range is the difference between the highest and lowest values in a column. It is calculated by '
                  'subtracting the lowest value from the highest value.')
            return self.df.apply(lambda col: max(col) - min(col)).apply(lambda x: '%.2f' % x)
        except ValueError:
            print('No numeric columns found!')
            pass

    def stdev(self):
        try:
            # explain what is standard deviation and how it is calculated
            print('Standard deviation is a measure of how spread out the values in a column are. It is calculated by '
                  'taking the square root of the variance.')
            return self.df.apply(statistics.stdev).apply(lambda x: '%.2f' % x)
        except statistics.StatisticsError:
            print('No numeric columns found!')
            pass

    def variance(self):
        try:
            # explain what is variance and how it is calculated
            print('Variance is a measure of how spread out the values in a column are. It is calculated by taking the '
                  'average of the squared differences from the mean.')
            return self.df.apply(statistics.variance).apply(lambda x: '%.2f' % x)
        except statistics.StatisticsError:
            print('No numeric columns found!')
            pass


class DistributionStatistics:
    def __init__(self, filename):
        try:
            self.df = pd.read_csv(filename).select_dtypes(include=['int64', 'float64'])
        except FileNotFoundError:
            raise FileNotFoundError("CSV file not found!")
        except ValueError:
            raise ValueError("Invalid CSV file!")

    def create_histogram(self, column_name):
        """
            Create a histogram to visualize the distribution of a variable.
            """
        try:
            sns.histplot(data=self.df, x=column_name, kde=False)
            plt.show()
        except ValueError:
            print('Column not found or is not numeric!')
            pass

    def create_density_plot(self, column_name):
        """
            Create a density plot to visualize the distribution of a variable.
            """
        try:
            sns.kdeplot(data=self.df, x=column_name)
            plt.show()
        except ValueError:
            print('Column not found or is not numeric!')
            pass
