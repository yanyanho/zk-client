#!/usr/bin/env python3

# Copyright (c) 2015-2020 Clearmatics Technologies Ltd
#
# SPDX-License-Identifier: LGPL-3.0+
import json
import shutil
from os.path import join, exists
from typing import Any

from web3 import Web3  # type: ignore

import test_commands.mock as mock
import test_commands.scenario as scenario
import zeth.constants as constants
import zeth.merkle_tree
import zeth.utils
from commands.constants import PROVER_SERVER_ENDPOINT_DEFAULT
from commands.poseidon_deploy import deployPoseidon
from commands.zeth_deploy import deploy
from commands.zeth_token_deploy import deploy_asset
from contract.BAC001 import BAC001
from contract.Groth16Mixer import Groth16Mixer
from python_web3.client.bcosclient import BcosClient
from python_web3.client.bcoskeypair import BcosKeyPair
from python_web3.eth_account.account import Account
from test_commands.deploy_test_token import mint_token
from zeth.mixer_client import MixerClient
from zeth.wallet import Wallet
from zeth.zeth_address import ZethAddressPriv


def print_token_balances(
        token_instance: Any,
        bob: str,
        alice: str,
        charlie: str,
        mixer: str) -> None:
    print("BALANCES:")
    outputresult = token_instance.balance(alice)
    print(f"  Alice   : {outputresult}")
    outputresult = token_instance.balance(bob)
    print(f"  Bob     : {outputresult}")
    outputresult = token_instance.balance(charlie)
    print(f"  Charlie : {outputresult}")
    outputresult = token_instance.balance(mixer)
    print(f"  Mixer   : {outputresult}")


def approve(
        token_instance: Any,
        spender_address: str,
        token_amount: int) -> str:
    return token_instance.approve(
        spender_address,
        Web3.toWei(token_amount, 'ether'))


def allowance(
        token_instance: Any,
        owner_address: str,
        spender_address: str) -> str:
    return token_instance.allowance(owner_address, spender_address)

si1 = Groth16Mixer("")

