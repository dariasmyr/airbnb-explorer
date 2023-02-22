import pandas as pd

# create a DataFrame with missing values
data = pd.read_csv('data/AB_NYC_2019.csv')

df = pd.DataFrame(data)

print("DataFrame:")
print(df)

# apply the dtype attribute
result = df.dtypes

print("Output:")
print(result)

# find the missing values in key columns like price, minimum_nights, and reviews_per_month
print("Missing values in id:")
print(df['id'].isnull().sum())

print("Missing values in name:")
print(df['name'].isnull().sum())

print("Missing values in host_id:")
print(df['host_id'].isnull().sum())

print("Missing values in host_name:")
print(df['host_name'].isnull().sum())

print("Missing values in neighbourhood_group:")
print(df['neighbourhood_group'].isnull().sum())

print("Missing values in neighbourhood:")
print(df['neighbourhood'].isnull().sum())

print("Missing values in latitude:")
print(df['latitude'].isnull().sum())

print("Missing values in longitude:")
print(df['longitude'].isnull().sum())

print("Missing values in room_type:")
print(df['room_type'].isnull().sum())

print("Missing values in price:")
print(df['price'].isnull().sum())

print("Missing values in minimum_nights:")
print(df['minimum_nights'].isnull().sum())

print("Missing values in number_of_reviews:")
print(df['number_of_reviews'].isnull().sum())

print("Missing values in last_review:")
print(df['last_review'].isnull().sum())

print("Missing values in reviews_per_month:")
print(df['reviews_per_month'].isnull().sum())

print("Missing values in calculated_host_listings_count:")
print(df['calculated_host_listings_count'].isnull().sum())

print("Missing values in availability_365:")
print(df['availability_365'].isnull().sum())



