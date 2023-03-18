# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
import plotly.express as px
from modules.database_repository import Database

app = Dash(__name__)

database = Database("sqlite+pysqlite:///:/../data/data.sqlite3")

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

database.connect()

df = database.get_dataframe()

mean_price = df.groupby('neighbourhood_group')['price'].mean().sort_values(ascending=False)

fig = px.bar(mean_price, x=mean_price.values, y=mean_price.index, orientation='h', color=mean_price.values, color_continuous_scale=px.colors.sequential.Plasma)

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
