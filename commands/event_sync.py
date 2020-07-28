import sys
from python_web3.client.bcosclient import BcosClient
from python_web3.client.datatype_parser import DatatypeParser
from python_web3.client.contractnote import ContractNote
import json
import time
from python_web3.client.channel_push_dispatcher import ChannelPushHandler
from python_web3.client.event_callback import BcosEventCallback
from python_web3.client.event_callback import EventCallbackHandler
from click import command, argument, option, pass_context, ClickException, Context
from zeth.contracts import _event_args_to_mix_result
import os
from commands.constants import WALLET_USERNAME, FISCO_ADDRESS_FILE, USER_DIR, ADDRESS_FILE_DEFAULT, WALLET_DIR_DEFAULT
from click import command, argument, option, pass_context, ClickException, Context
from zeth.wallet import Wallet, ZethNoteDescription
from commands.utils import load_zeth_address
from typing import List
'''
def usage():
    usagetext = '\nUsage:\nparams: contractname address event_name indexed\n' \
                '\t1. contractname :\t合约的文件名,不需要带sol后缀,默认在当前目录的contracts目录下\n' \
                '\t2. address :\t十六进制的合约地址,或者可以为:last,表示采用bin/contract.ini里的记录\n' \
                '\t3. event_name :\t可选,如不设置监听所有事件 \n' \
                '\t4. indexed :\t可选,根据event定义里的indexed字段,作为过滤条件)\n\n'
    usagetext = usagetext + "\teg: for contract sample [contracts/HelloEvent.sol], use cmdline:\n\n"

    usagetext = usagetext + "\tpython demo_event_callback.py HelloEvent last \n"
    usagetext = usagetext + "\t--listen all event at all indexed ： \n\n"

    usagetext = usagetext + "\tpython demo_event_callback.py HelloEvent last on_set \n"
    usagetext = usagetext + "\t--listen event on_set(string newname) （no indexed）： \n\n"

    usagetext = usagetext + \
        "\tpython demo_event_callback.py HelloEvent last on_number 5\n"
    usagetext = usagetext + \
        "\t--listen event on_number(string name,int indexed age), age ONLY  5 ： \n"
    usagetext = usagetext + "\n...(and other events)"
    print(usagetext)
'''

class LogMixEvent(object):
    def __init__(
            self,
            root: bytes,
            nullifiers: bytes(2),
            commitments: bytes(2),
            ciphertexts: bytes(2)):
        self.root = root
        self.nullifiers = nullifiers
        self.commitments = commitments
        self.ciphertexts = ciphertexts

def make_wallet() -> List[Wallet]:
    '''
    Return all the wallet in local server
    '''
    wallet_list = []
    for username in os.listdir(USER_DIR):
        wallet_dir = "{}/{}/{}".format(USER_DIR, username, WALLET_DIR_DEFAULT)
        if os.path.exists(wallet_dir) is False:
            raise ClickException(f"invalid wallet_dir: {wallet_dir}")
        zeth_address = load_zeth_address(username)
        wallet_list.append(Wallet(None, username, wallet_dir, zeth_address.addr_sk))
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
        logMix = logresult[0]['eventdata']
        logMixEvent = LogMixEvent(logMix[0],logMix[1], logMix[2], logMix[3])
        mix_result = _event_args_to_mix_result(logMixEvent)
        new_merkle_root = mix_result.new_merkle_root
        print("new_merkle_root in log: ", new_merkle_root)
        for wallet in make_wallet():
            received_notes = wallet.receive_notes(mix_result.output_events)
            print(f"{wallet.username} received notes:  {received_notes}")
            wallet.update_and_save_state()
            update_merkle_root = wallet.merkle_tree.get_root()
            print(f"The update_merkle_root in wallet of {wallet.username} is {update_merkle_root}")


@command()
@option("--mixer-addr", help="The Groth16Mixer contract address you want to listen")
def event_sync(mixer_addr: str):

    indexed_value = None
    try:
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
        abifile = "contract/Groth16Mixer.abi"
        abiparser = DatatypeParser(abifile)
        eventcallback = EventCallbackImpl()
        eventcallback.abiparser = abiparser

        result = bcos_event.register_eventlog_filter(
            eventcallback, abiparser, [mixer_addr], "LogMix", indexed_value)
        #result = bcos_event.register_eventlog_filter(eventcallback02,abiparser, [address], "on_number")

        print(
            "after register LogMix,result:{},all:{}".format(
                result['result'], result))

        while True:
            print("waiting event...")
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
