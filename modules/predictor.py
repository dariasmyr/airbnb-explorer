import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from modules.database_repository import Database


class Predictor:

    def __init__(self):
        self.db = Database("sqlite+pysqlite:///:/../data/data.sqlite3")
        self.db.connect()
        self.data = self.db.get_dataframe()

        # Load and preprocess data
        self.data = self.data.drop(['id', 'name', 'host_id', 'host_name', 'last_review'], axis=1)
        self.data = pd.get_dummies(self.data, columns=['neighbourhood_group', 'neighbourhood', 'room_type'])
        self.data.columns = self.data.columns.astype(str)

        # Split the data into features and target
        self.X = self.data.drop(['price'], axis=1)
        self.y = self.data['price']

        # Train Random Forest Regression model
        self.rf_model = RandomForestRegressor()
        self.rf_model.fit(self.X, self.y)

    def predict_price(self):
        # Load data and drop unnecessary columns
        data = self.data
        data = data.drop(['id', 'name', 'host_id', 'host_name', 'last_review'], axis=1)

        # One-hot encode categorical variables
        data = pd.get_dummies(data, columns=['neighbourhood_group', 'neighbourhood', 'room_type'])

        # Convert column names to strings
        data.columns = data.columns.astype(str)

        # Split the data into features and target
        X = data.drop(['price'], axis=1)
        y = data['price']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Convert feature names to strings
        X_train.columns = X_train.columns.astype(str)

        # Train and evaluate Linear Regression model
        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        lr_score = lr_model.score(X_test, y_test)

        # Train and evaluate Decision Tree Regression model
        dt_model = DecisionTreeRegressor()
        dt_model.fit(X_train, y_train)
        dt_score = dt_model.score(X_test, y_test)

        # Train and evaluate Random Forest Regression model
        rf_model = RandomForestRegressor()
        rf_model.fit(X_train, y_train)
        rf_score = rf_model.score(X_test, y_test)

        # Compare the models and choose the best one
        scores = {'Linear Regression': lr_score, 'Decision Tree Regression': dt_score,
                  'Random Forest Regression': rf_score}
        best_model = max(scores, key=scores.get)

        # Predict the prices using the best model
        if best_model == 'Linear Regression':
            y_pred = lr_model.predict(X_test)
        elif best_model == 'Decision Tree Regression':
            y_pred = dt_model.predict(X_test)
        elif best_model == 'Random Forest Regression':
            y_pred = rf_model.predict(X_test)

        # Print the mean squared error and the coefficient of determination
        print('Mean squared error: %.2f'
              % mean_squared_error(y_test, y_pred))
        print('Coefficient of determination: %.2f'
              % r2_score(y_test, y_pred))

        print('Best model: ', best_model)

        # Return the predicted prices and the best model
        return y_pred

    def predict_single_price(self, neighbourhood_group, neighbourhood, latitude, longitude, room_type, minimum_nights,
                             number_of_reviews, reviews_per_month, calculated_host_listings_count, availability_365):
        # Create a dictionary of input features
        input_data = {'neighbourhood_group': neighbourhood_group,
                      'neighbourhood': neighbourhood,
                      'latitude': latitude,
                      'longitude': longitude,
                      'room_type': room_type,
                      'minimum_nights': minimum_nights,
                      'number_of_reviews': number_of_reviews,
                      'reviews_per_month': reviews_per_month,
                      'calculated_host_listings_count': calculated_host_listings_count,
                      'availability_365': availability_365}

        # Convert input data to DataFrame
        input_df = pd.DataFrame([input_data])

        # One-hot encode categorical variables
        input_df = pd.get_dummies(input_df, columns=['neighbourhood_group', 'neighbourhood', 'room_type'])

        # Reorder columns to match training data
        input_df = input_df.reindex(columns=self.X.columns, fill_value=0)

        # Predict the price using Random Forest Regression model
        y_pred = self.rf_model.predict(input_df)

        # Return the predicted price
        return y_pred[0]
