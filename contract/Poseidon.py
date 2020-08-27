# template for codegen
from python_web3.client.bcosclient import (
    BcosClient
)
from python_web3.client.datatype_parser import DatatypeParser
import json


class Poseidon:  # name of abi
    address = None
    contract_abi_string = '''[{"constant": true, "inputs": [{"internalType": "uint256[]", "name": "input", "type": "uint256[]"}], "name": "poseidon", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": false, "stateMutability": "pure", "type": "function"}]'''
    contract_abi = None
    data_parser = DatatypeParser()
    client = None

    def __init__(self, address):
        self.client = BcosClient()
        self.address = address
        self.contract_abi = json.loads(self.contract_abi_string)
        self.data_parser.set_abi(self.contract_abi)

    def deploy(self, contract_bin_file):
        result = self.client.deployFromFile(contract_bin_file)
        self.address = result["contractAddress"]
        return result

    # ------------------------------------------
    def poseidon(self, input):
        func_name = 'poseidon'
        args = [input]
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result
