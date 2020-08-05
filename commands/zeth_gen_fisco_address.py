# Copyright (c) 2015-2020 Clearmatics Technologies Ltd
#
# SPDX-License-Identifier: LGPL-3.0+

from zeth.zeth_address import generate_zeth_address
from typing import Optional
from commands.utils import get_zeth_address_file, pub_address_file, \
    write_zeth_address_secret, write_zeth_address_public
from commands.constants import USER_DIR, FISCO_ADDRESS_FILE, WALLET_DIR_DEFAULT
from click import command, ClickException, option
from os.path import exists
from python_web3.eth_account.account import Account
from zeth.wallet import _ensure_dir
import json




def gen_fisco_address(username: str, password: str) :
    """
    Generate a new fisco account
    """
    keystore_file = "{}/{}/{}".format(USER_DIR, username, FISCO_ADDRESS_FILE)
    account = Account.create(password)
    user_dir = "{}/{}/{}".format(USER_DIR, username, WALLET_DIR_DEFAULT)
    _ensure_dir(user_dir)
    keytext = Account.encrypt(account.privateKey, password)
    with open(keystore_file, "w") as dump_f:
        json.dump(keytext, dump_f)
    print(f"{username}'s address: {account.address}")
    print(f"{username}'s publickey: {account.publickey}")
    print(f"fisco account keypair written to {keystore_file}")
    return account.address, account.publickey, account.privateKey


if __name__ == '__main__':
    gen_fisco_address()