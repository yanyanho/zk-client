// Copyright (c) 2015-2020 Clearmatics Technologies Ltd
//
// SPDX-License-Identifier: LGPL-3.0+

pragma solidity ^0.5.0;

contract Test1 {

    function check_mkroot_nullifiers_hsig_append_nullifiers_state(
        uint256[4] memory vk,
        uint256[2] memory nfs)
        public returns (uint256 ){
        // 1. We re-assemble the full root digest and check it is in the tree

        // 3. We re-compute h_sig, re-assemble the expected h_sig and check
        // they are equal (i.e. that h_sig re-assembled was correctly generated
        // from vk).
        bytes32[] memory nfs1 = new bytes32[](2);
        nfs1[0] = bytes32(nfs[0]);
        nfs1[1] = bytes32(nfs[1]);
        bytes32 expected_hsig = sha256(abi.encodePacked(nfs1, vk));

        //expected_hsig =  expected_hsig >> 3;
        uint p_mod = 21888242871839275222246405745257275088548364400416034343698204186575808495617;
        uint expected_hsig_mod =  uint256(expected_hsig) % p_mod;

        return  expected_hsig_mod;
    }
}
