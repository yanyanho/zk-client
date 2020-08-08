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
import ast
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
    '''
    fo = open("./contract/mixer/abi/Groth16Mixer.abi")
    abistring = fo.read()
    abi = json.loads(abistring)
    fo.close()
    f1 = open("./contract/mixer/abi/Groth16Mixer.bin")
    bin = f1.read()
    f1.close()
    '''
    abi = []
    binstr = ""
    with open("./contract/mixer/abi/Groth16Mixer.abi", "r") as abistring:
        abistr = abistring.readlines()[0]
        abi = ast.literal_eval(abistr)
    with open("./contract/mixer/abi/Groth16Mixer.bin", "r") as binstring:
        binstr = binstring.readlines()[0]

    client = BcosClient()
    mixerTransactionRecipient = client.sendRawTransactionGetReceipt("", abi, None, constructArgs, binstr)
    mixer_address = mixerTransactionRecipient['contractAddress']
    print(f"deploy: mixer_address={mixer_address}")
    #mixer_instance = Groth16Mixer(address)
    return mixer_address


if __name__ == '__main__':
    deploy()

