# template for codegen
from client.bcosclient import (
    BcosClient
)
from client.datatype_parser import DatatypeParser
from eth_utils import to_checksum_address
import json


class SimpleInfo:  # name of abi
    address = None
    contract_abi_string = '''[{"constant": false, "inputs": [{"name": "b", "type": "uint256"}], "name": "add", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "getaddress", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "getbalance", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "b", "type": "uint256"}], "name": "setbalance", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"name": "plus", "type": "uint256"}], "name": "getbalance1", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "getall", "outputs": [{"name": "", "type": "string"}, {"name": "", "type": "uint256"}, {"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "getname", "outputs": [{"name": "", "type": "string"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "n", "type": "string"}, {"name": "b", "type": "uint256"}, {"name": "a", "type": "address"}], "name": "set", "outputs": [{"name": "", "type": "int256"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [], "name": "reset", "outputs": [{"name": "", "type": "int256"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "getcounter", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [], "name": "setempty", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}, {"payable": false, "stateMutability": "nonpayable", "type": "fallback"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "retcode", "type": "int256"}, {"indexed": false, "name": "name", "type": "string"}, {"indexed": false, "name": "balance", "type": "uint256"}, {"indexed": false, "name": "addr", "type": "address"}, {"indexed": false, "name": "memo", "type": "string"}], "name": "on_set", "type": "event", "topic": "0xf2dd11606b57e733a74ee877736d9c8a3da833d5129301d100669eff223a3829"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "retcode", "type": "int256"}, {"indexed": true, "name": "name", "type": "string"}, {"indexed": false, "name": "balance", "type": "uint256"}, {"indexed": true, "name": "addr", "type": "address"}, {"indexed": false, "name": "memo", "type": "string"}], "name": "on_change", "type": "event", "topic": "0x1c6cf3c083b623fd9a108d037161265f6a736e368fc345d3d8ee6fe3f94cf39f"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "retcode", "type": "int256"}, {"indexed": false, "name": "name", "type": "string"}, {"indexed": false, "name": "balance", "type": "uint256"}, {"indexed": false, "name": "addr", "type": "address"}, {"indexed": false, "name": "memo", "type": "string"}], "name": "on_sender", "type": "event", "topic": "0x37c87e74ec29efa2615574aeb214b87c3bb72c1e1fa9fee2892dce36a7e7f3b2"}, {"anonymous": true, "inputs": [{"indexed": false, "name": "retcode", "type": "int256"}, {"indexed": true, "name": "name", "type": "string"}], "name": "on_reset", "type": "event", "topic": "0x9540f234b204da235110a66168f5feb9940a8551da5172974c67392c147630d0"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "msg", "type": "string"}], "name": "on_set_empty", "type": "event", "topic": "0x447fb56343d9108e0b2708a0aa57837bc8f847356d9119daae2d724f6f0724e1"}]'''
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
    def add(self, b):
        func_name = 'add'
        args = [b]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def getaddress(self):
        func_name = 'getaddress'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def getbalance(self):
        func_name = 'getbalance'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def setbalance(self, b):
        func_name = 'setbalance'
        args = [b]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def getbalance1(self, plus):
        func_name = 'getbalance1'
        args = [plus]
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def getall(self):
        func_name = 'getall'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def getname(self):
        func_name = 'getname'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def set(self, n, b, a):
        func_name = 'set'
        args = [n, b, to_checksum_address(a)]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def reset(self):
        func_name = 'reset'
        args = []
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def getcounter(self):
        func_name = 'getcounter'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def setempty(self):
        func_name = 'setempty'
        args = []
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt
