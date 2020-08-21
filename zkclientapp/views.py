from django.shortcuts import render
from commands.constants import DATABASE_DEFAULT_ADDRESS, DATABASE_DEFAULT_PORT, DATABASE_DEFAULT_USER, DATABASE_DEFAULT_PASSWORD, DATABASE_DEFAULT_DATABASE
from commands.zeth_token_deploy import  deploy_asset
from commands.zeth_deploy import deploy
import pymysql
import re
BACTYPE = "bac"
MIXERTYPE = "mixer"
db = pymysql.connect(
    host = DATABASE_DEFAULT_ADDRESS,
    port = DATABASE_DEFAULT_PORT,
    user = DATABASE_DEFAULT_USER,
    password = DATABASE_DEFAULT_PASSWORD,
    database = DATABASE_DEFAULT_DATABASE,
    charset='utf8'
    )
cursor = db.cursor()
# Create your views here.
ownerAddr = "0x598cf8fba4dcc36417f4c11497dee7eb23fb1431"
'''
def create_table():
    print("check whether existed tables")
    sqlSearch = "show tables"
    cursor.execute(sqlSearch)
    tables = cursor.fetchall()
    db.commit()
    tables_list = re.findall('(\'.*?\')',str(tables))
    tables_list = [re.sub("'",'',each) for each in tables_list]
    mertab = "merkletree"
    contab = "contract"
    tratab = "transactions"
    if not mertab in tables_list:
        print("create table merkletree")
        sqlCreateMer = "create table merkletree (MID int, tree_data text(40000), blockNumber int)"
        cursor.execute(sqlCreateMer)
        db.commit()
    if not contab in tables_list:
        print("create table contract")
        sqlCreateCon = "create table contract (conName char(20), conType char(20), conAddr text(500), time char(60), owner text(500), totalAmount bigint, shortName char(20))"
        cursor.execute(sqlCreateCon)
        db.commit()
    if not tratab in tables_list:
        print("create table transactions")
        sqlCreateTra = "create table transactions (traType char(20), username char(20), vin int, vout int, input_notes char(40), output_specs text(2000), time char(60))"
        cursor.execute(sqlCreateTra)
        db.commit()
'''


def deploy_contract():
    print("check whether existed bac token contract and mixer contract")
    sqlSearchBac = "select * from contract where conType = %s"
    cursor.execute(sqlSearchBac, [BACTYPE])
    resultBac = cursor.fetchall()
    db.commit()
    if resultBac:
        sqlSearchMixer = "select * from contract where conType = %s"
        cursor.execute(sqlSearchMixer, [MIXERTYPE])
        resultMixer = cursor.fetchall()
        db.commit()
        if resultMixer:
            print("all contract existed")
            return
        else:
            token_address = resultBac[0][2]
            print("deploy mixer contract on bac token contract of: ", token_address)
            mixer_address = deploy(token_address)
            if mixer_address:
                print("save mixer contract to database, address: ", mixer_address)
                sqlInsertMixer = "insert into contract (conName, conType, conAddr, owner, totalAmount, shortName) values (%s, %s, %s, %s, %s, %s);"
                conName = "Groth16Mixer"
                shortName = "mixer_test"
                cursor.execute(sqlInsertMixer, [conName, MIXERTYPE, mixer_address, ownerAddr, 0, shortName])
                db.commit()
    else:
        print("deploy bac token contract")
        shortName = "zk-AAA-demo"
        minUnit = 18
        totalAmount = 50000000000
        token_address = deploy_asset("bac token test contract", shortName, minUnit, totalAmount)
        if token_address:
            print("save bac token contract to database, address: ", token_address)
            sqlInsertBac = "insert into contract (conName, conType, conAddr, owner, totalAmount, shortName) values (%s, %s, %s, %s, %s, %s);"
            conName = "BAC001"
            cursor.execute(sqlInsertBac, [conName, BACTYPE, token_address, ownerAddr, totalAmount, shortName])
            db.commit()
            print("deploy mixer contract on bac token contract of: ", token_address)
            mixer_address = deploy(token_address)
            if mixer_address:
                print("save mixer contract to database, address: ", mixer_address)
                sqlInsertMixer = "insert into contract (conName, conType, conAddr, owner, totalAmount, shortName) values (%s, %s, %s, %s, %s, %s);"
                conNameMixer = "Groth16Mixer"
                shortNameMixer = "mixer_test"
                cursor.execute(sqlInsertMixer, [conNameMixer, MIXERTYPE, mixer_address, ownerAddr, 0, shortNameMixer])
                db.commit()

#create_table()

deploy_contract()