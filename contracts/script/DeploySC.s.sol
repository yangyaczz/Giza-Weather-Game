// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

import {GizaWeatherGame} from "../src/GizaWeatherGame.sol";
import "forge-std/Script.sol";

contract Deploy is Script {
    GizaWeatherGame public gwg;
    address bob = 0x40ac93Ef2b3A5162466fef7308A6097BdA61D3c1;

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        gwg = new GizaWeatherGame();
        gwg.grantRole(bob);
        vm.stopBroadcast();
    } 
    
    // forge script script/DeploySC.s.sol:Deploy --rpc-url https://eth-sepolia.public.blastapi.io --broadcast --verify -vvvv 
    // forge script script/DeploySC.s.sol:Deploy --rpc-url https://eth-sepolia.public.blastapi.io --verify --resume
}
