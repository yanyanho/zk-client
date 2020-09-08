import json
from os.path import exists
from typing import List, Tuple

from django.http import JsonResponse

from api.zeth_messages_pb2 import ZethNote
from commands.constants import USER_DIR, FISCO_ADDRESS_FILE, WALLET_DIR_DEFAULT, ADDRESS_FILE_DEFAULT
from commands.mysql_pool import MysqlPool
from commands.utils import load_zeth_address, load_zeth_address_secret, open_wallet, parse_output, \
	load_zeth_address_public
from commands.zeth_deploy import deploy
from commands.zeth_deposit import deposit
from commands.zeth_gen_address import gen_address
from commands.zeth_gen_fisco_address import gen_fisco_address
from commands.zeth_ls_notes import ls_notes
from commands.zeth_mix import mix
from commands.zeth_token_approve import token_approve
from commands.zeth_token_deploy import deploy_asset
from contract.BAC001 import BAC001
from python_web3.client.bcosclient import BcosClient
from python_web3.client.bcoskeypair import BcosKeyPair
from python_web3.eth_account.account import Account
from zeth.utils import EtherValue, from_zeth_units
from zeth.wallet import _ensure_dir
from zeth.zeth_address import ZethAddressPub

mysql_pool = MysqlPool()
db = mysql_pool.conn()
cursor = db.cursor()

'''
The wallet of user is designed as that every wallet need to be specified a username and store the 
reference accounts and assets data of that user. There two kinds of account in the wallet of a user,
including Fisco account (saved as keystore) and zbac account (saved as publickey file and privatekey file).
Note that different wallet must have different zbac account but any of them are allowed to have same Fisco
account.
'''
def checkUser(request) ->None:
	result = {}
	req = json.loads(request.body)
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	if exists(keystore_file):
		with open(keystore_file, "r") as dump_f:
			keytext = json.load(dump_f)
			privatekey = Account.decrypt(keytext, req['password'])
			if privatekey:
				result['status'] = 0
				prikey = ''.join(['%02X' % b for b in privatekey])
				result['privatekey'] = "0x" + prikey.lower()
				return JsonResponse(result)
			else:
				result['status'] = 1
				result['text'] = 'password not true'
				return JsonResponse(result)
	else:
		result['status'] = 1
		result['text'] = 'your account is not recorded in server, please import it firstly or create a new one'
		return JsonResponse(result)
'''
make wallet by generate a new Fisco account for user with username and password
params:
username:str 
password:str 

def genFiscoAddr(request) -> None:
	result = {}
	req = json.loads(request.body)
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	if exists(keystore_file):
		result['status'] = 1
		result['text'] = 'username existed'
		return JsonResponse(result)
	(address, publickey, privatekey) = gen_fisco_address(req['username'], req['password'])
	result['status'] = 0
	result['address'] = address
	pubkey = ''.join(['%02X' % b for b in publickey])
	result['publickey'] = "0x" + pubkey.lower()
	prikey = ''.join(['%02X' % b for b in privatekey])
	result['privatekey'] = "0x" + prikey.lower()
	return JsonResponse(result)
'''
def genAccount(request) -> None:
	result = {}
	req = json.loads(request.body)
	if req['username'] is None or req['username'] == '':
		result['status'] = 0
		result['text'] = 'username cannot be null'
		return JsonResponse(result)
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	addr_file = "{}/{}/{}".format(USER_DIR, req['username'], ADDRESS_FILE_DEFAULT)
	if exists(keystore_file) and exists(addr_file):
		with open(keystore_file, "r") as dump_f:
			keytext = json.load(dump_f)
			try:
				privatekey = Account.decrypt(keytext, req['password'])
			except ValueError:
				result['status'] = 1
				result['text'] = 'invalid password'
				return JsonResponse(result)
			account = Account.privateKeyToAccount(privatekey)
			result['fisco_address'] = account.address

		zbac_addr = load_zeth_address_public(req['username'])
		result['zbac_address'] = str(zbac_addr)
		result['status'] = 0
		result['text'] = 'account existed'
		return JsonResponse(result)
	(address, publickey, privatekey) = gen_fisco_address(req['username'], req['password'])
	zbac_addr = gen_address(req['username'])
	pubkey = ''.join(['%02X' % b for b in publickey])
	prikey = ''.join(['%02X' % b for b in privatekey])
	result['status'] = 0
	result['fisco_address'] = address
	result['publickey'] = "0x" + pubkey.lower()
	result['privatekey'] = "0x" + prikey.lower()
	result['zbac_address'] = str(zbac_addr)
	return JsonResponse(result)
'''
make wallet by import the Fisco account that the user want to use with privatekey, username and password
params:
username:str
password:str
privatekey:str
'''
def importFiscoAddr(request) -> None:
	result = {}
	req = json.loads(request.body)
	account = Account.privateKeyToAccount(req['privatekey'])
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	addr_file = "{}/{}/{}".format(USER_DIR, req['username'], ADDRESS_FILE_DEFAULT)
	if exists(keystore_file):
		with open(keystore_file, "r") as dump_f:
			keytext = json.load(dump_f)
			privatekey = Account.decrypt(keytext, req['password'])
			account = Account.privateKeyToAccount(privatekey)
			result['fisco_address'] = account.address
		zbac_addr = load_zeth_address_public(req['username'])
		result['zbac_address'] = str(zbac_addr)
		result['status'] = 0
		result['text'] = 'keystore existed'
		return JsonResponse(result)
	user_dir = "{}/{}/{}".format(USER_DIR, req['username'], WALLET_DIR_DEFAULT)
	_ensure_dir(user_dir)
	keytext = Account.encrypt(account.privateKey, req['password'])
	with open(keystore_file, "w") as dump_f:
		json.dump(keytext, dump_f)
	zbac_addr = ''
	if not exists(addr_file):
		zbac_addr = zbac_addr + str(gen_address(req['username']))
	else:
		zbac_addr = zbac_addr + str(load_zeth_address_public(req['username']))
	result['status'] = 0
	print(f"{req['username']}'s address: {account.address}")
	print(f"{req['username']}'s publickey: {account.publickey}")
	print(f"fisco account keypair written to {keystore_file}")
	result['status'] = 0
	result['fisco_address'] = account.address
	pubkey = ''.join(['%02X' % b for b in account.publickey])
	result['publickey'] = "0x" + pubkey.lower()
	result['zbac_address'] = zbac_addr
	return JsonResponse(result)
    

'''
generate a new zbac account for user with username, return the zbac address used for recieving notes
params:
username:str
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
params:
miner_address:str --help: the fisco address of initial owner
token_amount:int --help: the total amount of bac
'''
def deployToken(request) -> None:
	result = {}
	req = json.loads(request.body)
	token_address = deploy_asset(req['description'], req['shortName'],req['minUnit'],req['totalAmount'])
	if token_address :
		result['status'] = 0
		result['address'] = str(token_address)
		return JsonResponse(result)
	result['status'] = 1
	result['text'] = 'deploy bac contract failed'
	return JsonResponse(result)

'''
deploy zksnark mixer contract, only used by admin
params:
token_address:str --help: the bac contract address
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


def sendAsset(request) -> None:
	result = {}
	req = json.loads(request.body)
	asset_instance = BAC001(req['token_address'])
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	with open(keystore_file, "r") as dump_f:
		keytext = json.load(dump_f)
		privkey = Account.decrypt(keytext, req['password'])
		asset_instance.client.ecdsa_account = Account.from_key(privkey)
		keypair = BcosKeyPair()
		keypair.private_key = asset_instance.client.ecdsa_account.privateKey
		keypair.public_key = asset_instance.client.ecdsa_account.publickey
		keypair.address = asset_instance.client.ecdsa_account.address
		asset_instance.client.keypair = keypair
	print(f"- {req['username']}  the transfer of BAC001asset to the Mixer")
	value = EtherValue(req['value'])
	out, transactionReceipt = asset_instance.send(
		req['fiscoAddress'],
		value.wei,'')
	print("send tranaction output {}", out)
	balance = asset_instance.balance(keypair.address)
	result['status'] = 0
	result['balance'] = balance[0]/1000000000000000000.0
	return JsonResponse(result)

def faucet(request) -> None:
	print("apply for bac tokens")
	result = {}
	req = json.loads(request.body)
	asset_instance = BAC001(req['token_address'])
	asset_instance.client = BcosClient()
	value = EtherValue(req['value'])
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	with open(keystore_file, "r") as dump_f:
		keytext = json.load(dump_f)
		privatekey = Account.decrypt(keytext, req['password'])
		account = Account.privateKeyToAccount(privatekey)
		out, transactionReceipt = asset_instance.send(
			account.address,
			value.wei,'')
		balance = asset_instance.balance(account.address)
		print("get tokens: ", balance)
		result['status'] = 0
		result['balance'] = balance[0]/1000000000000000000.0
		return JsonResponse(result)


'''
deposit bac to mixer and get two notes with specified value
params:
username:str
password:str
token_amount:int --help the amount of bac you want to deposit
mixer_address:str --help the mixer contract address
token_address:str --help: the bac contract address
value1:int --help: value of the first output note
value2:int --help: value of the second output note
'''
def depositBac(request) -> None:
	result = {}
	req = json.loads(request.body)
	if req['token_amount'] != (req['value1'] + req['value2']):
		result['status'] = 1
		result['text'] = 'deposit token_amount is not equal to output value1 plus value2'
		return JsonResponse(result)
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	addr_file = "{}/{}/{}".format(USER_DIR, req['username'], ADDRESS_FILE_DEFAULT)
	if exists(keystore_file) and exists(addr_file) :
		'''
		while (merkletree.objects.all().count() and not merkletree.objects.all().last().is_new):
			time.sleep(1)
			print("sleep")
		sqlResult = merkletree.objects.all().last()
		blockNumber = 1;
		if sqlResult:
			sqlResult.is_new = False
			sqlResult.save()
			blockNumber = sqlResult.blockNumber
		'''
		outputapprove = token_approve(req['token_amount'], req['mixer_address'], req['token_address'], req['username'], req['password'])
		if outputapprove :
			zeth_address = load_zeth_address(req['username'])
			output_specs = []
			print(str(zeth_address.addr_pk) + ',' + str(req['value1']))
			output_specs.append(str(zeth_address.addr_pk) + ',' + str(req['value1']))
			output_specs.append(str(zeth_address.addr_pk) + ',' + str(req['value2']))

			outputdeposit = deposit(req['mixer_address'], req['username'], req['password'], req['token_amount'], output_specs)
			# todo
			if outputdeposit :
				'''
				event_sync(req['mixer_address'], blockNumber)
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
				'''
				traType = "deposit"
				output_specstr = output_specs[0] + ';' + output_specs[1]
				sqlInsert = "insert into transactions (traType, username, vin, vout, output_specs) values (%s, %s, %s, %s, %s);"
				db.ping(reconnect=True)
				cursor.execute(sqlInsert, [traType, req['username'], req['token_amount'], 0, output_specstr])
				db.commit()
				result['status'] = 0
				result['text'] = 'deposit success'
				return JsonResponse(result)
			else:
				'''
				if models.merkletree.objects.all().count():
					sqlResult.is_new = True
					sqlResult.save()
				'''
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

'''
params:
username:str
password:str
token_address:str --help: the bac contract address
mixer_address:str --help the mixer contract address
vin:int --help public input, amount of bac you want to deposit firstly
vout:int --help amount of bac you want to withdraw
input_notes:List[str(noteid)] --help the notes you want to spent
output_specs:List[str(zeth_address,value)] --help the reciever and value
'''
def mixBac(request) -> None:
	result = {}
	req = json.loads(request.body)
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	addr_file = "{}/{}/{}".format(USER_DIR, req['username'], ADDRESS_FILE_DEFAULT)
	if exists(keystore_file) and exists(addr_file):
		js_secret = load_zeth_address_secret(req['username'])
		wallet = open_wallet(None, js_secret, req['username'], None, None)
		inputs: List[Tuple[int, ZethNote]] = [
			wallet.find_note(note_id).as_input() for note_id in req['input_notes']]
		outputs: List[Tuple[ZethAddressPub, EtherValue]] = [
			parse_output(out_spec) for out_spec in req['output_specs']]
		mids = []
		for note_id in req['input_notes']:
			mids.append(wallet.find_note(note_id).mid)
		'''
		todo: check the reciever zeth_address whether record in server, if not, return /
		by searching the address in mysql, so for every zeth account, we need to save their zeth_address in mysql when generating /
		or specify the reciever by name instead zeth_address, so we can search the user dir
		'''
		input_note_sum = from_zeth_units(
			sum([int(note.value, 16) for _, note in inputs]))
		output_note_sum = sum([value for _, value in outputs], EtherValue(0))
		vin_pub = EtherValue(req['vin']  )
		vout_pub = EtherValue(req['vout'])
		if vin_pub + input_note_sum != vout_pub + output_note_sum:
			result['status'] = 1
			result['text'] = 'input and output value mismatch'
			return JsonResponse(result)
		'''
		while (merkletree.objects.all().count() and not merkletree.objects.all().last().is_new):
			time.sleep(1)
		sqlResult = merkletree.objects.all().last()
		if sqlResult:
			sqlResult.is_new = False
			sqlResult.save()
		'''
		if req['vin']:
			outputapprove = token_approve(req['vin'], req['mixer_address'], req['token_address'], req['username'], req['password'])
			if not outputapprove:
				result['status'] = 1
				result['text'] = 'token approve failed'
				return JsonResponse(result)
		outputmix = mix(req['mixer_address'], req['username'], req['password'], vin_pub, vout_pub, inputs, outputs, mids)
		if outputmix:
			'''
			event_sync(req['mixer_address'],sqlResult.blockNumber)
			total = EtherValue(0)
			commits = []
			for addr, short_commit, value in wallet.note_summaries():
				total = total + value
				commits.append(short_commit)
			result['status'] = 0
			result['commits'] = commits
			result['total_value'] = total.ether()
			'''
			traType = "mix"
			inputstr = ""
			for note_id in req['input_notes']:
				inputstr = inputstr + note_id + ';'
			outputstr = ""
			for out_spec in req['output_specs']:
				outputstr = outputstr + out_spec + ';'
			sqlInsert = "insert into transactions (traType, username, vin, vout, input_notes, output_specs) values (%s, %s, %s, %s, %s, %s);"
			db.ping(reconnect=True)
			cursor.execute(sqlInsert, [traType, req['username'], req['vin'], req['vout'], inputstr, outputstr])
			db.commit()
			result['status'] = 0
			result['text'] = 'mix success'
			return JsonResponse(result)
		else:
			'''
			if merkletree.objects.all().count():
				sqlResult.is_new = True
				sqlResult.save()
			'''
			result['status'] = 1
			result['text'] = 'mix failed'
			return JsonResponse(result)
	result['status'] = 1
	result['text'] = 'your account is not recorded in server, please import it firstly or create a new one'
	return JsonResponse(result)

'''
get the unspent and spented notes of your account
params:
username:str
password:str
'''
def getNotes(request) -> None:
	result = {}
	req = json.loads(request.body)
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	addr_file = "{}/{}/{}".format(USER_DIR, req['username'], ADDRESS_FILE_DEFAULT)
	if exists(keystore_file) and exists(addr_file):
		with open(keystore_file, "r") as dump_f:
			keytext = json.load(dump_f)
			if Account.decrypt(keytext, req['password']):
				(total, commits, values, spend_commits) = ls_notes(req['username'])
				result['status'] = 0
				result['commits'] = commits
				result['values'] = values
				result['total_value'] = total.ether()
				result['spend_commits'] = spend_commits
				return JsonResponse(result)
			else:
				result['status'] = 1
				result['text'] = 'the password is not match the account'
				return JsonResponse(result)
	result['status'] = 1
	result['text'] = 'your account is not recorded in server, please import it firstly or create a new one'
	return JsonResponse(result)

'''
get all commiments in merkletree
params:
username:str
'''
'''
def getCommits(request) -> None:
	result = {}
	#req = json.loads(request.body)
	username = request.META.get('HTTP_USERNAME', 'unknown')
	print("username: ", username)
	keystore_file = "{}/{}/{}".format(USER_DIR, username, FISCO_ADDRESS_FILE)
	addr_file = "{}/{}/{}".format(USER_DIR, username, ADDRESS_FILE_DEFAULT)
	if exists(keystore_file) and exists(addr_file):
		commits = []
		for commit in ls_commits(username):
			comm = ''.join(['%02X' % b for b in commit])
			commits.append(comm.lower())
		print("commits: ", commits)
		result['status'] = 0
		result['commits'] = commits
		return JsonResponse(result)
	result['status'] = 1
	result['text'] = 'your account is not recorded in server, please import it firstly or create a new one'
	return JsonResponse(result)
'''
def getContract(request) -> None:
	result = {}
	sqlSearch = "select * from contract"
	db.ping(reconnect=True)
	cursor.execute(sqlSearch)
	results = cursor.fetchall()
	db.commit()
	resultbac = results[0]
	resultmixer = results[1]
	bacContract = {
		"contractName": resultbac[0],
		"contractType": resultbac[1],
		"contractAddr": resultbac[2],
		"ownerAddr": resultbac[3],
		"totalAmount": resultbac[4],
		"shortName": resultbac[5],
	}
	mixerContract = {
		"contractName": resultmixer[0],
		"contractType": resultmixer[1],
		"contractAddr": resultmixer[2],
		"ownerAddr": resultmixer[3],
		"totalAmount": resultmixer[4],
		"shortName": resultmixer[5],
	}
	result['contracts'] = {
		"bacContract": bacContract,
		"mixerContract": mixerContract,
	}
	result['status'] = 0
	return JsonResponse(result)


def getTransactions(request) -> None:
	result = {}
	req = json.loads(request.body)
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	if exists(keystore_file):
		with open(keystore_file, "r") as dump_f:
			keytext = json.load(dump_f)
			privatekey = Account.decrypt(keytext, req['password'])
			if privatekey:
				sqlSearch = "select * from transactions where username = %s"
				db.ping(reconnect=True)
				cursor.execute(sqlSearch, [req['username']])
				results = cursor.fetchall()
				db.commit()
				result['transactions'] = []
				for resultTra in results:
					transacInfo = {
						"trasactionType": resultTra[0],
						"senderName": resultTra[1],
						"publicInput": resultTra[2],
						"publicOutput": resultTra[3],
						"input_notes": resultTra[4],
						"output_specs": resultTra[5],
					}
					result['transactions'].append(transacInfo)
				result['status'] = 0
				return JsonResponse(result)
			else:
				result['status'] = 1
				result['text'] = 'password not true'
				return JsonResponse(result)
	else:
		result['status'] = 1
		result['text'] = 'your account is not recorded in server, please import it firstly or create a new one'
		return JsonResponse(result)

def getBalance(request) -> None:
	result = {}
	req = json.loads(request.body)
	bac_instance = BAC001(req['token_address'])
	keystore_file = "{}/{}/{}".format(USER_DIR, req['username'], FISCO_ADDRESS_FILE)
	with open(keystore_file, "r") as dump_f:
		keytext = json.load(dump_f)
		privkey = Account.decrypt(keytext, req['password'])
		bac_instance.client.ecdsa_account = Account.from_key(privkey)
		keypair = BcosKeyPair()
		keypair.private_key = bac_instance.client.ecdsa_account.privateKey
		keypair.public_key = bac_instance.client.ecdsa_account.publickey
		keypair.address = bac_instance.client.ecdsa_account.address
		bac_instance.client.keypair = keypair
	balance = bac_instance.balance(bac_instance.client.ecdsa_account.address)
	result['status'] = 0
	result['balance'] = balance[0]/1000000000000000000.0
	return JsonResponse(result)