# Copyright (c) 2015-2020 Clearmatics Technologies Ltd
#
# SPDX-License-Identifier: LGPL-3.0+

from zeth.zeth_address import generate_zeth_address
from typing import Optional
from commands.utils import get_zeth_address_file, pub_address_file, \
    write_zeth_address_secret, write_zeth_address_public
from commands.constants import USER_DIR, FISCO_ADDRESS_FILE
from click import command, ClickException, option
from os.path import exists
from python_web3.eth_account.account import Account
from zeth.wallet import _ensure_dir
import json



@command()
@option("--username", prompt='Your name', help="specify a username for you")
@option("--password", prompt='Your password', help="specify a password for you")
#@pass_context
def gen_fisco_address(username: str, password: str) -> None:
    """
    Generate a new fisco account
    """
    account = Account.create(password)
    keystore_file = "{}/{}/{}".format(USER_DIR, username, FISCO_ADDRESS_FILE)
    if exists(keystore_file):
        raise ClickException(f"ZethAddress file {keystore_file} exists")
    user_dir = "{}/{}".format(USER_DIR, username)
    _ensure_dir(user_dir)
    keytext = Account.encrypt(account.privateKey, password)
    with open(keystore_file, "w") as dump_f:
        json.dump(keytext, dump_f)
    print(f"{username}'s address: {account.address}")
    print(f"{username}'s publickey: {account.publickey}")
    print(f"fisco account keypair written to {keystore_file}")
if __name__ == '__main__':
    gen_fisco_address()