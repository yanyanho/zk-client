# Copyright (c) 2015-2020 Clearmatics Technologies Ltd
#
# SPDX-License-Identifier: LGPL-3.0+

from commands.utils import EtherValue
from click import ClickException

from contract.BAC001 import BAC001
from contract.Groth16Mixer import Groth16Mixer
from python_web3.eth_account.account import Account
from python_web3.client.bcoskeypair import BcosKeyPair
from commands.constants import USER_DIR, FISCO_ADDRESS_FILE
import json
from os.path import exists


def asset_approve(assets: str, mixer_addr: str, asset_addr: str, username: str, password: str) :
    """
    Approve the mixer to spend some amount of assets
    """
    approve_value = EtherValue(assets)
    #eth_addr = load_eth_address(eth_addr)
    #client_ctx = ctx.obj
    #web3 = open_web3_from_ctx(client_ctx)
    #mixer_desc = load_mixer_description_from_ctx(client_ctx)
    #if not mixer_desc.asset:
    #    raise ClickException("no asset for mixer {mixer_desc.mixer.address}")

    asset_instance = BAC001(asset_addr)
    keystore_file = "{}/{}/{}".format(USER_DIR, username, FISCO_ADDRESS_FILE)
    with open(keystore_file, "r") as dump_f:
        keytext = json.load(dump_f)
        privkey = Account.decrypt(keytext, password)
        asset_instance.client.ecdsa_account = Account.from_key(privkey)
        keypair = BcosKeyPair()
        keypair.private_key = asset_instance.client.ecdsa_account.privateKey
        keypair.public_key = asset_instance.client.ecdsa_account.publickey
        keypair.address = asset_instance.client.ecdsa_account.address
        asset_instance.client.keypair = keypair
    print(f"- {username} approves the transfer of BAC001asset to the Mixer")
    out, transactionReceipt = asset_instance.approve(
        mixer_addr,
        approve_value.wei)
    print("approve tranaction output", out)
    outputresult = asset_instance.allowance(asset_instance.client.ecdsa_account.address, mixer_addr)
    print(f"- The allowance for the Mixer from {username} is: {outputresult}")
    return outputresult

if __name__ == '__main__':
    asset_approve()