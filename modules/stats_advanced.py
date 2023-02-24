import numpy as np
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import seaborn as sns


class Metrics:

    def __init__(self, filename):
        try:
            self.df = pd.read_csv(filename)
        except FileNotFoundError:
            raise FileNotFoundError("CSV file not found!")
        except ValueError:
            raise ValueError("Invalid CSV file!")

    def mean_price_per_heighbourhood(self):
        print('Average price of Airbnb listings in each neighbourhood group: ')
        mean_price = self.df.groupby('neighbourhood_group')['price'].mean().sort_values(ascending=False)
        print(mean_price)

        fig, ax = plt.subplots()
        ax.set_title('Average price of Airbnb listings in each neighbourhood group')
        ax.set_xlabel('Price')
        ax.set_ylabel('Neighbourhood group')

        ax.set_yticks(mean_price.values)
        ax.set_yticklabels(mean_price.index)

        ax.set_xlim([0, mean_price.max() + 10])
        ax.barh(mean_price.index, mean_price.values, color='orange', tick_label=mean_price.index)
        ax.set_yticklabels(mean_price.index)
        plt.show()

    def correlation_with_price(self):
        print('Correlation between price and other columns: ')

        numeric_cols = ['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'availability_365']

        correlation = self.df[numeric_cols].corr()['price'].sort_values(ascending=False)

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

    def most_common_room_type(self):
        # Group by neighborhood group and find the mode of room type
        mode_by_neighborhood = self.df.groupby('neighbourhood_group')['room_type'].agg(pd.Series.mode)
        print(mode_by_neighborhood)

        # Group by neighborhood group and room type, and count the number of occurrences
        room_counts = self.df.groupby(['neighbourhood_group', 'room_type']).size().reset_index(name='count')

        # Get the most common room type for each neighborhood group
        most_common = room_counts.groupby('neighbourhood_group').apply(lambda x: x.loc[x['count'].idxmax()])

        # Create a stacked bar chart with one bar per neighborhood group, showing the count of each room type
        sns.barplot(data=most_common, x='neighbourhood_group', y='count', hue='room_type')

        # Set the chart title and axis labels
        plt.title('Distribution of Room Types by Neighborhood Group')
        plt.xlabel('Neighborhood Group')
        plt.ylabel('Count')

        # Show the chart
        plt.show()

    def avg_number_of_reviews_per_month(self):
        print('Average number of reviews for listings per month in each neighbourhood group: ')
        avg_reviews = self.df.groupby('neighbourhood_group')['reviews_per_month'].mean().sort_values(
            ascending=False).apply(lambda x: '%.2f' % x)
        print(avg_reviews)

    def percentage_of_available_listings_from(self):
        print('Percentage of available listings with minimum 10 nights in each neighbourhood group: ')
        available_listings = self.df.groupby('neighbourhood_group')['minimum_nights'].apply(
            lambda x: (x >= 10).sum() / len(x) * 100).apply(lambda x: '%.2f%%' % x)
        print(available_listings)

        # create a stacked bar chart with number of listings with minimum 10 nights per neighbourhood group
        fig, ax = plt.subplots()
        ax.set_title('Number of listings with minimum 10 nights per neighbourhood group')
        ax.set_xlabel('Neighbourhood group')
        ax.set_ylabel('Number of listings')

        ax.set_yticks(self.df.groupby('neighbourhood_group')['minimum_nights'].count().values)
        ax.set_yticklabels(self.df.groupby('neighbourhood_group')['minimum_nights'].count().index)

        ax.set_xlim([0, self.df.groupby('neighbourhood_group')['minimum_nights'].count().max() + 10])
        ax.barh(self.df.groupby('neighbourhood_group')['minimum_nights'].count().index,
                self.df.groupby('neighbourhood_group')['minimum_nights'].count().values,
                color='orange',
                tick_label=self.df.groupby('neighbourhood_group')['minimum_nights'].count().index)
        ax.set_yticklabels(self.df.groupby('neighbourhood_group')['minimum_nights'].count().index)
        plt.show()

    def unique_host_count(self):
        print('Number of unique hosts in each neighbourhood group: ')
        return self.df.groupby('neighbourhood_group')['host_id'].nunique(dropna=True)

    def hosts_with_multiple_listings(self):
        print('Number of hosts with multiple listings in each neighbourhood group: ')
        return self.df.groupby('neighbourhood_group')['host_id'].apply(lambda x: (x.value_counts() > 3).sum())

    def top_hosts_by_number_of_listings(self):
        print('Top 10 hosts by number of listings in each neighbourhood group: ')
        return self.df.groupby('neighbourhood_group')['host_id'].value_counts().groupby('neighbourhood_group').head(10)