import pprint
import numpy as np
from PIL import Image
import requests
from giza.agents import GizaAgent, AgentResult
import time
from ape import accounts
from passphrase import passphrase
import os


os.environ['YYCZTEST_PASSPHRASE'] = passphrase
# Make sure to fill these in
MODEL_ID = 675
VERSION_ID = 4
# As we are executing in sepolia, we need to specify the chain
CHAIN = "ethereum:sepolia:geth"
# The address of the deployed contract
GWG_CONTRACT = "0x7EF2CFc86513ec79b8C8DE742a0991be2798A8e9"  ###

URL = "https://api.weatherxm.com/api/v1/cells/8729a1d82ffffff/devices"


def get_current_data_from_WeatherXM():

    # data = [12.5,95.0,0.19,1008.35,False]
    response = requests.get(URL)
    current_data = []
    if response.status_code == 200:
        data = response.json()

        results = []
        for device in data:
            weather_data = device['current_weather']
            result = {
                'temperature': weather_data['temperature'],
                'humidity': weather_data['humidity'],
                'wind_speed': weather_data['wind_speed'],
                'pressure': weather_data['pressure'],
                'precipitation': bool(weather_data['precipitation'])
            }
            results.append(result)

    print(results[0])
    for value in results[0].values():
        current_data.append(value)

    return np.array(current_data, dtype=object)


def create_agent(model_id: int, version_id: int, chain: str, contract: str):
    """
    Create a Giza agent for the GWG model
    """
    agent = GizaAgent(
        contracts={"gwg": contract},
        id=model_id,
        version_id=version_id,
        chain=chain,
        account="yycztest"
    )
    return agent

def predict(agent: GizaAgent, input):
    prediction = agent.predict(
        input_feed={"input": input}, verifiable=True, model_category="XGB"
    )
    print('prediction', int(prediction.value * 1000))
    return prediction

def get_probability(prediction: AgentResult):
    return int(prediction.value * 1000)

def execute_contract(agent: GizaAgent, pob: int):
    with agent.execute() as contracts:
        contract_result = contracts.gwg.createRound(int(time.time()), pob)
    return contract_result


# main ai agent flow
def create_prediction_round():

    current_weather_data = get_current_data_from_WeatherXM()

    agent = create_agent(MODEL_ID, VERSION_ID, CHAIN, GWG_CONTRACT)

    prediction = predict(agent, current_weather_data)

    probability = get_probability(prediction)

    execute_contract(agent, probability)

    print('probability', probability)



# schedule task
while True:
    create_prediction_round()
    time.sleep(60 * 60 * 24)

