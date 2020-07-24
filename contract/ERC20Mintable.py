# template for codegen
import sys
sys.path.append('../')
from python_web3.client.bcosclient import (
    BcosClient
)
from python_web3.client.datatype_parser import DatatypeParser
import json

from python_web3.eth_utils import to_checksum_address


class ERC20Mintable:  # name of abi
    address = None
    contract_abi_string = '''[{"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": true, "internalType": "address", "name": "spender", "type": "address"}, {"indexed": false, "internalType": "uint256", "name": "value", "type": "uint256"}], "name": "Approval", "type": "event", "topic": "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "account", "type": "address"}], "name": "MinterAdded", "type": "event", "topic": "0x6ae172837ea30b801fbfcdd4108aa1d5bf8ff775444fd70256b44e6bf3dfc3f6"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "account", "type": "address"}], "name": "MinterRemoved", "type": "event", "topic": "0xe94479a9f7e1952cc78f2d6baab678adc1b772d936c6583def489e524cb66692"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "from", "type": "address"}, {"indexed": true, "internalType": "address", "name": "to", "type": "address"}, {"indexed": false, "internalType": "uint256", "name": "value", "type": "uint256"}], "name": "Transfer", "type": "event", "topic": "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"}, {"constant": false, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "addMinter", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"}], "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "addedValue", "type": "uint256"}], "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "isMinter", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "account", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "mint", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [], "name": "renounceMinter", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "sender", "type": "address"}, {"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transferFrom", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}]'''
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
    def addMinter(self, account):
        func_name = 'addMinter'
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
    def approve(self, spender, amount):
        func_name = 'approve'
        args = [to_checksum_address(spender), amount]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def balanceOf(self, account):
        func_name = 'balanceOf'
        args = [to_checksum_address(account)]
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def decreaseAllowance(self, spender, subtractedValue):
        func_name = 'decreaseAllowance'
        args = [to_checksum_address(spender), subtractedValue]
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
    def isMinter(self, account):
        func_name = 'isMinter'
        args = [to_checksum_address(account)]
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def mint(self, account, amount):
        func_name = 'mint'
        args = [to_checksum_address(account), amount]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def renounceMinter(self):
        func_name = 'renounceMinter'
        args = []
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def totalSupply(self):
        func_name = 'totalSupply'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def transfer(self, recipient, amount):
        func_name = 'transfer'
        args = [to_checksum_address(recipient), amount]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def transferFrom(self, sender, recipient, amount):
        func_name = 'transferFrom'
        args = [to_checksum_address(sender), to_checksum_address(recipient), amount]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt
