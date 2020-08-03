from commands.zeth_gen_fisco_address import gen_fisco_address
from commands.zeth_gen_address import gen_address
from commands.event_sync import event_sync
from commands.zeth_deposit import deposit
from commands.zeth_token_approve import token_approve
from commands.zeth_token_deploy import deploy_token
from commands.zeth_deploy import deploy
from commands.zeth_mix import mix
from commands.zeth_ls_commits import ls_commits
from commands.zeth_ls_notes import ls_notes
from commands.zeth_deploy import deploy
from commands.utils import load_zeth_address, load_zeth_address_secret, open_wallet
from zeth.utils import EtherValue
from python_web3.eth_account.account import Account
from commands.constants import USER_DIR, FISCO_ADDRESS_FILE, WALLET_DIR_DEFAULT, ADDRESS_FILE_DEFAULT
from django.shortcuts import render
import json
import time
from django.http import JsonResponse
from os.path import exists
from . import models

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
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	if exists(keystore_file):
		result['status'] = 1
		result['text'] = 'keystore existed'
		return JsonResponse(result)
	(address, publickey) = gen_fisco_address(req['username'], req['password'])
	result['status'] = 0
	result['address'] = address
	pubkey = ''.join(['%02X' % b for b in publickey])
	result['publickey'] = "0x" + pubkey.lower()
	return JsonResponse(result)

'''
make wallet by import the Fisco account that the user want to use with privatekey, username and password
'''
def importFiscoAddr(request) -> None:
	result = {}
	req = json.loads(request.body)
	account = Account.privateKeyToAccount(req['privatekey'])
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	if exists(keystore_file):
		result['status'] = 1
		result['text'] = 'keystore existed'
		return JsonResponse(result)
	user_dir = "{}/{}/{}".format(USER_DIR, req['username'], WALLET_DIR_DEFAULT)
	_ensure_dir(user_dir)
	keytext = Account.encrypt(account.privateKey, req['password'])
	with open(keystore_file, "w") as dump_f:
		json.dump(keytext, dump_f)
	print(f"{req['username']}'s address: {account.address}")
	print(f"{req['username']}'s publickey: {account.publickey}")
	print(f"fisco account keypair written to {keystore_file}")
	result['status'] = 0
	result['address'] = account.address
	pubkey = ''.join(['%02X' % b for b in account.publickey])
	result['publickey'] = "0x" + pubkey.lower()
	return JsonResponse(result)
    

'''
generate a new zbac account for user with username, return the zbac address used for recieving notes
'''
def genZbacAddr(request) -> None:
	result = {}
	req = json.loads(request.body)
	addr_file = "{}/{}/{}".format(USER_DIR, req['username'], ADDRESS_FILE_DEFAULT)
	if exists(addr_file):
		result['status'] = 1
		result['text'] = 'account existed'
		return JsonResponse(result)
	zbac_addr = gen_address(req['username'])
	result['status'] = 0
	result['address'] = str(zbac_addr)
	return JsonResponse(result)

'''
deploy bac contract, only used by admin
'''
def deployToken(request) -> None:
	result = {}
	req = json.loads(request.body)
	token_address = deploy_token(req['miner_address'], req['token_amount'])
	if token_address :
		result['status'] = 0
		result['address'] = str(token_address)
		return JsonResponse(result)
	result['status'] = 1
	result['text'] = 'deploy bac contract failed'
	return JsonResponse(result)

'''
deploy zksnark mixer contract, only used by admin
'''
def deployMixer(request) -> None:
	result = {}
	req = json.loads(request.body)
	mixer_address = deploy(req['token_address'])
	if mixer_address :
		result['status'] = 0
		result['address'] = str(mixer_address)
		return JsonResponse(result)
	result['status'] = 1
	result['text'] = 'deploy zksnark mixer contract failed'
	return JsonResponse(result)

'''
deposit bac to mixer and get two notes with specified value
'''
def depositBac(request) -> None:
	#todo: 从数据库中获取前一个交易是否已经完成，也就是merkletree是否已经更新
	#即is_new是否为True，如果不是则等待，如果是则置为False，开始执行交易
	while (models.merkletree.objects.all().count() and not models.merkletree.objects.all().last().is_new):
		time.sleep(1)
	sqlResult = models.merkletree.objects.all().last()
	if models.merkletree.objects.all().count():
		sqlResult.is_new = False
		sqlResult.save()
	result = {}
	req = json.loads(request.body)
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	addr_file = "{}/{}/{}".format(USER_DIR, req['username'], ADDRESS_FILE_DEFAULT)
	if exists(keystore_file) and exists(addr_file) :
		outputapprove = token_approve(req['token_amount'], req['mixer_address'], req['token_address'], req['username'], req['password'])
		if outputapprove :
			zeth_address = load_zeth_address(req['username'])
			output_specs = []
			print(str(zeth_address.addr_pk) + ',' + str(req['value1']))
			output_specs.append(str(zeth_address.addr_pk) + ',' + str(req['value1']))
			output_specs.append(str(zeth_address.addr_pk) + ',' + str(req['value2']))
			outputdeposit = deposit(req['mixer_address'], req['username'], req['password'], req['token_amount'], output_specs)
			if outputdeposit :
				event_sync(req['mixer_address'])
				js_secret = load_zeth_address_secret(req['username'])
				wallet = open_wallet(None, js_secret, req['username'])
				total = EtherValue(0)
				commits = []
				for addr, short_commit, value in wallet.note_summaries():
					total = total + value
					commits.append(short_commit)
				result['status'] = 0
				result['commits'] = commits
				result['total_value'] = total.ether()
				return JsonResponse(result)
			else:
				result['status'] = 1
				result['text'] = 'deposit failed'
				return JsonResponse(result)
		else:
			result['status'] = 1
			result['text'] = 'token approve failed'
			return JsonResponse(result)

	result['status'] = 1
	result['text'] = 'your account is not recorded in server, please import it firstly or create a new one'
	return JsonResponse(result)