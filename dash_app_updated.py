# Run this app with `python dash_app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import plotly.express as px
from dash import Dash, dcc, html
from modules.database_repository import Database
import dash_bootstrap_components as dbc

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    'https://fonts.googleapis.com/css?family=Roboto+Slab&display=swap'
]

# Initialize the app
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Initialize the database connection
database = Database("sqlite+pysqlite:///:/../data/data.sqlite3")
database.connect()

# Define the color scheme and shared visual properties
colors = {
    'background': '#ffffff',
    'text': '#444444',
    'accent': '#008080',
}

style = {
    'page': {
        'margin': '0px 200px 0px 200px',
        'maxWidth': '1200px',
        'padding': '0px 0px 0px 0px',
        'backgroundColor': colors['background'],
        'boxShadow': '0px 0px 20px 0px rgba(0,0,0,0.05)',
        'border-radius': '20px',
        'fontFamily': 'Roboto Slab, sans-serif',
    },
    'title': {
        'font': {
            'size': 20,
            'color': colors['text'],
            'family': 'Roboto Slab, sans-serif'
        },
        'x': 0.5,
        'y': 0.9,
    },
    'axis_title': {
        'font': {
            'size': 18,
            'color': colors['text'],
            'family': 'Roboto Slab, sans-serif'
        },
    },
    'text': {
        'color': colors['text'],
        'font': {
            'size': 24,
            'family': 'Roboto Slab, sans-serif'
        },
    },
    'h1': {
        'textAlign': 'left',
        'color': colors['text'],
        'font': {
            'size': 48,
            'weight': 'bold',
            'family': 'Roboto Slab, sans-serif'
        },
        'padding': '40px 0px 20px 20px'
    },
    'p': {
        'textAlign': 'left',
        'padding': '0px 0px 20px 20px'
    },
    'graph': {
        'padding': '0px 20px 20px 20px'
    }
}

# Retrieve data from the database
df = database.get_dataframe()

# Compute the mean price per neighbourhood group
mean_price_per_neighbourhood = df.groupby('neighbourhood_group')['price'].mean().sort_values(ascending=False)

# Create the bar chart
mean_price_per_neighbourhood_fig = px.bar(
    mean_price_per_neighbourhood,
    x=mean_price_per_neighbourhood.values,
    y=mean_price_per_neighbourhood.index,
    orientation='h',
    color_discrete_sequence=[colors['accent']],
)

# Customize the layout of the chart
mean_price_per_neighbourhood_fig.update_layout(
    title={
        'text': 'Average price of Airbnb listings in each neighbourhood group',
        **style['title']
    },
    xaxis_title={
        'text': 'Price',
        **style['axis_title']
    },
    yaxis_title={
        'text': 'Neighbourhood group',
        **style['axis_title']
    },
    yaxis_range=[mean_price_per_neighbourhood.index[-1], mean_price_per_neighbourhood.index[0]],
    margin=dict(t=100),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
)

numeric_cols = ['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'availability_365']

correlation_with_price = df[numeric_cols].corr()['price'].sort_values(ascending=False)

# Create the bar chart
correlation_with_price_fig = px.bar(
    correlation_with_price,
    x=correlation_with_price.values,
    y=correlation_with_price.index,
    orientation='h',
    color_discrete_sequence=[colors['accent']],
)

# Customize the layout of the chart
correlation_with_price_fig.update_layout(
    title={
        'text': 'Correlation with price',
        **style['title']
    },
    xaxis_title={
        'text': 'Correlation',
        **style['axis_title']
    },
    yaxis_title={
        'text': 'Feature',
        **style['axis_title']
    },
    yaxis_range=[correlation_with_price.index[-1], correlation_with_price.index[0]],
    margin=dict(t=100),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
)

# Define the app layout
app.layout = html.Div(style=style['page'], children=[
    html.Div([
        html.H1(
            children='Welcome to the Airbnb Explorer!',
            style=style['h1']
        ),
        html.P(
            children='The Airbnb Explorer project aims to provide users with insights into Airbnb listings in New '
                     'York City. '
                     'By analyzing data on Airbnb listings, this project helps users find the perfect rental for '
                     'their needs.',
            style=style['p']
        ),
    ]),
    html.Div([
        dcc.Graph(
            id='mean_price_per_neighbourhood',
            figure=mean_price_per_neighbourhood_fig,
            style=style['graph']
        ),
    ]),
    html.Div([
        html.P(
            children='This project is part of the Data Science for Social Good program at the University of Zurich.',
            style=style['p']
        ),
    ]),
    html.Div([
        dcc.Graph(
            id='correlation_with_price',
            figure=correlation_with_price_fig,
            style=style['graph']
        ),
    ]),
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
