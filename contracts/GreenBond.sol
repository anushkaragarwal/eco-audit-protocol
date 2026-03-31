// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GreenBond {

    address public company;
    uint public interestRate;
    uint public esgScore;

    constructor(uint _initialScore) {
        company = msg.sender;
        esgScore = _initialScore;
        interestRate = calculateInterest(_initialScore);
    }

    function updateESG(uint newScore) public {
        esgScore = newScore;
        interestRate = calculateInterest(newScore);
    }

    function calculateInterest(uint score) internal pure returns (uint) {
        if (score > 80) return 5;
        else if (score > 50) return 10;
        else return 20;
    }
}