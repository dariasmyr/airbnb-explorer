from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

import pandas as pd

# создаем простой датасет
data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'y': [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
})

# разделяем данные на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(data[['x']], data['y'], test_size=0.2, random_state=53)

# обучаем модель линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# делаем предсказания на тестовом наборе
predicted_y = model.predict(X_test)

# вычисляем метрики качества модели
mse = mean_squared_error(y_test, predicted_y)
r2 = r2_score(y_test, predicted_y)

# выводим результаты
print('Mean squared error:', mse)
print('R^2 score:', r2)

# predict values for 2, 3, 4
print(model.predict([[2], [3], [4]]))
