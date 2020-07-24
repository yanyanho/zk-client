# Copyright (c) 2015-2020 Clearmatics Technologies Ltd
#
# SPDX-License-Identifier: LGPL-3.0+
'''
from commands.utils import \
    open_web3_from_ctx, get_erc20_instance_description, load_eth_address, \
    write_mixer_description, MixerDescription
from zeth.mixer_client import MixerClient
from zeth.utils import EtherValue
'''
from click import Context, command, option, pass_context
from typing import Optional
import sys
sys.path.append('../')
from contract.Groth16Mixer import Groth16Mixer


@command()
#@option("--eth-addr", help="Sender eth address or address filename")
#@option("--token-address", help="Address of token contract (if used)")
@pass_context
def deploy(
        ctx: Context
        #eth_addr: Optional[str],
        ) -> None:
    """
    Deploy the zeth contracts and record the instantiation details.
    """
    #eth_address = load_eth_address(eth_addr)
    #client_ctx = ctx.obj
    #web3 = open_web3_from_ctx(client_ctx)
    #deploy_gas_value = EtherValue(deploy_gas, 'wei') if deploy_gas else None

    #print(f"deploy: eth_address={eth_address}")
    #print(f"deploy: token_address={token_address}")

    #token_instance = bac(token_address) \
    #    if token_address else None
    si = Groth16Mixer("")
    result = si.deploy("contract/Groth16Mixer.bin")
    address = result['contractAddress']
    print(f"deploy: mixer_address={address}")
    #mixer_instance = Groth16Mixer(address)

