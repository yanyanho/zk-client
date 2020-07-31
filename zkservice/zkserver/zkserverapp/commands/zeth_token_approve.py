# Copyright (c) 2015-2020 Clearmatics Technologies Ltd
#
# SPDX-License-Identifier: LGPL-3.0+

from commands.utils import EtherValue
from click import command, argument, option, pass_context, ClickException, Context
import sys
sys.path.append('../')
from contract.Groth16Mixer import Groth16Mixer
from contract.ERC20Mintable import ERC20Mintable
from python_web3.eth_account.account import Account
from python_web3.client.bcoskeypair import BcosKeyPair
from commands.constants import USER_DIR, FISCO_ADDRESS_FILE
import json
from os.path import exists


def token_approve(tokens: str, mixer_addr: str, token_addr: str, username: str, password: str) -> None:
    """
    Approve the mixer to spend some amount of tokens
    """
    approve_value = EtherValue(tokens)
    #eth_addr = load_eth_address(eth_addr)
    #client_ctx = ctx.obj
    #web3 = open_web3_from_ctx(client_ctx)
    #mixer_desc = load_mixer_description_from_ctx(client_ctx)
    #if not mixer_desc.token:
    #    raise ClickException("no token for mixer {mixer_desc.mixer.address}")

    token_instance = ERC20Mintable(token_addr)
    keystore_file = "{}/{}/{}".format(USER_DIR, username, FISCO_ADDRESS_FILE)
    if exists(keystore_file) is False:
        raise ClickException(f"invalid output spec: {keystore_file}")
    with open(keystore_file, "r") as dump_f:
        keytext = json.load(dump_f)
        privkey = Account.decrypt(keytext, password)
        token_instance.client.ecdsa_account = Account.from_key(privkey)
        keypair = BcosKeyPair()
        keypair.private_key = token_instance.client.ecdsa_account.privateKey
        keypair.public_key = token_instance.client.ecdsa_account.publickey
        keypair.address = token_instance.client.ecdsa_account.address
        token_instance.client.keypair = keypair
    print(f"- {username} approves the transfer of ERC20Token to the Mixer")
    token_instance.approve(
        mixer_addr,
        approve_value.wei)
    outputresult = token_instance.allowance(token_instance.client.ecdsa_account.address, mixer_addr)
    print(f"- The allowance for the Mixer from {username} is: {outputresult}")

if __name__ == '__main__':
    token_approve()