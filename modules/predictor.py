from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from modules.database_repository import Database
import pandas as pd


class Predictor:

    def __init__(self):
        try:
            self.db = Database("sqlite+pysqlite:///:/../data/data.sqlite3")
            self.db.connect()
            self.data = self.db.get_dataframe()
        except Exception as e:
            print(e)

    def handle_data(self):
        # Drop unnecessary columns
        self.data = self.data.drop(['id', 'name', 'host_id', 'host_name', 'last_review'], axis=1)
        # Encode categorical variables
        self.data = pd.get_dummies(self.data, columns=['neighbourhood_group', 'neighbourhood', 'room_type'])

    def train_model(self):
        # Split the dataset into features and target 'X' will contain all the features (independent variables) that
        # will be used to predict the target variable The 'drop' function removes the 'price' column from the
        # dataset, since it is the target variable that we want to predict
        X = self.data.drop(['price'], axis=1)
        X.columns = X.columns.astype(str)

        # 'y' will contain the target variable (dependent variable) that we want to predict using the features in 'X'
        y = self.data['price']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create a Linear Regression model
        model = LinearRegression()
        # Train the model using the training sets
        model.fit(X_train, y_train)

        # Evaluate the model using the testing data
        score = model.score(X_test, y_test)
        print("R-squared:", score)

        # Make predictions using the testing set
        y_pred = model.predict(X_test)
        # The coefficients
        print('Coefficients: \n', model.coef_)
        # The mean squared error
        print('Mean squared error: %.2f'
              % mean_squared_error(y_test, y_pred))
        # The coefficient of determination: 1 is perfect prediction
        print('Coefficient of determination: %.2f'
              % r2_score(y_test, y_pred))
