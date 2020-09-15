# template for codegen
from python_web3.client.bcosclient import (
    BcosClient
)
from python_web3.client.datatype_parser import DatatypeParser
import json


class Test1:  # name of abi
    address = None
    contract_abi_string = '''[{"constant": false, "inputs": [{"internalType": "uint256[4]", "name": "vk", "type": "uint256[4]"}, {"internalType": "uint256[2]", "name": "nfs", "type": "uint256[2]"}], "name": "check_mkroot_nullifiers_hsig_append_nullifiers_state", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}]'''
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
    def check_mkroot_nullifiers_hsig_append_nullifiers_state(self, vk, nfs):
        func_name = 'check_mkroot_nullifiers_hsig_append_nullifiers_state'
        args = [vk, nfs]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt
