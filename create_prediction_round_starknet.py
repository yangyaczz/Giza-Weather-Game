import asyncio
from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.contract import Contract
from giza.agents import AgentResult, GizaAgent
import numpy as np
import requests
import passphrase
import time
import os

# setup params
os.environ['YYCZTEST_PASSPHRASE'] = passphrase.passphrase
address = passphrase.sn_address
private_key = passphrase.sn_private_key
class_hash = passphrase.sn_class_hash
node_url = passphrase.sn_node_url
contract_address = "0x02080d031fe3e46b4b4d3b7236e62021ec9d4adea303ce741141a79874e0ac03"
agent_id = 24

client = FullNodeClient(node_url=node_url)

URL = "https://api.weatherxm.com/api/v1/cells/8729a1d82ffffff/devices"

# get feed data
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

# main ai agent flow
async def main():
    account = Account(
        address=address,
        client=client,
        key_pair=KeyPair.from_private_key(private_key),
        chain=StarknetChainId.SEPOLIA,
    )
    
    contract = await Contract.from_address(provider=account, address=contract_address)
    agent = GizaAgent.from_id(
        id=agent_id
    )

    prediction = agent.predict(input_feed={"input": get_current_data_from_WeatherXM()}, verifiable=True, model_category="XGB")

    p = int(prediction.value * 1000)
    ts = int(time.time())

    print('prediction', p, "timestamp", ts)

    (current_round_id,) = await contract.functions["get_current_round_id"].call()
    print("before create round current round id", current_round_id)

    try:
        invocation = await contract.functions["create_round"].invoke_v1(
            start_timestamp= ts, probability=p, max_fee=int(1e16)
        )
        await invocation.wait_for_acceptance()
    except:
        print('---')

    (current_round_id,) = await contract.functions["get_current_round_id"].call()
    print("after create round current round id", current_round_id)



# schedule task
while True:
    asyncio.run(main())
    time.sleep(60 * 60 * 24)

