import numpy as np
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import seaborn as sns


class Metrics:

    # The average price of Airbnb listings in each neighbourhood group or neighbourhood.

    def __init__(self, filename):
        try:
            self.df = pd.read_csv(filename)
        except FileNotFoundError:
            raise FileNotFoundError("CSV file not found!")
        except ValueError:
            raise ValueError("Invalid CSV file!")

    def mean_price(self):
        print('Average price of Airbnb listings in each neighbourhood group: ')
        return self.df.groupby('neighbourhood_group')['price'].mean().apply(lambda x: '%.2f$' % x)

    def most_common_room_type(self):
        print('The most common room types in each neighbourhood group: ')
        return self.df.groupby('neighbourhood_group')['room_type'].agg(pd.Series.mode)

    def avg_number_of_reviews_per_month(self):
        print('Average number of reviews for listings per month in each neighbourhood group: ')
        return self.df.groupby('neighbourhood_group')['reviews_per_month'].mean().apply(lambda x: '%.2f' % x)

    def percentage_of_available_listings_from(self):
        print('Percentage of available listings with minimum 10 nights in each neighbourhood group: ')
        return self.df.groupby('neighbourhood_group')['minimum_nights'].apply(lambda x: (x >= 10).sum() / len(x) * 100).apply(lambda x: '%.2f%%' % x)

    def unique_host_count(self):
        print('Number of unique hosts in each neighbourhood group: ')
        return self.df.groupby('neighbourhood_group')['host_id'].nunique(dropna=True)

    def hosts_with_multiple_listings(self):
        print('Number of hosts with multiple listings in each neighbourhood group: ')
        return self.df.groupby('neighbourhood_group')['host_id'].apply(lambda x: (x.value_counts() > 3).sum())

    def top_hosts_by_number_of_listings(self):
        print('Top 10 hosts by number of listings in each neighbourhood group: ')
        return self.df.groupby('neighbourhood_group')['host_id'].value_counts().groupby('neighbourhood_group').head(10)

    def correlation_with_price(self):
        print('Correlation between price and other columns: ')
        correlation = self.df.corr()['price'].sort_values(ascending=False)

        corr_explanation = []
        for corr_value in correlation:
            if corr_value > 0.5:
                corr_explanation.append('Strong positive correlation')
            elif corr_value > 0:
                corr_explanation.append('Positive correlation')
            elif corr_value == 0:
                corr_explanation.append('No correlation')
            elif corr_value < -0.5:
                corr_explanation.append('Strong negative correlation')
            elif corr_value < 0:
                corr_explanation.append('Negative correlation')
            else:
                corr_explanation.append('Invalid correlation value')

        correlation_df = pd.DataFrame({'Correlation': correlation, 'Explanation': corr_explanation})
        print(correlation_df)
        fig, ax = plt.subplots()
        ax.set_title('Correlation between price and other columns')
        ax.set_xlabel('Correlation (price)')
        ax.set_ylabel('Columns')
        ax.barh(correlation_df.index, correlation_df['Correlation'])
        plt.show()




