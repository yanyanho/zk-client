// Copyright (c) 2015-2020 Clearmatics Technologies Ltd
//
// SPDX-License-Identifier: LGPL-3.0+

pragma solidity ^0.5.0;

import "./Poseidon.sol";

// The Merkle tree implementation must trade-off complexity, storage,
// initialization cost, and update & root computation cost.
//
// This implementation stores all leaves and nodes, skipping those that have
// not been populated yet. The final entry in each layer stores that layer's
// default value.
contract MerkleTreePos
{
    uint256 constant MASK_LS_BIT = ~uint256(1);

    constructor(uint256 treeDepth, address poseidon)  public
    {
           // Constructor
        poseidonAddress = poseidon;
        require (
            treeDepth == DEPTH,
            "Invalid depth in BaseMerkleTree");
        initializeTree();
    }

    function recomputeRoot(uint num_new_leaves) internal returns (bytes32)
    {
        // Assume `num_new_leaves` have been written into the leaf slots.
        // Update any affected nodes in the tree, up to the root, using the
        // default values for any missing nodes.

        uint256 end_idx = num_leaves;
        uint256 start_idx = num_leaves - num_new_leaves;
        uint256 layer_size = MAX_NUM_LEAVES;

        while (layer_size > 1) {
            (start_idx, end_idx) =
                recomputeParentLayer(layer_size, start_idx, end_idx);
            layer_size = layer_size / 2;
        }

        return nodesWithMid[mid][0];
    }

    // Recompute nodes in the parent layer that are affected by entries
    // [child_start_idx, child_end_idx[ in the child layer.  If
    // `child_end_idx` is required in the calculation, the final entry of
    // the child layer is used (since this contains the default entry for
    // the layer if the tree is not full).
    //
    //            /     \         /     \         /     \
    // Parent:   ?       ?       F       G       H       0
    //          / \     / \     / \     / \     / \     / \
    // Child:  ?   ?   ?   ?   A   B   C   D   E   ?   ?   0
    //                         ^                   ^
    //                child_start_idx         child_end_idx
    //
    // Returns the start and end indices (within the parent layer) of touched
    // parent nodes.
    function recomputeParentLayer(
        uint256 child_layer_size,
        uint256 child_start_idx,
        uint256 child_end_idx)
        private
        returns (uint256, uint256)
    {
        uint256 child_layer_start = child_layer_size - 1;


        // Start at the right and iterate left, so we only execute the
        // default_value logic once.  child_left_idx_rend (reverse-end) is the
        // smallest value of child_left_idx at which we should recompute the
        // parent node hash.

        uint256 child_left_idx_rend =
            child_layer_start + (child_start_idx & MASK_LS_BIT);

        // If child_end_idx is odd, it is the RIGHT of a computation we need to
        // make.  Do the computation using the default value, and move to the
        // next pair (on the left).  Otherwise, we have a fully populated pair.

        //-----------fix------------//
        uint256 child_left_idx;
        if ((child_end_idx & 1) != 0) {
            child_left_idx = child_layer_start + child_end_idx - 1;
             uint256[] memory input = new uint[](2);
             input[0] = uint256(nodesWithMid[mid][child_left_idx]);
             input[1] = uint256(nodesWithMid[mid][2 * child_layer_start]);

            nodesWithMid[mid][(child_left_idx - 1) / 2] = bytes32(Poseidon(poseidonAddress).poseidon(input));
        } else {
            child_left_idx = child_layer_start + child_end_idx;
        }

        // At this stage, pairs are all populated.  Compute until we reach
        // child_left_idx_rend.

        while (child_left_idx > child_left_idx_rend) {
             child_left_idx = child_left_idx - 2;
             uint256[] memory input = new uint[](2);
             input[0] = uint256(nodesWithMid[mid][child_left_idx]);
             input[1] = uint256(nodesWithMid[mid][child_left_idx + 1]);

             nodesWithMid[mid][(child_left_idx - 1) / 2] = bytes32(Poseidon(poseidonAddress).poseidon(input));
        }

        return (child_start_idx / 2, (child_end_idx + 1) / 2);
    }


    //----------------------basemerkeltree--------------------//
      // cpp prover)
    uint256 constant DEPTH = 5;

    // Number of leaves
    uint256 constant MAX_NUM_LEAVES = 2**DEPTH;

    // Number of nodes
    uint constant MAX_NUM_NODES = (MAX_NUM_LEAVES * 2) - 1;

    bytes32 constant DEFAULT_LEAF_VALUE = 0x0;

    // Array containing the 2^(depth) leaves of the merkle tree.  We can switch
    // the leaves to be of type bytes and not bytes32 to support digest of
    // various size (eg: if we use different hash functions).  That way we'd
    // have a merkle tree for any type of hash function (that can be implemented
    // as a precompiled contract for instance)
    //
    // Leaves is a 2D array

    // Sparse array of populated leaves of the merkle tree.  Unpopulated leaves
    // have the DEFAULT_LEAF_VALUE.
    uint  public mid = 0;
//    bytes32[MAX_NUM_NODES] nodes;
    mapping(uint => bytes32[MAX_NUM_NODES]) nodesWithMid;
    // Number of leaves populated in `nodes`.
    uint256 num_leaves;
    address poseidonAddress;

    // Debug only
    event LogDebug(bytes32 message);


      function initializeTree() internal
    {
        // First layer
        bytes32 default_value = DEFAULT_LEAF_VALUE;

        nodesWithMid[mid][2 * MAX_NUM_LEAVES - 2] = default_value;
        uint256 layer_size = MAX_NUM_LEAVES / 2;


        // Subsequent layers
        while (layer_size > 0) {
              uint256[] memory input = new uint[](2);
              input[0] = uint256(default_value);
              input[1] = uint256(default_value);
            default_value = bytes32(Poseidon(poseidonAddress).poseidon(input));
            uint256 layer_final_entry_idx = 2 * layer_size - 2;
            nodesWithMid[mid][layer_final_entry_idx] = default_value;
            layer_size = layer_size / 2;
        }
    }

    // Appends a commitment to the tree, and returns its address
    function insert(bytes32 commitment) public {

        // If this require fails => the merkle tree is full, we can't append
        // leaves anymore.
         if( num_leaves==MAX_NUM_LEAVES) {
             mid = mid+1;
             num_leaves =  num_leaves % MAX_NUM_LEAVES;
             initializeTree();
         }

        require(
            num_leaves < MAX_NUM_LEAVES,
            "Merkle tree full: Cannot append anymore"
        );

        // Address of the next leaf is the current number of leaves (before
        // insertion).  Compute the next index in the full set of nodes, and
        // write.

        uint256 next_address = num_leaves;
        ++num_leaves;
        uint256 next_entry_idx = (MAX_NUM_LEAVES - 1) + next_address;
        nodesWithMid[mid][next_entry_idx] = commitment;
    }
}
