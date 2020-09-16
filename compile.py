# Copyright (c) 2015-2020 Clearmatics Technologies Ltd
#
# SPDX-License-Identifier: LGPL-3.0+
import os
from os.path import join

import solcx
from solcx import compile_files, set_solc_version
from zeth.constants import SOL_COMPILER_VERSION
from zeth.contracts import Interface
from zeth.utils import get_zeth_dir


def compile_mixer() -> Interface:
    """
    Compile the testing ERC20 token contract
    """

    zeth_dir = get_zeth_dir()
    print("***********", zeth_dir)
    allowed_path = join(
        zeth_dir,
        "zeth_contracts/node_modules/openzeppelin-solidity/contracts")
    path_to_token = join(
        zeth_dir,
        "zeth_contracts/node_modules/openzeppelin-solidity/contracts",
        "token/ERC20/ERC20Mintable.sol")
    # Compilation
    set_solc_version(SOL_COMPILER_VERSION)
    compiled_sol = compile_files([path_to_token], allow_paths=allowed_path)
    token_interface = compiled_sol[path_to_token + ":ERC20Mintable"]
    return token_interface


def compile_mixer() -> Interface:
    """
    Compile the testing mixer token contract
    """

    # zeth_dir = "/Users/ruanyang/works/snark-project/zeth/zeth/client"
    # print("***********", zeth_dir)
    # allowed_path = join(
    #     zeth_dir,
    #     "zeth_contracts/contracts")
    path_to_token = join(
        os.path.abspath('.'),
        "contract",
        "mixer","Groth16Mixer.sol")
    # Compilation
    set_solc_version(SOL_COMPILER_VERSION)
    compiled_sol = compile_files([path_to_token], allow_paths=os.path.abspath('.').join("contract"))
    mixer_interface = compiled_sol[path_to_token + ":Groth16Mixer"]
    fo = open("./contract/mixer/abi/Groth16Mixer.abi", "w")
    fo0 = open("./contract/mixer/abi/Groth16Mixer1.abi", "w")
    fo1 = open("./contract/mixer/abi/Groth16Mixer.bin", "w")
    s1 = str(mixer_interface["abi"])
    origin = str(mixer_interface["abi"])
    s2 = s1.replace('True','true')
    s3 = s2.replace('False','false')
    s4 = s3.replace('\'','\"')

    fo.write(s4)
    fo.close()
    fo0.write(origin)
    fo1.write(str(mixer_interface["bin"]))
    fo1.close()


def compile_token():

    zeth_dir = "/Users/ruanyang/works/snark-project/zk-client"
    print("***********", zeth_dir)
    allowed_path = join(
        zeth_dir,
        "contract")
    path_to_token = join(
        zeth_dir,
        "contract",
        "test1.sol")
    # Compilation
    set_solc_version(SOL_COMPILER_VERSION)
    compiled_sol = compile_files([path_to_token], allow_paths=allowed_path)
    token_interface = compiled_sol[path_to_token + ":Test1"]
    fo = open("./contract/Test1.abi", "w")
    fo1 = open("./contract/Test1.bin", "w")
    fo.write(str(token_interface["abi"]))
    fo.close()
    fo1.write(str(token_interface["bin"]))
    fo1.close()






if __name__ == "__main__":
    compile_mixer()  # pylint: disable=no-value-for-parameter
