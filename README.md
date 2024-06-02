# Giza-Weather-Game
GWG, inspired by Giza and WeatherXM, uses historical weather data and time series machine learning to predict future weather. The model will be deployed on the zkml platform Giza. With Giza AI Agent, offering daily weather predictions and betting options.
`https://gwg-frontend.vercel.app/`


1. fetch weather data from WeatherXM Data Index `https://index.weatherxm.network/`, organize and clean data and get `WeatherXMData.csv`

2. Create and Train an XGBoost Model, Save the model throught `train_xgboost.py`  // python train_xgboost.py

3. Transpile model to Orion Cairo
```
giza transpile xgb_weather.json --output-path xgb_weather
[giza][2024-06-01 03:47:17.251] No model id provided, checking if model exists ✅ 
[giza][2024-06-01 03:47:17.253] Model name is: xgb_weather
[giza][2024-06-01 03:47:18.773] Model already exists, using existing model ✅ 
[giza][2024-06-01 03:47:18.775] Model found with id -> 675! ✅
[giza][2024-06-01 03:47:20.103] Version Created with id -> 4! ✅
[giza][2024-06-01 03:47:20.105] Sending model for transpilation ✅ 
[giza][2024-06-01 03:47:36.077] Transpilation is fully compatible. Version compiled and Sierra is saved at Giza ✅
[giza][2024-06-01 03:47:38.093] Downloading model ✅
[giza][2024-06-01 03:47:38.099] model saved at: xgb_weather
```

4. Deploy an inference endpoint
```
giza endpoints list
giza endpoints get --endpoint-id 1

giza endpoints deploy --model-id 675 --version-id 4
▰▰▰▰▰▰▱ Creating endpoint!
[giza][2024-06-01 04:36:19.718] Endpoint is successful ✅
[giza][2024-06-01 04:36:19.720] Endpoint created with id -> 244 ✅
[giza][2024-06-01 04:36:19.721] Endpoint created with endpoint URL: https://endpoint-yycztest-675-4-ba8264e2-7i3yxzspbq-ew.a.run.app 🎉
```

5. Run a verifiable inference
```
python verifiable_inference.py   
🚀 Starting deserialization process...
✅ Deserialization completed! 🎉
Predicted value for input [13.4 97.0 0.26 1001.4 True] is 0.03626
Proof ID: f090058e0df44647ad39de0e74e28341
```

6. Download the proof
```
giza endpoints get-proof --endpoint-id 244 --proof-id "f090058e0df44647ad39de0e74e28341"
[giza][2024-06-01 04:43:40.527] Getting proof from endpoint 244 ✅ 
{
  "id": 985,
  "job_id": 1139,
  "metrics": {
    "proving_time": 20.960533
  },
  "created_date": "2024-05-31T20:41:37.424524"
}

giza endpoints download-proof --endpoint-id 244 --proof-id "f090058e0df44647ad39de0e74e28341" --output-path zk_xgboost_weather.proof
path zk_xgboost_weather.proof
[giza][2024-06-01 04:44:40.110] Getting proof from endpoint 244 ✅ 
[giza][2024-06-01 04:44:45.849] Proof downloaded to zk_xgboost_weather.proof ✅ 
```

7. Verify the proof
```
giza verify --proof-id 985
[giza][2024-06-01 04:45:24.257] Verifying proof...
[giza][2024-06-01 04:45:26.364] Verification result: True
[giza][2024-06-01 04:45:26.365] Verification time: 0.445587406
```


8. Creating an AI Agent
```
giza agents create --model-id 675 --version-id 4 --name GWG --description GizaWeatherGame
{
  "id": 24,
  "name": "GWG",
  "description": "GizaWeatherGame",
  "parameters": {
    "model_id": 675,
    "version_id": 4,
    "endpoint_id": 244,
    "account": "yycztest"
  },
  "created_date": "2024-05-31T21:12:25.271732",
  "last_update": "2024-05-31T21:12:25.271732"
}
```