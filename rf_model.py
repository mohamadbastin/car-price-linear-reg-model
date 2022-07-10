import pycaret.regression as pycreg
import pandas as pd
import sklearn.metrics
from pycaret.utils import check_metric



test = pd.read_csv('cars-test2.csv').drop('_id', axis=1).drop('url', axis=1)

model = pycreg.load_model("rf")

prediction = pycreg.predict_model(model, test)

print("mse: ", sklearn.metrics.mean_squared_error(test['price'], prediction['Label']))
print("r2: ", sklearn.metrics.r2_score(test['price'], prediction['Label']))
print(check_metric(test['price'], prediction['Label'], 'R2'))