import pickle
import sklearn
import pandas
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def save_model_info_to_disk():
    input_columns = [{'name': col, 'type': X_temp[col].dtype, 'unique_vals': X_temp[col].unique() if X_temp[col].dtype == object else None} for col in X_temp.columns]
    pickle.dump(input_columns, open('input_columns.sav', 'wb'))
    pickle.dump(X.columns, open('model_meta.sav', 'wb'))
    pickle.dump(regressor, open('model.sav', 'wb'))

data = pandas.read_csv('cars.csv')

data_dropped = data.dropna()
X_temp = data_dropped.drop('price', axis=1).drop('_id', axis=1).drop('url', axis=1)
y = data_dropped['price']
X = pandas.get_dummies(X_temp)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

regressor = LinearRegression()
regressor.fit(X_train, y_train)

save_model_info_to_disk()

y_predicted = regressor.predict(X_test)

mse = sklearn.metrics.mean_squared_error(y_test, y_predicted)
r2 = sklearn.metrics.r2_score(y_test, y_predicted)
s = regressor.score(X_test, y_test)

print("mse:", mse)
print("score:", s)

data_test = pandas.read_csv('cars-test.csv')

data_test_dropped = data_test.dropna()
X_temp = data_test_dropped.drop('price', axis=1).drop('_id', axis=1).drop('url', axis=1)
y_test2 = data_test_dropped['price']

X_test2 = X_temp.reindex(labels=X_train.columns, axis=1, fill_value=0)

y_test_pred = regressor.predict(X_test)

amir_mamad_error = 0
l = len(y_test.values)
for i in range(len(y_test_pred)):
    amir_mamad_error += y_test_pred[i] / y_test.values[i]

print("ams:", amir_mamad_error / l)