import xgboost as xgb
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
import pandas as pd

from giza.agents.model import GizaModel


MODEL_ID = 675  # Update with your model ID
VERSION_ID = 4  # Update with your version ID

def prediction(input, model_id, version_id):
    model = GizaModel(id=model_id, version=version_id)

    (result, proof_id) = model.predict(
        input_feed={"input": input}, verifiable=True, model_category="XGB"
    )

    return result, proof_id


def execution():
    # The input data type should match the model's expected input
    input = X_test[1, :]

    print(input)
    print(X_test)

    (result, proof_id) = prediction(input, MODEL_ID, VERSION_ID)

    print(f"Predicted value for input {input} is {result}")

    return result, proof_id


if __name__ == "__main__":
    df = pd.read_csv('WeatherXMData.csv')

    features = ['temperature', 'humidity', 'wind_speed', 'pressure', 'has_precipitation']
    target = 'next_day_precipitation'

    X = df[features].values
    y = df[target].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    _, proof_id = execution()
    print(f"Proof ID: {proof_id}")