# template for codegen
from eth_utils import to_checksum_address

from python_web3.client.bcosclient import (
    BcosClient
)
from python_web3.client.datatype_parser import DatatypeParser
import json


class BAC001:  # name of abi
    address = None
    contract_abi_string = '''[{"inputs": [{"internalType": "string", "name": "description", "type": "string"}, {"internalType": "string", "name": "shortName", "type": "string"}, {"internalType": "uint8", "name": "minUnit", "type": "uint8"}, {"internalType": "uint256", "name": "totalAmount", "type": "uint256"}], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": true, "internalType": "address", "name": "spender", "type": "address"}, {"indexed": false, "internalType": "uint256", "name": "value", "type": "uint256"}], "name": "Approval", "type": "event", "topic": "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "account", "type": "address"}], "name": "IssuerAdded", "type": "event", "topic": "0x05e7c881d716bee8cb7ed92293133ba156704252439e5c502c277448f04e20c2"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "account", "type": "address"}], "name": "IssuerRemoved", "type": "event", "topic": "0xaf66545c919a3be306ee446d8f42a9558b5b022620df880517bc9593ec0f2d52"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "from", "type": "address"}, {"indexed": true, "internalType": "address", "name": "to", "type": "address"}, {"indexed": false, "internalType": "uint256", "name": "value", "type": "uint256"}, {"indexed": false, "internalType": "bytes", "name": "data", "type": "bytes"}], "name": "Send", "type": "event", "topic": "0x76d4fc8756cf1c2b5aa667285d8c20b304dcd86209b4c34a84fc491867de76f1"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "address", "name": "account", "type": "address"}], "name": "Suspended", "type": "event", "topic": "0x6f123d3d54c84a7960a573b31c221dcd86e13fd849c5adb0c6ca851468cc1ae4"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "account", "type": "address"}], "name": "SuspenderAdded", "type": "event", "topic": "0xf4fbb5a5e62a703643fe5be0722720f728980fdde74f11d76eca7e13bdc3301d"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "account", "type": "address"}], "name": "SuspenderRemoved", "type": "event", "topic": "0x17eb45856cd2283111eeb8a1dddf8a43121889e3ce798241f96d2afed353eaa3"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "address", "name": "account", "type": "address"}], "name": "UnSuspended", "type": "event", "topic": "0x349b4285cb8dde314c53fd9d8e8e578381a7375e4f76f9dd9fe07f9960f120a4"}, {"constant": false, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "addIssuer", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "addSuspender", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "value", "type": "uint256"}], "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"internalType": "address", "name": "owner", "type": "address"}], "name": "balance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address[]", "name": "to", "type": "address[]"}, {"internalType": "uint256[]", "name": "values", "type": "uint256[]"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "batchSend", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"}], "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "description", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"internalType": "uint256", "name": "value", "type": "uint256"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "destroy", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "uint256", "name": "value", "type": "uint256"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "destroyFrom", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "addedValue", "type": "uint256"}], "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "isIssuer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "isSuspender", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "value", "type": "uint256"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "issue", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "minUnit", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [], "name": "renounceIssuer", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [], "name": "renounceSuspender", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "value", "type": "uint256"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "send", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "value", "type": "uint256"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "sendFrom", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "shortName", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [], "name": "suspend", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "suspended", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "totalAmount", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [], "name": "unSuspend", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}]'''
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
    def addIssuer(self, account):
        func_name = 'addIssuer'
        args = [to_checksum_address(account)]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def addSuspender(self, account):
        func_name = 'addSuspender'
        args = [to_checksum_address(account)]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def allowance(self, owner, spender):
        func_name = 'allowance'
        args = [to_checksum_address(owner), to_checksum_address(spender)]
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def approve(self, spender, value):
        func_name = 'approve'
        args = [to_checksum_address(spender), value]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def balance(self, owner):
        func_name = 'balance'
        args = [to_checksum_address(owner)]
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def batchSend(self, to, values, data):
        func_name = 'batchSend'
        args = [to, values, data]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def decreaseAllowance(self, spender, subtractedValue):
        func_name = 'decreaseAllowance'
        args = [to_checksum_address(spender), subtractedValue]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def description(self):
        func_name = 'description'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def destroy(self, value, data):
        func_name = 'destroy'
        args = [value, data]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def destroyFrom(self, from1, value, data):
        func_name = 'destroyFrom'
        args = [to_checksum_address(from1), value, data]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def increaseAllowance(self, spender, addedValue):
        func_name = 'increaseAllowance'
        args = [to_checksum_address(spender), addedValue]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def isIssuer(self, account):
        func_name = 'isIssuer'
        args = [to_checksum_address(account)]
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def isSuspender(self, account):
        func_name = 'isSuspender'
        args = [to_checksum_address(account)]
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def issue(self, to, value, data):
        func_name = 'issue'
        args = [to_checksum_address(to), value, data]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def minUnit(self):
        func_name = 'minUnit'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def renounceIssuer(self):
        func_name = 'renounceIssuer'
        args = []
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def renounceSuspender(self):
        func_name = 'renounceSuspender'
        args = []
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def send(self, to, value, data):
        func_name = 'send'
        args = [to_checksum_address(to), value, data]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def sendFrom(self, from1, to, value, data):
        func_name = 'sendFrom'
        args = [to_checksum_address(from1), to_checksum_address(to), value, data]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def shortName(self):
        func_name = 'shortName'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def suspend(self):
        func_name = 'suspend'
        args = []
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def suspended(self):
        func_name = 'suspended'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def totalAmount(self):
        func_name = 'totalAmount'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def unSuspend(self):
        func_name = 'unSuspend'
        args = []
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt
