// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.25;

import {Test, console2} from "forge-std/Test.sol";
import {GizaWeatherGame} from "../src/GizaWeatherGame.sol";

contract gwg is Test {
    GizaWeatherGame public gwg;

    address alice = 0xBEbAF2a9ad714fEb9Dd151d81Dd6d61Ae0535646;
    address bob = 0x40ac93Ef2b3A5162466fef7308A6097BdA61D3c1;

    function setUp() public {
        vm.startPrank(alice);
        gwg = new GizaWeatherGame();
        gwg.grantRole(bob);
        vm.stopPrank();
    }

    function test_create() public {
        vm.startPrank(bob);
        gwg.createRound(0, 37);
        vm.stopPrank();
    }

    function test_bet() public {
        test_create();
        gwg.placeBet(1, true);
    }
    
    function test_over() public {
        test_bet();
        vm.warp(block.timestamp + 2 hours);

        vm.startPrank(bob);
        gwg.overRound(1, true);
        vm.stopPrank();
    }

    function test_claim() public {
        test_over();
        
        gwg.claimReward(1);
        console2.log('balance', gwg.balanceOf(address(this)));
    }

} // forge test --match-path test/gwg.t.sol
