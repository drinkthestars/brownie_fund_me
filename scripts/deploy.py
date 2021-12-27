from brownie import config, FundMe, MockV3Aggregator, network
from scripts.common import get_account, deploy_mocks, LOCAL_BC_ENVS

def deploy_fund_me():
    account = get_account()
    active_network = network.show_active()
    fund_me = FundMe.deploy(
        get_price_feed_addr(account, active_network),
        {"from": account}, 
        publish_source=get_publish_source(active_network)
    )
    print(f"Contract deployed to {fund_me.address}!")
    return fund_me

def get_price_feed_addr(account, active_network):
    # if on persistent network like rinkeby use assoc. addr
    # else, deploy mocks
    if  active_network not in LOCAL_BC_ENVS:
        return config["networks"][active_network]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        return MockV3Aggregator[-1].address

def get_publish_source(active_network):
    return config["networks"][active_network].get("verify")

def main():
    deploy_fund_me()