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
from python_web3.eth_utils import to_checksum_address
from python_web3.client.bcosclient import BcosClient
from contract.Groth16Mixer import Groth16Mixer
from zeth.prover_client import ProverClient
from zeth.mixer_client import write_verification_key
from zeth.zksnark import get_zksnark_provider
from commands.constants import PROVER_SERVER_ENDPOINT_DEFAULT


def deploy(
        token_address: Optional[str]
        ) :
    """
    Deploy the zeth contracts and record the instantiation details.
    """
    zksnark = get_zksnark_provider("GROTH16")
    prover_client = ProverClient(PROVER_SERVER_ENDPOINT_DEFAULT)
    vk_obj = prover_client.get_verification_key()
    vk_json = zksnark.parse_verification_key(vk_obj)
    #print("VK.json: ", vk_json)

    print("Received VK, writing verification key...")
    write_verification_key(vk_json)
    verification_key_params = zksnark.verification_key_parameters(vk_json)
    constructArgs = [5, to_checksum_address(token_address), verification_key_params['Alpha'], verification_key_params['Beta1'], verification_key_params['Beta2'], verification_key_params['Delta1'], verification_key_params['Delta2'], verification_key_params['ABC_coords']]

    si = Groth16Mixer("")
    fo = open("./contract/mixer/abi/Groth16Mixer.abi")
    abi = fo.read()
    fo.close()
    f1 = open("./contract/mixer/abi/Groth16Mixer.bin")
    bin = f1.read()
    f1.close()
    abi1 = [{'inputs': [{'internalType': 'uint256', 'name': 'mk_depth', 'type': 'uint256'}, {'internalType': 'address', 'name': 'token', 'type': 'address'}, {'internalType': 'uint256[2]', 'name': 'Alpha', 'type': 'uint256[2]'}, {'internalType': 'uint256[2]', 'name': 'Beta1', 'type': 'uint256[2]'}, {'internalType': 'uint256[2]', 'name': 'Beta2', 'type': 'uint256[2]'}, {'internalType': 'uint256[2]', 'name': 'Delta1', 'type': 'uint256[2]'}, {'internalType': 'uint256[2]', 'name': 'Delta2', 'type': 'uint256[2]'}, {'internalType': 'uint256[]', 'name': 'ABC_coords', 'type': 'uint256[]'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'string', 'name': 'message', 'type': 'string'}], 'name': 'LogDebug', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'bytes32', 'name': 'message', 'type': 'bytes32'}], 'name': 'LogDebug', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'bytes32', 'name': 'root', 'type': 'bytes32'}, {'indexed': False, 'internalType': 'bytes32[2]', 'name': 'nullifiers', 'type': 'bytes32[2]'}, {'indexed': False, 'internalType': 'bytes32[2]', 'name': 'commitments', 'type': 'bytes32[2]'}, {'indexed': False, 'internalType': 'bytes[2]', 'name': 'ciphertexts', 'type': 'bytes[2]'}], 'name': 'LogMix', 'type': 'event'}, {'constant': True, 'inputs': [{'internalType': 'uint256[9]', 'name': 'primary_inputs', 'type': 'uint256[9]'}], 'name': 'assemble_hsig', 'outputs': [{'internalType': 'bytes32', 'name': 'hsig', 'type': 'bytes32'}], 'payable': False, 'stateMutability': 'pure', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'uint256', 'name': 'index', 'type': 'uint256'}, {'internalType': 'uint256[9]', 'name': 'primary_inputs', 'type': 'uint256[9]'}], 'name': 'assemble_nullifier', 'outputs': [{'internalType': 'bytes32', 'name': 'nf', 'type': 'bytes32'}], 'payable': False, 'stateMutability': 'pure', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'uint256[9]', 'name': 'primary_inputs', 'type': 'uint256[9]'}], 'name': 'assemble_public_values', 'outputs': [{'internalType': 'uint256', 'name': 'vpub_in', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'vpub_out', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'pure', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'get_constants', 'outputs': [{'internalType': 'uint256', 'name': 'js_in', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'js_out', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'num_inputs', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'pure', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'bytes32', 'name': 'commitment', 'type': 'bytes32'}], 'name': 'insert', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'uint256[2]', 'name': 'a', 'type': 'uint256[2]'}, {'internalType': 'uint256[4]', 'name': 'b', 'type': 'uint256[4]'}, {'internalType': 'uint256[2]', 'name': 'c', 'type': 'uint256[2]'}, {'internalType': 'uint256[4]', 'name': 'vk', 'type': 'uint256[4]'}, {'internalType': 'uint256', 'name': 'sigma', 'type': 'uint256'}, {'internalType': 'uint256[9]', 'name': 'input', 'type': 'uint256[9]'}, {'internalType': 'bytes[2]', 'name': 'ciphertexts', 'type': 'bytes[2]'}], 'name': 'mix', 'outputs': [], 'payable': True, 'stateMutability': 'payable', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}, {'internalType': 'address', 'name': '', 'type': 'address'}, {'internalType': 'uint256', 'name': '', 'type': 'uint256'}, {'internalType': 'bytes', 'name': '', 'type': 'bytes'}], 'name': 'onBAC001Received', 'outputs': [{'internalType': 'bytes4', 'name': '', 'type': 'bytes4'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'token', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}]
    client = BcosClient()
    mixerTransactionRecipient = client.sendRawTransactionGetReceipt("", abi1, None, constructArgs, bin)
    mixer_address = mixerTransactionRecipient['contractAddress']
    print(f"deploy: mixer_address={mixer_address}")
    #mixer_instance = Groth16Mixer(address)
    return mixer_address


if __name__ == '__main__':
    deploy()

