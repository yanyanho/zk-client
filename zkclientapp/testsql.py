
import pymysql
import time
import re
db = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='8614',
    database='merkle',
    charset='utf8',
    )
cursor = db.cursor()
#treedata = '{"depth": 5, "default_values": ["23453ee476428c4bd601f5f74b09fabe5af02f20a121803b46e728ad02dc3c"], "layers": [["12768d51ae7923fc132b23f9d91999384720785109715b1a66b12bf4b337b101"], ["0abd670539bfe8eef99ff2ef9dc797a5195ab496d738c6d94855cd7afdd2388a"]]}'
#treedata = pymysql.escape_string(treedata)
#sqlCreate = "create table tree (id INT auto_increment PRIMARY KEY ,treedata TEXT(10000) NOT NULL)"
#sqlInsert = "insert into tree (treedata) values (%s)"
#treedata1 = '{"depth":5}'
#sqlUpdate = "update tree set treedata=%s where id=1"
id = 0
sqlSearch = "show tables"
cursor.execute(sqlSearch)
results = cursor.fetchall()
print("results: ", results)
tables_list = re.findall('(\'.*?\')',str(results))
print("tables_list: ", tables_list)
tables_list = [re.sub("'",'',each) for each in tables_list]
print("tables_list: ", tables_list)
db.commit()
sqlCreateMer = "create table mtree (MID int, tree_data text(40000), blockNumber int)"
cursor.execute(sqlCreateMer)
db.commit()
#cursor.execute(sqlSearch, [id])
#results = cursor.fetchall()[0]
#print("blocknumber: ", results[3])
cursor.close()
db.close()

'''
from python_web3.eth_account.account import Account
import json

import ast
with open("./contract/mixer/abi/Groth16Mixer.abi", "r") as abistring:
	abistr = abistring.readlines()[0]
	#abistr = json.load(abistr)
	list_list = ast.literal_eval(abistr)
	print("abistring type: ", list_list)

with open("./contract/mixer/abi/Groth16Mixer.bin", "r") as binstring:
	binstr = binstring.readlines()[0]
	print("binstr type: ", type(binstr))
	print("binstr: ", binstr)
'''
'''
keystore_file = "pyaccount.keystore"
with open(keystore_file, "r") as dump_f:
	keytext = json.load(dump_f)
	privatekey = Account.decrypt(keytext, '123456')
	prikey = ''.join(['%02X' % b for b in privatekey])
	prikey = "0x" + prikey.lower()
	print(prikey)
'''
