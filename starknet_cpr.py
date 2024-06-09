import asyncio
from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.contract import Contract
from giza.agents import AgentResult, GizaAgent
import numpy as np
import passphrase
import time
import os

# setup params
os.environ['YYCZTEST_PASSPHRASE'] = passphrase.passphrase
address = passphrase.sn_address
private_key = passphrase.sn_private_key
class_hash = passphrase.sn_class_hash
node_url = passphrase.sn_node_url
contract_address = "0x06a42c26f5c2eca4be1e7272dd3bec4fc24403c3d195b71e398df601b61bb52b"
agent_id = 24

client = FullNodeClient(node_url=node_url)

# get feed data
def get_current_data_from_WeatherXM():

    data = [12.5,95.0,0.19,1008.35,False]

    return np.array(data, dtype=object)


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


asyncio.run(main())