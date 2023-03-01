from modules.cleaner import DataFormatter
from modules.stats_advanced import Metrics
from modules.stats_basic import DescriptiveStatistics
from modules.stats_basic import DistributionStatistics
from modules.stats_basic import CorrelationStatistics
from modules.stats_basic import TepmoralStatistics

from modules.database_repository import Database


def connect_to_database():
    print('Connecting to database...')
    db = Database("sqlite+pysqlite:///:/../data/data.sqlite3")
    db.connect()


print('Cleaning data...')


def clean_data():
    data_formatter = DataFormatter()
    data_formatter.get_dataframe()
    # data_formatter.get_datatypes()
    # data_formatter.check_missing_values()
    # data_formatter.drop_missing_values()
    # data_formatter.get_missing_values_after_drop()
    # new_filename = data_formatter.save_cleared_data('data/cleared_data.csv')
    # return new_filename


print('Getting descriptive statistics...')


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
    metrics.most_common_room_type()
    metrics.avg_number_of_reviews_per_month()
    metrics.percentage_of_available_listings_from()
    metrics.unique_host_count()
    metrics.hosts_with_multiple_listings()


connect_to_database()
clean_data()
# get_stats('data/cleared_data.csv')
# get_distribution('data/cleared_data.csv')
# get_correlation('data/cleared_data.csv')
# get_temporal('data/cleared_data.csv')
get_metrics()
