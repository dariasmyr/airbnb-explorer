import random

import pandas as pd
import matplotlib.pyplot as plt

# чтение данных из CSV-файла
data = pd.read_csv('data/test.csv')

# Add random 1000 rows: name, age, income (income - random value from 100 to 1000)
for i in range(1000):
    income = random.randint(100, 100000)
    data.loc[len(data)] = ['name' + str(i), i, income]


# фильтрация данных
filtered_data = data[data['age'] > 25]

# сортировка данных
sorted_data = filtered_data.sort_values(by='income', ascending=False)

# визуализация данных
plt.scatter(sorted_data['income'], sorted_data['age'])
plt.title('Income vs Age')
plt.xlabel('Income')
plt.ylabel('Age')
plt.show()
