from dash import Dash, html, dcc
from modules.metrics import Metrics
from modules.predictor import Predictor

metrics = Metrics()
predictor = Predictor()

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Airbnb Metrics'),
    html.Img(src="./New_York_City_.png", width="400", alt="New_York_City"),

    html.H2('Overview'),
    html.P('The Airbnb Explorer project aims to provide users with insights into Airbnb listings in New York City. By '
           'analyzing data on Airbnb listings, this project helps users find the perfect rental for their needs.'),

    html.H2('Price'),
    html.H3('Average price of Airbnb listings in each neighbourhood group'),
    dcc.Graph(id='mean-price-per-neighbourhood', figure=metrics.mean_price_per_neighbourhood()),

    html.H2('Price Correlation'),
    html.P('The following graph shows the correlation between the price of a several features of a rental.'),
    html.H3('Correlation between price and other columns'),
    dcc.Graph(id='correlation-with-price', figure=metrics.correlation_with_price()),

    html.H3('Correlation between columns'),
    dcc.Graph(id='heatmap-correlation', figure=metrics.heatmap_correlation()),

    html.H2('Conveniences'),
    html.P('The following graph shows the number of rentals of each type in each neighborhood.'),
    html.H3('Density of listings by neighbourhood group and room type'),
    dcc.Graph(id='heatmap-density-of-listings', figure=metrics.heatmap_density_of_listings()),

    html.H3('Most common room type in each neighbourhood group'),
    dcc.Graph(id='most-common-room-type', figure=metrics.most_common_room_type()),

    html.H2('Reviews'),
    html.P(
        'The following graph shows the average number of reviews for listings per month in each neighbourhood group.'),
    html.H3('Average number of reviews for listings per month in each neighbourhood group'),
    html.Div(id='avg-number-of-reviews-per-month', children=metrics.avg_number_of_reviews_per_month()),

    html.H2('Availability'),
    html.P('The following graph shows the percentage of available listings from the last 365 days.'),
    html.H3('Percentage of available listings from the last 365 days'),
    html.Div(id='percentage-of-available-listings-from', children=metrics.percentage_of_available_listings_from()),

    predictor.create_form()
])

if __name__ == '__main__':
    app.run_server(debug=True)
