import sklearn
import pandas
import numpy as np
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression

data = pandas.read_csv('cars.csv')

data_dropped = data.dropna()
X_temp = data_dropped.drop('price', axis=1).drop('_id', axis=1).drop('url', axis=1)
y = data_dropped['price']
print(y.describe())
X = pandas.get_dummies(X_temp)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

regressor = LinearRegression()
regressor.fit(X_train, y_train)

y_predicted = regressor.predict(X_test)

mse = sklearn.metrics.mean_squared_error(y_test, y_predicted)
r2 = sklearn.metrics.r2_score(y_test, y_predicted)

print("mse:", mse)
# print("r2:", r2)

s = regressor.score(X_test, y_test)
print("score:", s)

data_test = pandas.read_csv('cars-test.csv')

data_test_dropped = data_test.dropna()
X_temp = data_test_dropped.drop('price', axis=1).drop('_id', axis=1).drop('url', axis=1)
y_test2 = data_test_dropped['price']

# X_test2 = pandas.get_dummies(X_temp)

X_test2 = X_temp.reindex(labels=X_train.columns, axis=1, fill_value=0)

# missing_cols = set(X_train.columns) - set(X_test2.columns)
# for c in missing_cols:
#     X_test2[c] = 0
# X_test2 = X_test2[X_test2.columns]

# train2, test2 = X_train.align(X_test2, join='outer', axis=1, fill_value=0)
# print(X_train.shape)
# print(X_test2.shape)
y_test_pred = regressor.predict(X_test)
#
# print(X_test2)
# print(y_test_pred)
# print(X_test2)
amir_mamad_error = 0
l = len(y_test.values)
for i in range(len(y_test_pred)):
    # print(i, y_test[i], y_test_pred[i], "------", y_test2[i] / y_test_pred[i])
    amir_mamad_error += y_test_pred[i] / y_test.values[i]
#
print("ams:", amir_mamad_error / l)

# y_test.columns = [id', 'price']
# print(y_test)
