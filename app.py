from modules.cleaner import DataFormatter
from modules.metrics import Metrics
from modules.predictor import Predictor


def clean_data():
    data_formatter = DataFormatter()
    data_formatter.get_datatypes()
    data_formatter.drop_missing_values()
    _cleaned_data = data_formatter.save_cleared_data('data/cleared_data.csv')
    return _cleaned_data


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
    predictor.create_form()


get_metrics()
# predict_price()
