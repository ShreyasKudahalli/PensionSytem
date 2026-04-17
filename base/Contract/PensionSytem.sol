// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract PensionSystem {

    address public owner;

    enum PensionType { NONE, OLD_AGE, WIDOW, DISABILITY }

    struct User {
        uint age;
        PensionType pensionType;
        bool isEligible;
        bool hasClaimed;
        bool isMarried;
        bool isDisabled;
    }

    mapping(address => User) public users;

    uint public totalFund;      // Govt deposited
    uint public totalClaimed;   // Total withdrawn
    uint public activeUsers;    // Eligible + not claimed

    event UserRegistered(address user, uint age, PensionType pType);
    event PensionClaimed(address user, uint amount);
    event FundsDeposited(uint amount);

    constructor() {
        owner = msg.sender;
    }

    // ✅ Register User
    function registerUser(
        address userAddr,
        uint age,
        PensionType pType,
        bool isMarried,
        bool isDisabled
    ) public {
        require(msg.sender == owner, "Only backend");

        bool eligible = false;

        if (pType == PensionType.OLD_AGE && age > 60) {
            eligible = true;
        }
        else if (pType == PensionType.WIDOW && isMarried == false) {
            eligible = true;
        }
        else if (pType == PensionType.DISABILITY && isDisabled == true) {
            eligible = true;
        }

        // If user was already active before, remove count first
        if (users[userAddr].isEligible && !users[userAddr].hasClaimed) {
            activeUsers--;
        }

        users[userAddr] = User(
            age,
            pType,
            eligible,
            false,
            isMarried,
            isDisabled
        );

        // Count only ACTIVE users
        if (eligible) {
            activeUsers++;
        }

        emit UserRegistered(userAddr, age, pType);
    }

    // ✅ Claim Pension
    function claimPension() public {
        User storage user = users[msg.sender];

        require(user.age > 0, "User not registered");
        require(user.isEligible, "Not eligible");
        require(!user.hasClaimed, "Already claimed");

        uint amount;

        if (user.pensionType == PensionType.OLD_AGE) {
            amount = 1 ether;
        } 
        else if (user.pensionType == PensionType.WIDOW) {
            amount = 1.5 ether;
        } 
        else if (user.pensionType == PensionType.DISABILITY) {
            amount = 2 ether;
        }

        require(address(this).balance >= amount, "Insufficient funds");

        user.hasClaimed = true;
        totalClaimed += amount;

        // ❗ reduce active users after claim
        activeUsers--;

        payable(msg.sender).transfer(amount);

        emit PensionClaimed(msg.sender, amount);
    }

    // ✅ Govt deposits funds
    function depositFunds() public payable {
        require(msg.sender == owner, "Only owner");

        totalFund += msg.value;

        emit FundsDeposited(msg.value);
    }

    // ✅ Dashboard API (single call)
    function getDashboardStats() public view returns (
        uint _totalFund,
        uint _remainingFund,
        uint _activeUsers,
        uint _totalClaimed
    ) {
        return (
            totalFund,
            address(this).balance,
            activeUsers,
            totalClaimed
        );
    }
}