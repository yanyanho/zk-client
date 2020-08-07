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
import json

from click import Context, command, option, pass_context
from typing import Optional
from web3 import Web3
#from test_commands.deploy_test_asset import mint_asset
from contract.BAC001 import BAC001
from python_web3.client.bcosclient import BcosClient


def deploy_asset(
        description,
        shortName,
        minUnit,
        total_amount: Optional[int]
        ) :
    """
    Deploy the zeth contracts and record the instantiation details.
    """
    # description, string memory shortName, uint8 minUnit, uint256 totalAmount
    constructArgs= [description,shortName,18,total_amount]
    fo = open("./contract/bac/abi/BAC001.abi")
    abi = fo.read()
    fo.close()
    f1 = open("./contract/bac/abi/BAC001.bin")
    bin = f1.read()
    f1.close()
    client = BcosClient()
    assetTransactionRecipient = client.sendRawTransactionGetReceipt("", abi, None, constructArgs, bin, 30000000, 15)
    asset_address = assetTransactionRecipient['contractAddress']
    asset_instance = BAC001(asset_address)
    print(f"deploy: asset_address= {asset_address}")
    # asset_instance.issue(
    #     miner_address,
    #     Web3.toWei(asset_amount, 'ether'), '')
    # print("- Initial balances: ")
    # outputresult = asset_instance.balanceOf(miner_address)
    # print(f"  {miner_address}     : {outputresult}")
    return asset_address

if __name__ == '__main__':
    deploy_asset()
