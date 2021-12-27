from brownie import accounts, FundMe, network, exceptions
from scripts.common import get_account, LOCAL_BC_ENVS
from scripts.deploy import deploy_fund_me
import pytest

def test_deploy_fund():
    # Arrange
    expected = 0
    account = get_account()
    account_addr = account.address
    # Act
    fund_me = deploy_fund_me()
    entr_fee = fund_me.getEntranceFee() + 100
    txn = fund_me.fund({"from": account, "value": entr_fee})
    txn.wait(1)
    # Assert
    assert fund_me.addrToFunds(account_addr) == entr_fee

def test_deploy_fund_withdraw():
    # Arrange
    expected = 0
    account = get_account()
    account_addr = account.address
    # Act
    fund_me = deploy_fund_me()
    entr_fee = fund_me.getEntranceFee() + 100
    txn_fund = fund_me.fund({"from": account, "value": entr_fee})
    txn_fund.wait(1)
    txn_withdraw = fund_me.withdraw({"from": account})
    txn_withdraw.wait(1)
    # Assert
    assert fund_me.addrToFunds(account_addr) == 0

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BC_ENVS:
        pytest.skip("test_only_owner_can_withdraw() is only for local testing")
    account = get_account()
    fund_me = deploy_fund_me()
    entr_fee = fund_me.getEntranceFee() + 100
    txn_fund = fund_me.fund({"from": account, "value": entr_fee})
    txn_fund.wait(1)
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
    assert fund_me.funders(0) == account.address

def test_funders_cleared_after_withdraw():
    if network.show_active() not in LOCAL_BC_ENVS:
        pytest.skip("test_funders_cleared_after_withdraw() is only for local testing")
    account = get_account()
    fund_me = deploy_fund_me()
    entr_fee = fund_me.getEntranceFee() + 100
    fund_me.fund({"from": account, "value": entr_fee})
    assert fund_me.funders(0) == account.address
    fund_me.withdraw({"from": account})        
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.funders(0)
