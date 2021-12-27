from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BC_ENVS = ["development", "ganache-local"]
DECIMALS = 8
STARTING_PRICE = 200000000000

def get_account():
    if (network.show_active() in LOCAL_BC_ENVS or network.show_active() in FORKED_LOCAL_ENVS):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    if len(MockV3Aggregator) <= 0:
        print("No mocks previously deployed. Deploying...")
        MockV3Aggregator.deploy(
            DECIMALS, 
            Web3.toWei(STARTING_PRICE, "ether"), 
            {"from": get_account()}
        )
        print("Mocks deployed!")
    else:
        print(f"Mock already exists at {MockV3Aggregator[-1].address}!")
