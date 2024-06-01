// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";


contract GizaWeatherGame is ERC20("GWG", "GWG"), AccessControl{

    bytes32 public constant OWNER_ROLE = keccak256("OWNER_ROLE");

    uint256 public currentRoundId;

    uint public durationInterval;
    uint public settlementInterval;
    uint public multi;

    struct Round {
        uint roundId;
        uint startTimestamp;
        uint durationTimestamp; 
        uint endTimestamp;
        uint256 betAward;
        bool isOver;
        bool isRain;
    }

    struct Bet {
        bool isParticipated;
        bool isBetRain;
        bool isOver;
    }

    mapping(uint => Round) public rounds;
    mapping(address => mapping(uint => Bet)) userBets;


    function createRound(uint startTimestamp, uint probability) external onlyRole(OWNER_ROLE) {
        require(probability <= 100, "Invalid probability");
        currentRoundId++;
        rounds[currentRoundId] = Round({
            roundId: currentRoundId,
            startTimestamp: startTimestamp,
            durationTimestamp: startTimestamp + durationInterval,
            endTimestamp: startTimestamp + settlementInterval,
            betAward: probability * multi,
            isOver: false,
            isRain: false
        });
    }
    

    function placeBet(uint roundId, bool prediction) external {
        Round storage round = rounds[roundId];
        require(!round.isOver, "Round is over");
        require(block.timestamp <= round.durationTimestamp, "Bet time is over");

        Bet storage bet = userBets[msg.sender][roundId];
        require(!bet.isParticipated, "Has participated");
        bet.isParticipated = true;
        bet.isBetRain = prediction;
    }

    function overRound(uint roundId, bool isRain) external onlyRole(OWNER_ROLE) {
        Round storage round = rounds[roundId];
        require(!round.isOver, "Round is over");
        round.isOver = true;
        round.isRain = isRain;
    }

    function claimReward(uint roundId) external {
        Round storage round = rounds[roundId];
        require(round.isOver, "Round isn't over");
        
        Bet storage bet = userBets[msg.sender][roundId];
        require(bet.isParticipated, "Didn't participate");
        require(!bet.isOver, "Reward already claimed");
        require(bet.isBetRain == round.isRain, "Bet error");
        
        bet.isOver = true;
        _mint(msg.sender, round.betAward * 10 ** 18);
    }

    function getRounds(uint[] memory _roundIds) external view returns (Round[] memory res) {
        res = new Round[](_roundIds.length);
        for(uint i; i<_roundIds.length; i) {
            Round memory round = rounds[_roundIds[i]];
            res[i] = round;
        }
    }

    constructor() {
        _grantRole(OWNER_ROLE, msg.sender);
        durationInterval = 1 hours;
        settlementInterval = 1 days;
        multi = 1;
    }

    function grantRole(address newOwner) external onlyRole(OWNER_ROLE) {
        _grantRole(OWNER_ROLE, newOwner);
    }

}