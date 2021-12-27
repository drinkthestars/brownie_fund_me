from brownie import FundMe
from scripts.common import get_account

def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entr_fee = fund_me.getEntranceFee()
    print(f"The current entry fee is {entr_fee}")
    print("Funding")
    fund_me.fund({"from": account, "value": entr_fee})

def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    withdrawn = fund_me.withdraw({"from": account})
    print(f"Funds withdrawn {withdrawn.value}")

def main():
    fund()
    withdraw()
