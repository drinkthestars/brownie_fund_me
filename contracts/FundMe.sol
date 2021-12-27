// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    address payable public owner;
    // address public owner;
    mapping(address => uint256) public addrToFunds;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) payable {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = payable(msg.sender);
    }

    // constructor(address _priceFeed) {
    //     priceFeed = AggregatorV3Interface(_priceFeed);
    //     owner = msg.sender;
    // }

    function getEntranceFee() public view returns (uint256) {
        // mimimumUSD
        uint256 mimimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (mimimumUSD * precision) / price;
    }

    function fund() public payable {
        uint256 minUsd = 50 * 10**18;
        require(
            getConversionRate(msg.value) >= minUsd,
            "You need to spend more ETH!"
        );
        addrToFunds[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10**10);
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 10**18;
        return ethAmountInUsd;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        // get the amount of Ether stored in this contract
        uint256 amount = address(this).balance;

        // send all Ether to owner
        // Owner can receive Ether since the address of owner is payable
        (bool success, ) = owner.call{value: amount}("");
        require(success, "Failed to send Ether");

        for (uint256 fIndex = 0; fIndex < funders.length; fIndex++) {
            address funder = funders[fIndex];
            addrToFunds[funder] = 0;
        }
        funders = new address[](0);
    }

    // function withdraw() public payable onlyOwner {
    //     payable(msg.sender).transfer(address(this).balance);
    //     for (uint256 fIndex = 0; fIndex < funders.length; fIndex++) {
    //         address funder = funders[fIndex];
    //         addrToFunds[funder] = 0;
    //     }
    //     funders = new address[](0);
    // }
}
