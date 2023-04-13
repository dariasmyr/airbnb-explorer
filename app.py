from modules.cleaner import DataFormatter
from modules.metrics import Metrics
from modules.predictor import Predictor
from modules.database_repository import Database


def clean_data():
    data_formatter = DataFormatter()
    data_formatter.get_datatypes()
    data_formatter.drop_missing_values()
    _cleaned_data = data_formatter.save_cleared_data('data/cleared_data.csv')


def create_database():
    db_url = 'sqlite+pysqlite:///data/database.sqlite3'
    database_repository = Database(db_url)
    database_repository.create_database()
    database_repository.save_data_to_db('data/cleared_data.csv')


def get_metrics():
    metrics = Metrics()
    metrics.mean_price_per_neighbourhood()
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
    predictor.predict_single_price('Manhattan', 'Harlem', 40.82085, -73.94025, 'Private room', 3, 0, 0, 1, 0)


# clean_data()
# create_database()
# get_metrics()
predict_price()
