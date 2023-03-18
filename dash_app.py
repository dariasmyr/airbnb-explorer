# Run this app with `python dash_app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import plotly.express as px
from dash import Dash, dcc, html
from modules.database_repository import Database

# Initialize the app
app = Dash(__name__)

# Initialize the database connection
database = Database("sqlite+pysqlite:///:/../data/data.sqlite3")
database.connect()

# Define the color scheme
colors = {
    'background': '#ffffff',
    'text': '#444444',
    'accent': '#008080',
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
        'font': {
            'size': 28,
            'family': 'Roboto',
            'color': colors['text']
        },
        'x': 0.5,
        'y': 0.9,
    },
    xaxis_title={
        'text': 'Price',
        'font': {
            'size': 18,
            'family': 'Roboto',
            'color': colors['text']
        },
    },
    yaxis_title={
        'text': 'Neighbourhood group',
        'font': {
            'size': 18,
            'family': 'Roboto',
            'color': colors['text']
        },
    },
    yaxis_range=[mean_price_per_neighbourhood.index[-1], mean_price_per_neighbourhood.index[0]],
    margin=dict(t=100),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
)

# Define the app layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div([
        html.H1(
            children='Welcome to the Airbnb Explorer!',
            style={
                'textAlign': 'left',
                'color': colors['text'],
                'font': {
                    'size': 48,
                    'family': 'Roboto',
                    'weight': 'bold'
                },
                'padding': '40px 0px 20px 20px'
            }
        ),
        html.P(
            children='The Airbnb Explorer project aims to provide users with insights into Airbnb listings in New York City. '
                     'By analyzing data on Airbnb listings, this project helps users find the perfect rental for their needs.',
            style={
                'textAlign': 'left',
                'color': colors['text'],
                'font': {
                    'size': 24,
                    'family': 'Roboto',
                },
                'padding': '0px 0px 20px 20px'
            }
        )
    ]),
    html.Div([
        dcc.Graph(
            id='mean_price_per_neighbourhood_fig',
            figure=mean_price_per_neighbourhood_fig,
            style={
                'padding': '0px 20px 20px 20px'
            }
        )
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)