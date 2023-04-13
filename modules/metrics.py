import plotly.graph_objs as go
import plotly.offline as pyo
import pandas as pd
from modules.database_repository import Database

pyo.init_notebook_mode(connected=True)


class Metrics:

    def __init__(self):
        try:
            self.db = Database("sqlite+pysqlite:///:/../data/database.sqlite3")
            self.db.connect()
            self.df = self.db.get_dataframe()
        except Exception as e:
            print(e)

    def mean_price_per_neighbourhood(self):
        mean_price = self.df.groupby('neighbourhood_group')['price'].mean().sort_values(ascending=False)
        trace = go.Bar(x=mean_price.values, y=mean_price.index, orientation='h', marker=dict(color='orange'))

        fig = go.Figure()
        fig.add_trace(trace)
        fig.update_layout(title='Average price of Airbnb listings in each neighbourhood group', xaxis_title='Price',
                          yaxis_title='Neighbourhood group', yaxis_range=[mean_price.index[-1], mean_price.index[0]])

        pyo.iplot(fig)

        html = fig.to_html(full_html=False)
        return html

    def correlation_with_price(self):

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

        trace = go.Bar(x=correlation_df['Correlation'], y=correlation_df.index, orientation='h',
                       marker=dict(color='orange'))

        fig = go.Figure()
        fig.add_trace(trace)
        fig.update_layout(title='Correlation between price and other columns', xaxis_title='Correlation (price)',
                          yaxis_title='Columns')

        pyo.iplot(fig)

        html = fig.to_html(full_html=False)
        return html

    def heatmap_correlation(self):
        numeric_cols = ['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'availability_365']
        data = go.Heatmap(z=self.df[numeric_cols].corr(), x=numeric_cols, y=numeric_cols, colorscale='agsunset',
                          zmin=-1, zmax=1)

        fig = go.Figure(data=[data], layout=go.Layout(title='Correlation between columns'))

        pyo.iplot(fig)

        html = fig.to_html(full_html=False)
        return html

    def heatmap_density_of_listings(self):
        data = []
        for ng in self.df['neighbourhood_group'].unique():
            df_ng = self.df[self.df['neighbourhood_group'] == ng]
            for rt in df_ng['room_type'].unique():
                df_rt = df_ng[df_ng['room_type'] == rt]
                data.append(go.Heatmap(z=[[df_rt.shape[0]]], x=[rt], y=[ng], colorscale='agsunset', zmin=0))

        fig = go.Figure(data=data, layout=go.Layout(title='Density of listings by neighbourhood group and room type'))

        pyo.iplot(fig)

        html = fig.to_html(full_html=False)
        return html

    def most_common_room_type(self):
        # Group by neighborhood group and room type, and count the number of occurrences
        room_counts = self.df.groupby(['neighbourhood_group', 'room_type']).size().reset_index(name='count')

        # Get the most common room type for each neighborhood group
        most_common = room_counts.groupby('neighbourhood_group').apply(lambda x: x.loc[x['count'].idxmax()])

        # Create a stacked bar chart with one bar per neighborhood group, showing the count of each room type
        trace1 = go.Bar(x=most_common['neighbourhood_group'],
                        y=most_common[most_common['room_type'] == 'Entire home/apt']['count'], name='Entire home/apt')
        trace2 = go.Bar(x=most_common['neighbourhood_group'],
                        y=most_common[most_common['room_type'] == 'Private room']['count'], name='Private room')
        trace3 = go.Bar(x=most_common['neighbourhood_group'],
                        y=most_common[most_common['room_type'] == 'Shared room']['count'], name='Shared room')

        data = [trace1, trace2, trace3]

        fig = go.Figure(data=data, layout=go.Layout(title='Most common room type in each neighbourhood group',
                                                    barmode='stack'))
        pyo.iplot(fig)

        html = fig.to_html(full_html=False)
        return html

    def avg_number_of_reviews_per_month(self):
        print('Average number of reviews for listings per month in each neighbourhood group: ')
        avg_reviews = self.df.groupby('neighbourhood_group')['reviews_per_month'].mean().sort_values(
            ascending=False).apply(lambda x: '%.2f' % x)
        print(avg_reviews)

    def percentage_of_available_listings_from(self):
        # Calculate the percentage of listings with minimum 10 nights per neighborhood group
        available_listings = self.df.groupby('neighbourhood_group')['minimum_nights'].apply(
            lambda x: (x >= 10).sum() / len(x) * 100).sort_values(ascending=False)

        # Create a horizontal bar chart showing the percentage of listings with minimum 10 nights per neighborhood group
        trace = go.Bar(x=available_listings.values, y=available_listings.index, orientation='h',
                       marker=dict(color='orange'))

        data = [trace]
        layout = go.Layout(title='Percentage of available listings with minimum 10 nights in each neighborhood group')

        fig = go.Figure(data=data, layout=layout)

        pyo.iplot(fig)

        html = fig.to_html(full_html=False)
        return html

    def unique_host_count(self):
        unique_hosts = self.df.groupby('neighbourhood_group')['host_id'].nunique(dropna=True)

        trace = go.Bar(x=unique_hosts.index, y=unique_hosts.values, marker=dict(color='orange'))

        fig = go.Figure()
        fig.add_trace(trace)
        fig.update_layout(title='Number of unique hosts in each neighbourhood group', xaxis_title='Neighborhood Group',
                          yaxis_title='Number of Unique Hosts')

        fig.show()

        html = fig.to_html(full_html=False)
        return html

    def hosts_with_multiple_listings(self):
        host_listings = self.df.groupby('host_name')['host_id'].count()

        top_hosts = host_listings.nlargest(10)

        trace = go.Bar(x=top_hosts.index, y=top_hosts.values, marker=dict(color='orange'))

        fig = go.Figure()
        fig.add_trace(trace)
        fig.update_layout(title='Top 10 hosts with multiple listings', xaxis_title='Host ID',
                          yaxis_title='Number of Listings')

        pyo.iplot(fig)

        html = fig.to_html(full_html=False)
        return html
