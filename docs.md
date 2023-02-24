# Airbnb Explorer: Discovering the Best Rentals in NYC
This project is designed to provide insights into Airbnb listings in New York City and help users find the perfect rental for their needs. The project consists of three releases, each with specific goals and tasks.

## Release 1: Data Collection and Cleaning
The goal of this release is to collect data on NYC Airbnb listings, clean the data, and perform basic exploratory data analysis.

### Tasks
- Collect NYC Airbnb data from public sources such as Kaggle or Inside Airbnb
- Clean the data by removing duplicates, handling missing values, and normalizing data
- Perform basic EDA to gain insights into the data, such as the most common neighborhoods, average prices, and room types
- Export cleaned data to a SQL database

### Tech Requirements
- [x] Ability to import data from various sources, such as CSV files, Excel spreadsheets, and SQL databases
- [x] Data cleaning and preprocessing functions, including removing duplicates, handling missing values, and normalizing data
- [x] Ability to perform basic exploratory data analysis (EDA) to gain insights into the data
- Suggested libraries: pandas, NumPy, SQLAlchemy

## Release 2: Data Analysis and Visualization
The goal of this release is to perform advanced data analysis, create visualizations to better understand the data, and use machine learning techniques to predict prices.

### Tasks
- Perform advanced data analysis, such as finding the most popular neighborhoods, identifying the factors that impact prices, and determining the busiest seasons
- Create visualizations to better understand the data, such as heatmaps showing the density of listings in different neighborhoods, scatter plots showing the relationship between price and other factors, and bar charts showing the most common amenities
- Use machine learning techniques to predict prices based on factors such as location, room type, and amenities

### Tech Requirements
- [x] Advanced data analysis capabilities, such as statistical analysis, correlation analysis, and regression analysis
- [x] Ability to create visualizations to better understand the data, including histograms, scatter plots, and heatmaps
- Suggested libraries: matplotlib, seaborn, Plotly, scikit-learn

## Release 3: Database Integration and Web Development
The goal of this release is to integrate the SQL database into a web application using Flask or Django, create a dashboard that displays the results of the data analysis in an interactive and visually appealing way, and implement a search function that allows users to find Airbnb listings that meet specific criteria.

### Tasks
- Integrate the SQL database into a web application using Flask or Django
- Create a dashboard that displays the results of the data analysis in an interactive and visually appealing way, allowing users to filter by neighborhood, room type, and other factors
- Implement a search function that allows users to find Airbnb listings that meet specific criteria, such as price range, number of bedrooms, and proximity to tourist attractions

### Tech Requirements
- [ ] Integration with SQL databases, allowing for data storage and retrieval
- [ ] Ability to create a web application that displays the results of the data analysis in an interactive and visually appealing way
- Suggested libraries: Flask, Django, SQLAlchemy, Dash


# Methods (basic EDA)
Descriptive statistics: You can calculate summary statistics for each variable, such as mean, median, mode, range, standard deviation, and variance. These metrics provide an overview of the data and help identify any outliers or unusual values.
Distribution analysis: You can create histograms or density plots to visualize the distribution of each variable. This can help identify any skewness, multimodality, or outliers in the data.
Correlation analysis: You can calculate correlation coefficients between pairs of variables to examine the strength and direction of their relationship. This can help identify any patterns or associations in the data.
Visualization: You can create scatterplots, heatmaps, or other visualizations to explore the relationship between variables. This can help identify any trends, patterns, or clusters in the data.
Time series analysis: You can analyze the temporal patterns in the data by examining variables such as last_review and availability_365 over time. This can help identify any seasonal patterns or trends.

# Metrics (advanced EDA)
The average price of Airbnb listings in each neighbourhood group or neighbourhood.
The most common room types in each neighbourhood group or neighbourhood.
The average number of reviews per month for listings in each neighbourhood group or neighbourhood.
The percentage of listings that are available for booking for different minimum_nights.
The number of unique hosts in each neighbourhood group or neighbourhood.
The top 10 hosts with the most listings.
The correlation between price and other variables, such as minimum_nights or calculated_host_listings_count.