import numpy as np
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import seaborn as sns

from modules.database_repository import Database


class DescriptiveStatistics:

    def __init__(self):
        try:
            self.db = Database("sqlite+pysqlite:///:/../data/data.sqlite3")
            self.db.connect()
            self.df = self.db.get_dataframe()
        except Exception as e:
            print(e)

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
                'Mean is the average of all the values in a column. It is calculated by adding all the values in a '
                'column and dividing the sum by the number of values in the column.')
            return self.df.apply(statistics.mean).apply(lambda x: '%.2f' % x)
        except statistics.StatisticsError:
            print('No numeric columns found!')
            pass

    def median(self):
        try:
            # explain what is median and how it is calculated
            print(
                'Median is the middle value of a column. It is calculated by sorting the values in a column and '
                'taking the middle value.')
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
    def __init__(self):
        try:
            self.db = Database("sqlite+pysqlite:///:/../data/data.sqlite3")
            self.db.connect()
            self.df = self.db.get_dataframe()
        except Exception as e:
            print(e)

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


class CorrelationStatistics:
    def __init__(self):
        try:
            self.db = Database("sqlite+pysqlite:///:/../data/data.sqlite3")
            self.db.connect()
            self.df = self.db.get_dataframe()
        except Exception as e:
            print(e)

    def create_correlation(self, column1, column2):
        """
        Calculate the Pearson correlation coefficient between two columns.
        """
        correlation_coefficient = self.df[column1].corr(self.df[column2], method='pearson')
        # Explain what is Pearson correlation coefficient and how it is calculated
        print('Correlation coefficients are used to assess the strength of associations between data variables. '
              'Pearson correlation coefficient is a measure of the strength of the linear relationship between two '
              'variables. It is calculated by dividing the covariance of the two variables by the product of their '
              'standard deviations.')
        print('Pearson correlation coefficient between', column1, 'and', column2, 'is', correlation_coefficient)
        return correlation_coefficient

    def create_heatmap(self):
        """
        Create a heatmap to visualize the correlation between variables.
        """
        try:
            sns.heatmap(self.df.corr(), annot=True)
            plt.show()
        except ValueError:
            print('Column not found or is not numeric!')
            pass

    def create_scatterplot(self, column1, column2):
        """
        Create a scatterplot to visualize the relationship between two variables.
        """
        try:
            sns.scatterplot(data=self.df, x=column1, y=column2)
            plt.show()
        except ValueError:
            print('Column not found or is not numeric!')
            pass

    def create_lineplot(self, column1, column2):
        """
        Create a lineplot to visualize the relationship between two variables.
        """
        try:
            sns.lineplot(data=self.df, x=column1, y=column2)
            plt.show()
        except ValueError:
            print('Column not found or is not numeric!')
            pass

    def create_boxplot(self, column1, column2):
        """
        Create a boxplot to visualize the relationship between two variables.
        """
        try:
            sns.boxplot(data=self.df, x=column1, y=column2)
            plt.show()
        except ValueError:
            print('Column not found or is not numeric!')
            pass

    def create_matrixplot(self, column1, column2):
        """
        Create a matrixplot to visualize the relationship between two variables.
        """
        try:
            sns.pairplot(data=self.df, x_vars=column1, y_vars=column2)
            plt.show()
        except ValueError:
            print('Column not found or is not numeric!')
            pass


class TepmoralStatistics:
    def __init__(self):
        try:
            self.db = Database("sqlite+pysqlite:///:/../data/data.sqlite3")
            self.db.connect()
            self.df = self.db.get_dataframe()
        except Exception as e:
            print(e)

    def plot_availability_365(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        self.df.plot(x='last_review', y='availability_365', ax=ax)
        ax.set_xlabel('Last Review')
        ax.set_ylabel('Availability 365')
        ax.set_title('Availability 365 Over Time')
        plt.show()

    def plot_last_review_vs_num_reviews(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        self.df.plot(kind='scatter', x='last_review', y='number_of_reviews', ax=ax)
        ax.set_xlabel('Last Review')
        ax.set_ylabel('Number of Reviews')
        ax.set_title('Last Review vs. Number of Reviews')
        plt.show()

    def plot_num_reviews_heatmap(self):
        # Extract year and month from last_review
        self.df['year'] = pd.DatetimeIndex(self.df['last_review']).year
        self.df['month'] = pd.DatetimeIndex(self.df['last_review']).month

        # Pivot table to count number of reviews by year and month
        review_counts = self.df.pivot_table(index='year', columns='month',
                                            values='number_of_reviews', aggfunc=np.sum)

        # Create heatmap
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(review_counts, cmap='Blues', ax=ax)
        ax.set_xlabel('Month')
        ax.set_ylabel('Year')
        ax.set_title('Number of Reviews by Year and Month')
        plt.show()
