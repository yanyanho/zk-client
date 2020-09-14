# template for codegen
from eth_utils import to_checksum_address

from python_web3.client.bcosclient import (
    BcosClient
)
from python_web3.client.datatype_parser import DatatypeParser
import json


class Groth16Mixer:  # name of abi
    address = None
    contract_abi_string = '''[{"inputs": [{"internalType": "uint256", "name": "mk_depth", "type": "uint256"}, {"internalType": "address", "name": "token", "type": "address"}, {"internalType": "address", "name": "poseidonAddress", "type": "address"}, {"internalType": "uint256[2]", "name": "Alpha", "type": "uint256[2]"}, {"internalType": "uint256[2]", "name": "Beta1", "type": "uint256[2]"}, {"internalType": "uint256[2]", "name": "Beta2", "type": "uint256[2]"}, {"internalType": "uint256[2]", "name": "Delta1", "type": "uint256[2]"}, {"internalType": "uint256[2]", "name": "Delta2", "type": "uint256[2]"}, {"internalType": "uint256[]", "name": "ABC_coords", "type": "uint256[]"}], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "string", "name": "message", "type": "string"}], "name": "LogDebug", "type": "event", "topic": "0xd44da6836c8376d1693e8b9cacf1c39b9bed3599164ad6d8e60902515f83938e"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "bytes32", "name": "message", "type": "bytes32"}], "name": "LogDebug", "type": "event", "topic": "0x05e46912c9be87d8a6830598db8544b61884d9d22f3921597a9a6e8a340914b3"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "mid", "type": "uint256"}, {"indexed": false, "internalType": "bytes32", "name": "root", "type": "bytes32"}, {"indexed": false, "internalType": "bytes32[2]", "name": "nullifiers", "type": "bytes32[2]"}, {"indexed": false, "internalType": "bytes32[2]", "name": "commitments", "type": "bytes32[2]"}, {"indexed": false, "internalType": "bytes[2]", "name": "ciphertexts", "type": "bytes[2]"}], "name": "LogMix", "type": "event", "topic": "0x5b20d7b970f991ad433adaa73d15ec55f2dc64ddfecb9505eb1f94e330ecddf7"}, {"constant": true, "inputs": [{"internalType": "uint256[10]", "name": "primary_inputs", "type": "uint256[10]"}], "name": "assemble_hsig", "outputs": [{"internalType": "bytes32", "name": "hsig", "type": "bytes32"}], "payable": false, "stateMutability": "pure", "type": "function"}, {"constant": true, "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}, {"internalType": "uint256[10]", "name": "primary_inputs", "type": "uint256[10]"}], "name": "assemble_nullifier", "outputs": [{"internalType": "bytes32", "name": "nf", "type": "bytes32"}], "payable": false, "stateMutability": "pure", "type": "function"}, {"constant": true, "inputs": [{"internalType": "uint256[10]", "name": "primary_inputs", "type": "uint256[10]"}], "name": "assemble_public_values", "outputs": [{"internalType": "uint256", "name": "vpub_in", "type": "uint256"}, {"internalType": "uint256", "name": "vpub_out", "type": "uint256"}], "payable": false, "stateMutability": "pure", "type": "function"}, {"constant": true, "inputs": [], "name": "get_constants", "outputs": [{"internalType": "uint256", "name": "js_in", "type": "uint256"}, {"internalType": "uint256", "name": "js_out", "type": "uint256"}, {"internalType": "uint256", "name": "num_inputs", "type": "uint256"}], "payable": false, "stateMutability": "pure", "type": "function"}, {"constant": false, "inputs": [{"internalType": "bytes32", "name": "commitment", "type": "bytes32"}], "name": "insert", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "mid", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"internalType": "uint256[2]", "name": "a", "type": "uint256[2]"}, {"internalType": "uint256[4]", "name": "b", "type": "uint256[4]"}, {"internalType": "uint256[2]", "name": "c", "type": "uint256[2]"}, {"internalType": "uint256[4]", "name": "vk", "type": "uint256[4]"}, {"internalType": "uint256", "name": "sigma", "type": "uint256"}, {"internalType": "uint256[10]", "name": "input", "type": "uint256[10]"}, {"internalType": "bytes[2]", "name": "ciphertexts", "type": "bytes[2]"}], "name": "mix", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function"}, {"constant": false, "inputs": [{"internalType": "address", "name": "", "type": "address"}, {"internalType": "address", "name": "", "type": "address"}, {"internalType": "uint256", "name": "", "type": "uint256"}, {"internalType": "bytes", "name": "", "type": "bytes"}], "name": "onBAC001Received", "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "token", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}]'''
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
    def assemble_hsig(self, primary_inputs):
        func_name = 'assemble_hsig'
        args = [primary_inputs]
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def assemble_nullifier(self, index, primary_inputs):
        func_name = 'assemble_nullifier'
        args = [index, primary_inputs]
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def assemble_public_values(self, primary_inputs):
        func_name = 'assemble_public_values'
        args = [primary_inputs]
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def get_constants(self):
        func_name = 'get_constants'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def insert(self, commitment):
        func_name = 'insert'
        args = [commitment]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def mid(self):
        func_name = 'mid'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result

    # ------------------------------------------
    def mix(self, a, b, c, vk, sigma, input, ciphertexts):
        func_name = 'mix'
        args = [a, b, c, vk, sigma, input, ciphertexts]
        receipt = self.client.sendRawTransactionGetReceipt(self.address, self.contract_abi, func_name, args)
        outputresult = self.data_parser.parse_receipt_output(func_name, receipt['output'])
        return outputresult, receipt

    # ------------------------------------------
    def token(self):
        func_name = 'token'
        args = []
        result = self.client.call(self.address, self.contract_abi, func_name, args)
        return result
