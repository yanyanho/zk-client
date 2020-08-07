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
        totalAmount: Optional[int]
        ) :
    """
    Deploy the zeth contracts and record the instantiation details.
    """
    # description, string memory shortName, uint8 minUnit, uint256 totalAmount
    constructArgs= [description,shortName,18,totalAmount]
    fo = open("./contract/bac/abi/BAC001.abi")
    abi = fo.read()
    fo.close()
    f1 = open("./contract/bac/abi/BAC001.bin")
    bin = f1.read()
    f1.close()
    client = BcosClient()
    abi1 = [{'inputs': [{'internalType': 'string', 'name': 'description', 'type': 'string'}, {'internalType': 'string', 'name': 'shortName', 'type': 'string'}, {'internalType': 'uint8', 'name': 'minUnit', 'type': 'uint8'}, {'internalType': 'uint256', 'name': 'totalAmount', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'Approval', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'IssuerAdded', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'IssuerRemoved', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'from', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'to', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}, {'indexed': False, 'internalType': 'bytes', 'name': 'data', 'type': 'bytes'}], 'name': 'Send', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'Suspended', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'SuspenderAdded', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'SuspenderRemoved', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'UnSuspended', 'type': 'event'}, {'constant': False, 'inputs': [{'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'addIssuer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'addSuspender', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'internalType': 'address', 'name': 'spender', 'type': 'address'}], 'name': 'allowance', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'approve', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'address', 'name': 'owner', 'type': 'address'}], 'name': 'balance', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'address[]', 'name': 'to', 'type': 'address[]'}, {'internalType': 'uint256[]', 'name': 'values', 'type': 'uint256[]'}, {'internalType': 'bytes', 'name': 'data', 'type': 'bytes'}], 'name': 'batchSend', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'subtractedValue', 'type': 'uint256'}], 'name': 'decreaseAllowance', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'description', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}, {'internalType': 'bytes', 'name': 'data', 'type': 'bytes'}], 'name': 'destroy', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'address', 'name': 'from', 'type': 'address'}, {'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}, {'internalType': 'bytes', 'name': 'data', 'type': 'bytes'}], 'name': 'destroyFrom', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'addedValue', 'type': 'uint256'}], 'name': 'increaseAllowance', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'isIssuer', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'isSuspender', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}, {'internalType': 'bytes', 'name': 'data', 'type': 'bytes'}], 'name': 'issue', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'minUnit', 'outputs': [{'internalType': 'uint8', 'name': '', 'type': 'uint8'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'renounceIssuer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'renounceSuspender', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}, {'internalType': 'bytes', 'name': 'data', 'type': 'bytes'}], 'name': 'send', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'address', 'name': 'from', 'type': 'address'}, {'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}, {'internalType': 'bytes', 'name': 'data', 'type': 'bytes'}], 'name': 'sendFrom', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'shortName', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'suspend', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'suspended', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'totalAmount', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'unSuspend', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}]
    assetTransactionRecipient = client.sendRawTransactionGetReceipt("", abi1, None, constructArgs, bin, 30000000, 15)
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
