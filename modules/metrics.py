import numpy as np
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import seaborn as sns


class Metrics:

    # The average price of Airbnb listings in each neighbourhood group or neighbourhood.

    def __init__(self, filename):
        try:
            self.df = pd.read_csv(filename)
        except FileNotFoundError:
            raise FileNotFoundError("CSV file not found!")
        except ValueError:
            raise ValueError("Invalid CSV file!")

    def mean_price(self):
        print('Average price of Airbnb listings in each neighbourhood group: ')
        return self.df.groupby('neighbourhood_group')['price'].mean().apply(lambda x: '%.2f$' % x)
