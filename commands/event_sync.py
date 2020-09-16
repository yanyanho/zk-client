import os
import sys
import time
from typing import List

from commands.constants import USER_DIR, WALLET_DIR_DEFAULT
from commands.mysql_pool import MysqlPool
from commands.utils import load_zeth_address
from python_web3.client.bcosclient import BcosClient
from python_web3.client.datatype_parser import DatatypeParser
from python_web3.client.event_callback import BcosEventCallback
from python_web3.client.event_callback import EventCallbackHandler
from zeth.contracts import _event_args_to_mix_result
from zeth.wallet import Wallet
from zeth.merkle_tree import sqlMerkleTree
from zeth.constants import ZETH_MERKLE_TREE_DEPTH
import math

class LogMixEvent(object):
    def __init__(
            self,
            mid: int,
            root: bytes,
            nullifiers: bytes(2),
            commitments: bytes(2),
            ciphertexts: bytes(2)):
        self.mid = mid
        self.root = root
        self.nullifiers = nullifiers
        self.commitments = commitments
        self.ciphertexts = ciphertexts

def make_wallet(mid: int, next_addr: int) -> List[Wallet]:
    '''
    Return all the wallet in local server
    '''
    wallet_list = []
    for username in os.listdir(USER_DIR):
        wallet_dir = "{}/{}/{}".format(USER_DIR, username, WALLET_DIR_DEFAULT)
        zeth_address = load_zeth_address(username)
        wallet_list.append(Wallet(None, username, wallet_dir, zeth_address.addr_sk, mid, next_addr))
    return wallet_list

class EventCallbackImpl(EventCallbackHandler):
    """sample event push handler for application level,
    user can make a class base on "ChannelPushHandler" ,implement the on_push interface
    handle the message from nodes,message in ChannelPack type #see client/channelpack.py
    EVENT_LOG_PUSH type is 0x1002
    message in pack.data decode by utf-8
    EVENT_LOG  format see https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/docs/sdk/java_sdk.html#id19
    """
    abiparser: DatatypeParser = None

    def on_event(self, eventdata):
        logresult = self.abiparser.parse_event_logs(eventdata["logs"])
        print("--------------------EventCallbackImpl--------------------\n")
        blockNumber = eventdata["logs"][0]['blockNumber']
        print("the blockNumber in log is :", blockNumber)
        logMix = logresult[0]['eventdata']
        logMixEvent = LogMixEvent(logMix[0],logMix[1], logMix[2], logMix[3], logMix[4])
        mix_result = _event_args_to_mix_result(logMixEvent)
        mid = mix_result.mid
        # load merkletree from database
        merkle_tree = sqlMerkleTree.open(int(math.pow(2, ZETH_MERKLE_TREE_DEPTH)), mid)
        #print("init root: ", merkle_tree.get_root())
        # check merkel root whether is new or not
        new_merkle_root = mix_result.new_merkle_root
        print("new_merkle_roots in log: ", new_merkle_root)
        if new_merkle_root == merkle_tree.get_root():
            return

        # get the next_address of updated tree
        next_addr = merkle_tree.get_num_entries()

        # update each merkletree
        for out_ev in mix_result.output_events:
            print("commitment: ", out_ev.commitment)
            merkle_tree.insert(out_ev.commitment)
        merkle_tree.recompute_root()
        merkle_tree.save(blockNumber,mid)
        print(f"The update_merkle_root of {mid} is {merkle_tree.get_root()}")

        # update each user's wallet
        for wallet in make_wallet(mid, next_addr):
            # received_notes
            wallet.receive_notes(mix_result.output_events)
            spent_commits = wallet.mark_nullifiers_used(mix_result.nullifiers)
            for commit in spent_commits:
                print(f"{wallet.username} spent commits:  {commit}")
            wallet.update_and_save_state()


def event_sync():

    indexed_value = None
    try:
        tag = True
        print("check whether existed mixer contract")
        sqlSearchMixer = "select * from contract where conType = %s"
        MIXERTYPE = "mixer"
        mixer_addr = ""
        mysql_pool = MysqlPool()
        db = mysql_pool.steady_connection()
        cursor = db.cursor()
        while tag:
            # db.ping(reconnect=True)
            cursor.execute(sqlSearchMixer, [MIXERTYPE])
            resultMixer = cursor.fetchall()
            db.commit()
            if resultMixer:
                tag = False
                mixer_addr = resultMixer[0]['conAddr']
                print("found mixer contract: ", mixer_addr)
            else:
                print("could not find mixer contract, waiting...")
                time.sleep(10)
        bcos_event = BcosEventCallback()
        bcos_event.setclient(BcosClient())
        print(bcos_event.client.getinfo())
        '''
        print("usage input {},{},{},{}".format(contractname, address, event_name, indexed_value))
        if address == "last":
            cn = ContractNote()
            address = cn.get_last(contractname)
            print("hex address :", address)
            '''
        abifile = "contract/mixer/abi/Groth16Mixer.abi"
        abiparser = DatatypeParser(abifile)
        eventcallback = EventCallbackImpl()
        eventcallback.abiparser = abiparser
        blockNumber = 0
        # maybe change to use cursor.lastrowid to get the last row
        sqlSearch = "select * from merkletree"
        cursor.execute(sqlSearch)
        results = cursor.fetchall()
        if results:
            blockNumber = results[-1]['blockNumber']
        print("blockNumber: ", blockNumber)
        result = bcos_event.register_eventlog_filter(
            eventcallback, abiparser, [mixer_addr], "LogMix", indexed_value, str(blockNumber+1))
        #result = bcos_event.register_eventlog_filter(eventcallback02,abiparser, [address], "on_number")

        print(
            "after register LogMix,result:{},all:{}".format(
                result['result'], result))
        print("waiting event...")
        while True:
            # print("waiting event...")
            time.sleep(10)
    except Exception as e:
        print("Exception!")
        import traceback
        traceback.print_exc()
    finally:
        print("event callback finished!")
        if bcos_event.client is not None:
            bcos_event.client.finish()
    sys.exit(-1)


if __name__ == "__main__":
    event_sync()
