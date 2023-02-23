from modules.cleaner import DataFormatter
from modules.stats import DescriptiveStatistics
from modules.stats import DistributionStatistics
from modules.stats import CorrelationStatistics
from modules.stats import TepmoralStatistics

print('Cleaning data...')


def clean_data():
    filename = 'data/raw_data.csv'
    data_formatter = DataFormatter(filename)
    data_formatter.get_dataframe()
    data_formatter.get_datatypes()
    data_formatter.check_missing_values()
    data_formatter.drop_missing_values()
    data_formatter.get_missing_values_after_drop()
    new_filename = data_formatter.save_cleared_data('data/cleared_data.csv')
    return new_filename


clean_data()

print('Getting descriptive statistics...')


def get_stats(new_filename):
    stats = DescriptiveStatistics(new_filename)
    stats.set_data_type()
    print('Mean:\n', stats.mean())
    print('Median:\n', stats.median())
    print('Mode:\n', stats.mode())
    print('Range:\n', stats.range())
    print('Standard deviation:\n', stats.stdev())
    print('Variance:\n', stats.variance())


def get_distribution(new_filename):
    stats = DistributionStatistics(new_filename)
    stats.create_histogram('availability_365')
    stats.create_density_plot('availability_365')


def get_correlation(new_filename):
    stats = CorrelationStatistics(new_filename)
    stats.create_correlation('calculated_host_listings_count', 'price')
    stats.create_heatmap()
    stats.create_scatterplot('number_of_reviews', 'price')
    stats.create_lineplot('number_of_reviews', 'price')

def get_temporal(new_filename):
    stats = TepmoralStatistics(new_filename)
    stats.plot_availability_365()
    stats.plot_last_review_vs_num_reviews()
    stats.plot_num_reviews_heatmap()


get_stats('data/cleared_data.csv')
get_distribution('data/cleared_data.csv')
get_correlation('data/cleared_data.csv')
get_temporal('data/cleared_data.csv')
