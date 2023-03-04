from IPython.core.display_functions import display

from modules.cleaner import DataFormatter
from modules.stats_advanced import Metrics
from modules.stats_basic import DescriptiveStatistics
from modules.stats_basic import DistributionStatistics
from modules.stats_basic import CorrelationStatistics
from modules.stats_basic import TepmoralStatistics
from modules.predictor import Predictor
import ipywidgets as widgets

from modules.database_repository import Database


def connect_to_database():
    print('Connecting to database...')
    db = Database("sqlite+pysqlite:///:/../data/data.sqlite3")
    db.connect()


def clean_data():
    data_formatter = DataFormatter()
    data_formatter.get_dataframe()
    # data_formatter.get_datatypes()
    # data_formatter.check_missing_values()
    # data_formatter.drop_missing_values()
    # data_formatter.get_missing_values_after_drop()
    # new_filename = data_formatter.save_cleared_data('data/cleared_data.csv')
    # return new_filename


def get_stats():
    stats = DescriptiveStatistics()
    stats.set_data_type()
    print('Mean:\n', stats.mean())
    print('Median:\n', stats.median())
    print('Mode:\n', stats.mode())
    print('Range:\n', stats.range())
    print('Standard deviation:\n', stats.stdev())
    print('Variance:\n', stats.variance())


def get_distribution():
    stats = DistributionStatistics()
    stats.create_histogram('availability_365')
    stats.create_density_plot('availability_365')


def get_correlation():
    stats = CorrelationStatistics()
    stats.create_correlation('number_of_reviews', 'price')
    stats.create_heatmap()
    stats.create_scatterplot('number_of_reviews', 'price')
    stats.create_lineplot('number_of_reviews', 'price')


def get_temporal():
    stats = TepmoralStatistics()
    stats.plot_availability_365()
    stats.plot_last_review_vs_num_reviews()
    stats.plot_num_reviews_heatmap()


def get_metrics():
    metrics = Metrics()
    metrics.show_dataframe()
    metrics.mean_price_per_heighbourhood()
    metrics.correlation_with_price()
    metrics.heatmap_correlation()
    metrics.heatmap_density_of_listings()
    metrics.most_common_room_type()
    metrics.avg_number_of_reviews_per_month()
    metrics.percentage_of_available_listings_from()
    metrics.unique_host_count()
    metrics.hosts_with_multiple_listings()


def predict_price():
    predictor = Predictor()

    neighbourhood_group = widgets.Text(
        value='Manhattan',
        placeholder='Type neighbourhood group',
        description='Neighbourhood Group:'
    )

    neighbourhood = widgets.Text(
        value='Upper West Side',
        placeholder='Type neighbourhood',
        description='Neighbourhood:'
    )

    latitude = widgets.FloatText(
        value=40.785091,
        description='Latitude:'
    )

    longitude = widgets.FloatText(
        value=-73.968285,
        description='Longitude:'
    )

    room_type = widgets.Dropdown(
        options=['Private room', 'Entire home/apt', 'Shared room'],
        value='Private room',
        description='Room Type:'
    )

    minimum_nights = widgets.IntSlider(
        value=1,
        min=1,
        max=30,
        step=1,
        description='Minimum Nights:'
    )

    number_of_reviews = widgets.IntSlider(
        value=5,
        min=0,
        max=500,
        step=1,
        description='Number of Reviews:'
    )

    reviews_per_month = widgets.FloatSlider(
        value=1.0,
        min=0,
        max=20.0,
        step=0.1,
        description='Reviews per Month:'
    )

    calculated_host_listings_count = widgets.IntSlider(
        value=1,
        min=0,
        max=100,
        step=1,
        description='Host Listings Count:'
    )

    availability_365 = widgets.IntSlider(
        value=30,
        min=0,
        max=365,
        step=1,
        description='Availability (in days):'
    )

    form_items = [
        neighbourhood_group,
        neighbourhood,
        latitude,
        longitude,
        room_type,
        minimum_nights,
        number_of_reviews,
        reviews_per_month,
        calculated_host_listings_count,
        availability_365
    ]

    form = widgets.VBox(form_items)

    display(form)

    def on_button_click(button):
        price = predictor.predict_single_price(
            neighbourhood_group.value,
            neighbourhood.value,
            latitude.value,
            longitude.value,
            room_type.value,
            minimum_nights.value,
            number_of_reviews.value,
            reviews_per_month.value,
            calculated_host_listings_count.value,
            availability_365.value
        )

        print('Predicted price:', price)

    button = widgets.Button(description='Predict price')
    button.on_click(on_button_click)
    display(button)


# connect_to_database()
# clean_data()
# get_stats('data/cleared_data.csv')
# get_distribution('data/cleared_data.csv')
# get_correlation('data/cleared_data.csv')
# get_temporal('data/cleared_data.csv')
# get_metrics()
predict_price()