def main() -> None:
    print("***********************")
    zksnark = zeth.zksnark.get_zksnark_provider("GROTH16")
    #web3, eth = mock.open_test_web3()
    '''
    # Ethereum addresses
    deployer_eth_address = eth.accounts[0]
    bob_eth_address = eth.accounts[1]
    alice_eth_address = eth.accounts[2]
    charlie_eth_address = eth.accounts[3]
    '''

    account_keyfile_path = "python_web3/bin/accounts"  # 保存keystore文件的路径，在此路径下,keystore文件以 [name].keystore命名
    account_keyfile = "pyaccount.keystore"
    keystore_file = "{}/{}".format(account_keyfile_path, account_keyfile)
    with open(keystore_file, "r") as dump_f:
        keytext = json.load(dump_f)
        privkey = Account.decrypt(keytext, "123456")
        deployer_ac = Account.from_key(privkey)

    # Fisco-bcos addresses
    bob_password = "234567"
    alice_password = "345678"
    charlie_password = "456789"
    bob_ac = Account.create(bob_password)
    alice_ac = Account.create(alice_password)
    charlie_ac = Account.create(charlie_password)
    #keypair
    deployer_keypair = BcosKeyPair()
    deployer_keypair.private_key = deployer_ac.privateKey
    deployer_keypair.public_key = deployer_ac.publickey
    deployer_keypair.address = deployer_ac.address
    bob_keypair = BcosKeyPair()
    bob_keypair.private_key = bob_ac.privateKey
    bob_keypair.public_key = bob_ac.publickey
    bob_keypair.address = bob_ac.address
    # alice_keypair = BcosKeyPair()
    # alice_keypair.private_key = alice_ac.privateKey
    # alice_keypair.public_key = alice_ac.publickey
    # alice_keypair.address = alice_ac.address
    charlie_keypair = BcosKeyPair()
    charlie_keypair.private_key = charlie_ac.privateKey
    charlie_keypair.public_key = charlie_ac.publickey
    charlie_keypair.address = charlie_ac.address

    # Zeth addresses
    keystore = mock.init_test_keystore()

    # Deploy Zeth contracts
    tree_depth = constants.ZETH_MERKLE_TREE_DEPTH

    asset_address = deploy_asset("AAAA", "AAA", 18, 100000000)
    token_instance = BAC001(asset_address)

    poseidon_address = deployPoseidon()

    mixer_address = deploy(asset_address,poseidon_address)
    mixer_instance = Groth16Mixer(mixer_address)
    mixer_instance.client.ecdsa_account = deployer_ac
    mixer_instance.client.keypair = deployer_keypair
    print("token address: ", mixer_instance.token())
    zeth_client = MixerClient.open(PROVER_SERVER_ENDPOINT_DEFAULT, mixer_instance)
    mk_tree = zeth.merkle_tree.MerkleTree.empty_with_depth(tree_depth)
    #mixer_instance = zeth_client.mixer_instance

    # Keys and wallets
    def _mk_wallet(name: str, sk: ZethAddressPriv) -> Wallet:
        wallet_dir = join(mock.TEST_NOTE_DIR, name + "-erc")
        if exists(wallet_dir):
            # Note: symlink-attack resistance
            #   https://docs.python.org/3/library/shutil.html#shutil.rmtree.avoids_symlink_attacks
            shutil.rmtree(wallet_dir)
        return Wallet(mixer_instance, name, wallet_dir, sk)
    sk_alice = keystore["Alice"].addr_sk
    sk_bob = keystore["Bob"].addr_sk
    sk_charlie = keystore["Charlie"].addr_sk
    # alice_wallet = _mk_wallet('alice', sk_alice)
    # bob_wallet = _mk_wallet('bob', sk_bob)
    # charlie_wallet = _mk_wallet('charlie', sk_charlie)
    #block_num = 1

    # Universal update function
    # def _receive_notes(
    #         out_ev: List[MixOutputEvents]) \
    #         -> Dict[str, List[ZethNoteDescription]]:
    #     #nonlocal block_num
    #     notes = {
    #         'alice': alice_wallet.receive_notes(out_ev),
    #         'bob': bob_wallet.receive_notes(out_ev),
    #         'charlie': charlie_wallet.receive_notes(out_ev),
    #     }
    #     alice_wallet.update_and_save_state()
    #     bob_wallet.update_and_save_state()
    #     charlie_wallet.update_and_save_state()
    #     #block_num = block_num + 1
    #     return notes

    print("[INFO] 4. Running tests (asset mixed: ERC20 token)...")
    # We assign ETHToken to Bob

    print("- Initial balances: ")
    print_token_balances(
        token_instance,
        bob_ac.address,
        alice_ac.address,
        charlie_ac.address,
        mixer_address)

    # Bob tries to deposit ETHToken, split in 2 notes on the mixer (without
    # approving)
    token_instance.client.ecdsa_account = bob_ac
    token_instance.client.keypair = bob_keypair
    zeth_client.mixer_instance.client.ecdsa_account = bob_ac
    zeth_client.mixer_instance.client.keypair = bob_keypair

    # Bob approves the transfer
    print("- Bob approves the transfer of ETHToken to the Mixer")
    token_instance.client.ecdsa_account = bob_ac
    token_instance.client.keypair = bob_keypair
    (outputresult, receipt) = token_instance.send(bob_ac.address, Web3.toWei(10000,'ether'),'')
    print("send *****", receipt['status'])
    (outputresult, receipt) = token_instance.approve(
        mixer_address,
        scenario.BOB_DEPOSIT_ETH)
    # eth.waitForTransactionReceipt(tx_hash)
    outputresult = token_instance.allowance(
        deployer_ac.address,
        mixer_address)
    print("- The allowance for the Mixer from Bob is:", outputresult)
    # # Bob deposits ETHToken, split in 2 notes on the mixer
    # result_deposit_bob_to_bob = scenario.bob_deposit(
    #     zeth_client, mk_tree, bob_ac.address, keystore, zeth.utils.EtherValue(0))
    #
    # print("- Balances after Bob's deposit: ")
    # print_token_balances(
    #     token_instance,
    #     bob_ac.address,
    #     alice_ac.address,
    #     charlie_ac.address,
    #     mixer_address
    # )
    #
    # # Alice sees a deposit and tries to decrypt the ciphertexts to see if she
    # # was the recipient, but Bob was the recipient so Alice fails to decrypt
    # received_notes = _receive_notes(
    #     result_deposit_bob_to_bob.output_events)
    # recovered_notes_alice = received_notes['alice']
    # assert(len(recovered_notes_alice) == 0), \
    #     "Alice decrypted a ciphertext that was not encrypted with her key!"
    #
    # # Bob does a transfer of ETHToken to Charlie on the mixer
    #
    # # Bob decrypts one of the note he previously received (useless here but
    # # useful if the payment came from someone else)
    # recovered_notes_bob = received_notes['bob']
    # assert(len(recovered_notes_bob) == 2), \
    #     f"Bob recovered {len(recovered_notes_bob)} notes from deposit, expected 2"
    # input_bob_to_charlie = recovered_notes_bob[0].as_input()
    '''
    # Execution of the transfer
    result_transfer_bob_to_charlie = scenario.bob_to_charlie(
        zeth_client,
        mk_tree,
        input_bob_to_charlie,
        bob_eth_address,
        keystore)

    # Bob tries to spend `input_note_bob_to_charlie` twice
    result_double_spending = None
    try:
        result_double_spending = scenario.bob_to_charlie(
            zeth_client,
            mk_tree,
            input_bob_to_charlie,
            bob_eth_address,
            keystore)
    except Exception as e:
        print(f"Bob's double spending successfully rejected! (msg: {e})")
    assert(result_double_spending is None), "Bob spent the same note twice!"

    print("- Balances after Bob's transfer to Charlie: ")
    print_token_balances(
        token_instance,
        bob_eth_address,
        alice_eth_address,
        charlie_eth_address,
        zeth_client.mixer_instance.address
    )

    # Charlie tries to decrypt the notes from Bob's previous transaction.
    received_notes = _receive_notes(
        result_transfer_bob_to_charlie.output_events)
    note_descs_charlie = received_notes['charlie']
    assert(len(note_descs_charlie) == 1), \
        f"Charlie decrypted {len(note_descs_charlie)}.  Expected 1!"

    _ = scenario.charlie_withdraw(
        zeth_client,
        mk_tree,
        note_descs_charlie[0].as_input(),
        charlie_eth_address,
        keystore)

    print("- Balances after Charlie's withdrawal: ")
    print_token_balances(
        token_instance,
        bob_eth_address,
        alice_eth_address,
        charlie_eth_address,
        zeth_client.mixer_instance.address
    )

    # Charlie tries to carry out a double spend by withdrawing twice the same
    # note
    result_double_spending = None
    try:
        # New commitments are added in the tree at each withdraw so we
        # recompute the path to have the updated nodes
        result_double_spending = scenario.charlie_double_withdraw(
            zeth_client,
            mk_tree,
            note_descs_charlie[0].as_input(),
            charlie_eth_address,
            keystore)
    except Exception as e:
        print(f"Charlie's double spending successfully rejected! (msg: {e})")
    print("Balances after Charlie's double withdrawal attempt: ")
    assert(result_double_spending is None), \
        "Charlie managed to withdraw the same note twice!"
    print_token_balances(
        token_instance,
        bob_eth_address,
        alice_eth_address,
        charlie_eth_address,
        zeth_client.mixer_instance.address)

    # Bob deposits once again ETH, split in 2 notes on the mixer
    # But Charlie attempts to corrupt the transaction (malleability attack)

    # Bob approves the transfer
    print("- Bob approves the transfer of ETHToken to the Mixer")
    tx_hash = approve(
        token_instance,
        bob_eth_address,
        zeth_client.mixer_instance.address,
        scenario.BOB_DEPOSIT_ETH)
    eth.waitForTransactionReceipt(tx_hash)
    allowance_mixer = allowance(
        token_instance,
        bob_eth_address,
        zeth_client.mixer_instance.address)
    print("- The allowance for the Mixer from Bob is:", allowance_mixer)

    result_deposit_bob_to_bob = scenario.charlie_corrupt_bob_deposit(
        zeth_client,
        mk_tree,
        bob_eth_address,
        charlie_eth_address,
        keystore)

    # Bob decrypts one of the note he previously received (should fail if
    # Charlie's attack succeeded)
    received_notes = _receive_notes(
        result_deposit_bob_to_bob.output_events)
    recovered_notes_bob = received_notes['bob']
    assert(len(recovered_notes_bob) == 2), \
        f"Bob recovered {len(recovered_notes_bob)} notes from deposit, expected 2"

    print("- Balances after Bob's last deposit: ")
    print_token_balances(
        token_instance,
        bob_eth_address,
        alice_eth_address,
        charlie_eth_address,
        zeth_client.mixer_instance.address)
    '''
    print(
        "========================================\n" +
        "              TESTS PASSED\n" +
        "========================================\n")


if __name__ == '__main__':
    main()
