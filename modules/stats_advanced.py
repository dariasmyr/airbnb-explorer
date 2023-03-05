import base64
import io

from flask import render_template
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database_repository import Database


class Metrics:

    def __init__(self):
        try:
            self.db = Database("sqlite+pysqlite:///:/../data/data.sqlite3")
            self.db.connect()
            self.df = self.db.get_dataframe()
        except Exception as e:
            print(e)

    def show_dataframe(self):
        # show beautiful dataframe with tabulate
        print(tabulate(self.df.head(), headers='keys', tablefmt='psql'))

    def mean_price_per_neighbourhood(self, ax=None):
        # print('Average price of Airbnb listings in each neighbourhood group: ')
        mean_price = self.df.groupby('neighbourhood_group')['price'].mean().sort_values(ascending=False)
        # print(mean_price)

        if ax is None:
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

    def correlation_with_price(self, ax=None):
        # print('Correlation between price and other columns: ')

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

        if ax is None:
            fig, ax = plt.subplots()
        ax.set_title('Correlation between price and other columns')
        ax.set_xlabel('Correlation (price)')
        ax.set_ylabel('Columns')
        ax.barh(correlation_df.index, correlation_df['Correlation'])

        plt.show()

    def heatmap_correlation(self, ax=None):
        numeric_cols = ['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'availability_365']
        if not ax:
            fig, ax = plt.subplots()
        sns.heatmap(self.df[numeric_cols].corr(), annot=True, fmt='.2f', cmap='coolwarm', center=0.0, ax=ax)
        plt.show()
        return ax

    def heatmap_density_of_listings(self, ax=None):
        if not ax:
            fig, ax = plt.subplots()
        sns.heatmap(self.df.groupby(['neighbourhood_group', 'room_type']).size().unstack(fill_value=0), annot=True,
                    fmt='d', cmap='coolwarm', ax=ax)

        plt.title('Density of Listings by Neighborhood Group')
        plt.xlabel('Neighborhood')
        plt.ylabel('Neighborhood Group')

        plt.show()
        return ax

    def most_common_room_type(self, ax=None):
        # Group by neighborhood group and room type, and count the number of occurrences
        room_counts = self.df.groupby(['neighbourhood_group', 'room_type']).size().reset_index(name='count')

        # Get the most common room type for each neighborhood group
        most_common = room_counts.groupby('neighbourhood_group').apply(lambda x: x.loc[x['count'].idxmax()])

        # Create a stacked bar chart with one bar per neighborhood group, showing the count of each room type
        if ax is None:
            fig, ax = plt.subplots()
        sns.barplot(data=most_common, x='neighbourhood_group', y='count', hue='room_type', ax=ax)

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

    def percentage_of_available_listings_from(self, ax=None):
        # print('Percentage of available listings with minimum 10 nights in each neighbourhood group: ')
        available_listings = self.df.groupby('neighbourhood_group')['minimum_nights'].apply(
            lambda x: (x >= 10).sum() / len(x) * 100).apply(lambda x: '%.2f%%' % x)
        # print(available_listings)

        if ax is None:
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
                tick_label=self.df.groupby('neighbourhood_group')['minimum_nights'].count().index, ax=ax)
        ax.set_yticklabels(self.df.groupby('neighbourhood_group')['minimum_nights'].count().index)
        plt.show()

    def unique_host_count(self):
        print('Number of unique hosts in each neighbourhood group: ')
        unique_hosts = self.df.groupby('neighbourhood_group')['host_id'].nunique(dropna=True)
        # print(unique_hosts)

        unique_hosts.plot(kind='bar', color='orange')

        plt.title('Number of unique hosts in each neighbourhood group')
        plt.xlabel('Neighborhood Group')
        plt.ylabel('Number of Unique Hosts')

        plt.show()

    def hosts_with_multiple_listings(self):
        print('Number of hosts with multiple listings in each neighbourhood group: ')
        host_listings = self.df.groupby('host_name')['host_id'].count()

        top_hosts = host_listings.nlargest(10)
        # print(top_hosts)

        top_hosts.plot(kind='bar', color='orange')

        plt.title('Top 10 hosts with multiple listings')
        plt.xlabel('Host ID')
        plt.ylabel('Number of Listings')

        plt.show()

    # Get all the 6 visualizations in one method and render them to svg
    def get_all_visualizations(self):
        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(20, 20))
        self.mean_price_per_neighbourhood(ax=axes[0])
        self.correlation_with_price(ax=axes[1])
        self.heatmap_correlation(ax=axes[2])
        self.heatmap_density_of_listings(ax=axes[3])
        self.most_common_room_type(ax=axes[4])
        self.percentage_of_available_listings_from(ax=axes[5])

        fig.tight_layout()
        svg_io = io.StringIO()
        fig.savefig(svg_io, format='svg', bbox_inches='tight')
        svg_io.seek(0)
        svg_data = svg_io.getvalue().encode('utf-8')
        chart_data = base64.b64encode(svg_data).decode('ascii')

        return chart_data
