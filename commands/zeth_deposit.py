# Copyright (c) 2015-2020 Clearmatics Technologies Ltd
#
# SPDX-License-Identifier: LGPL-3.0+

from commands.utils import create_zeth_client_and_mixer_desc, \
    load_zeth_address, open_wallet, parse_output, do_sync
from zeth.constants import JS_INPUTS, JS_OUTPUTS
from commands.constants import PROVER_SERVER_ENDPOINT_DEFAULT
from zeth.mixer_client import ZethAddressPub
from zeth.utils import EtherValue, from_zeth_units
from api.zeth_messages_pb2 import ZethNote
from click import command, option, pass_context, ClickException, Context
from typing import List, Tuple, Optional
import sys
sys.path.append('../')
from contract.Groth16Mixer import Groth16Mixer
from python_web3.eth_account.account import Account

@command()
@option("--mixer-addr", help="The Groth16Mixer contract address you want to use")
@option("--username", help="The account you want to use")
@option("--password", help="the password of you keystore")
@option("--vin", default="0", help="public in value")
@option("--out", "output_specs", multiple=True, help="<receiver_pub_key>,<value>")
def deposit(
        mixer_addr: str,
        username: str,
        password: str,
        vin: str,
        output_specs: List[str]
        ) -> None:
    """
    Generic mix function
    """
    # Some sanity checks
    if len(output_specs) > JS_OUTPUTS:
        raise ClickException(f"too many outputs (max {JS_OUTPUTS})")

    print(f"vin = {vin}")

    vin_pub = EtherValue(vin)
    zeth_client = create_zeth_client_and_mixer_desc(PROVER_SERVER_ENDPOINT_DEFAULT, mixer_addr, username, password)

    zeth_address = load_zeth_address(username)
    wallet = open_wallet(
        zeth_client.mixer_instance, zeth_address.addr_sk, username)

    outputs: List[Tuple[ZethAddressPub, EtherValue]] = [
        parse_output(out_spec) for out_spec in output_specs]

    # Compute input and output value total and check that they match
    output_note_sum = sum([value for _, value in outputs], EtherValue(0))
    if vin_pub != output_note_sum:
        raise ClickException("input and output value mismatch")

    #eth_address = load_eth_address(eth_addr)
    fisco_bcos_address = zeth_client.mixer_instance.client.ecdsa_account.address
    # If instance uses an ERC20 token, tx_value can be 0 not default vin_pub.
    tx_value: Optional[EtherValue] = EtherValue(0)
    #if mixer_desc.token:
    #    tx_value = EtherValue(0)

    (outputresult, receipt) = zeth_client.deposit(
        wallet.merkle_tree,
        zeth_address,
        fisco_bcos_address,
        vin_pub,
        outputs,
        tx_value)

    print("receipt status: ", receipt['status'])
    #do_sync(wallet, receipt)
if __name__ == '__main__':
    deposit()