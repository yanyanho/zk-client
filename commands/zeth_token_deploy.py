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
from web3 import Web3
import sys
sys.path.append('../')
from contract.ERC20Mintable import ERC20Mintable
#from test_commands.deploy_test_token import mint_token



@command()
@option("--miner-address", help="Address of miner")
@option("--token-amount", help="amount of token been mint")
@pass_context
def deploy_token(
        ctx: Context,
        miner_address: Optional[str],
        token_amount: Optional[int]
        ) -> None:
    """
    Deploy the zeth contracts and record the instantiation details.
    """
    token_si = ERC20Mintable("")
    token_result = token_si.deploy("contract/ERC20Mintable.bin")
    token_address = token_result['contractAddress']
    token_instance = ERC20Mintable(token_address)
    print(f"deploy: token_address={token_address}")
    token_instance.mint(
        miner_address,
        Web3.toWei(token_amount, 'ether'))
    print("- Initial balances: ")
    outputresult = token_instance.balanceOf(miner_address)
    print(f"  {miner_address}     : {outputresult}")

if __name__ == '__main__':
    deploy_token()
