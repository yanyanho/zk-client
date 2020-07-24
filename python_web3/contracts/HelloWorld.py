# template for codegen
from client.bcosclient import (
    BcosClient
)
from client.datatype_parser import DatatypeParser
import json


class HelloWorld:  # name of abi
    address = None
    contract_abi_string = '''[{"constant": false, "inputs": [{"name": "n", "type": "string"}], "name": "set", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "get", "outputs": [{"name": "", "type": "string"}], "payable": false, "stateMutability": "view", "type": "function"}, {"inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "newname", "type": "string"}], "name": "onset", "type": "event", "topic": "0xafb180742c1292ea5d67c4f6d51283ecb11e49f8389f4539bef82135d689e118"}]'''
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
    def set(self, n):
        func_name = 'set'
        args = [n]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def get(self):
        func_name = 'get'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result
