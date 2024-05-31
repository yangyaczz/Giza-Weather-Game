## Create and Train an XGBoost Model
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

df = pd.read_csv('WeatherXMData.csv')

features = ['temperature', 'humidity', 'wind_speed', 'pressure', 'has_precipitation']
target = 'next_day_precipitation'

X = df[features].values
y = df[target].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

n_estimators = 10
max_depth = 6

model = xgb.XGBRegressor(n_estimators=n_estimators, max_depth=max_depth)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')


## Save the model
from giza.zkcook import serialize_model
serialize_model(model, "xgb_weather.json")
