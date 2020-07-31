from commands.zeth_gen_fisco_address import gen_fisco_address
from commands.zeth_gen_address import gen_address
from commands.event_sync import event_sync
from commands.zeth_deposit import deposit
from commands.zeth_token_approve import token_approve
from commands.zeth_mix import mix
from commands.zeth_ls_commits import ls_commits
from commands.zeth_ls_notes import ls_notes
from commands.zeth_deploy import deploy
from python_web3.eth_account.account import Account
from commands.constants import USER_DIR, FISCO_ADDRESS_FILE, WALLET_DIR_DEFAULT
from django.shortcuts import render
import json
from django.http import JsonResponse

'''
The wallet of user is designed as that every wallet need to be specified a username and store the 
reference accounts and assets data of that user. There two kinds of account in the wallet of a user,
including Fisco account (saved as keystore) and zbac account (saved as publickey file and privatekey file).
Note that different wallet must have different zbac account but any of them are allowed to have same Fisco
account.
'''

'''
make wallet by generate a new Fisco account for user with username and password
'''
def genFiscoAddr(request) -> None:
	result = {}
	req = json.loads(request.body)
	(address, publickey) = gen_fisco_address(req['username'], req['password'])
	result['address'] = address
	result['publickey'] = publickey
	JsonResponse(result)

'''
make wallet by import the Fisco account that the user want to use with privatekey, username and password
'''
def importFiscoAddr(request) -> None:
	result = {}
	req = json.loads(request.body)
	account = Account.privateKeyToAccount(req['privatekey'])
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	if exists(keystore_file):
		raise ClickException(f"ZethAddress file {keystore_file} exists")
	user_dir = "{}/{}/{}".format(USER_DIR, req['username'], WALLET_DIR_DEFAULT)
	_ensure_dir(user_dir)
	keytext = Account.encrypt(account.privateKey, req['password'])
	with open(keystore_file, "w") as dump_f:
		json.dump(keytext, dump_f)
	print(f"{req['username']}'s address: {account.address}")
	print(f"{req['username']}'s publickey: {account.publickey}")
	print(f"fisco account keypair written to {keystore_file}")
	result['address'] = account.address
	result['publickey'] = account.publickey
	JsonResponse(result)
    

'''
generate a new zbac account for user with username, return the zbac address used for recieving notes
'''
def genZbacAddr(request) -> None:
	result = {}
	req = json.loads(request.body)
	zbac_addr = gen_address(req['username'])
	result['address'] = zbac_addr
	JsonResponse(result)