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

@command()
@argument("tokens")
#@option("--eth-addr", help="Sender eth address or address filename")
@option("--wait", is_flag=True, help="Wait for transaction to complete")
@option("--mixer-addr", help="The Groth16Mixer contract address you want to use")
@option("--ERC20Mintable-addr", help="The Groth16Mixer contract address you want to use")
@option("--password", help="the password of you keystore")
@pass_context
def token_approve(ctx: Context, tokens: str, mixer_addr: str, ERC20Mintable_addr: str, password: str, wait: bool) -> None:
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

    token_instance = ERC20Mintable(ERC20Mintable_addr)
    keystore_file = "pyaccount.keystore"
    token_instance.client.keystore_file = "pyaccount.keystore"
    if os.path.exists(keystore_file) is False:
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
    (outputresult, receipt) = token_instance.approve(
        mixer_addr,
        approve_value.wei)

    print("receipt output :", outputresult)