# Copyright (c) 2015-2020 Clearmatics Technologies Ltd
#
# SPDX-License-Identifier: LGPL-3.0+

from zeth.zeth_address import generate_zeth_address
from typing import Optional
from commands.utils import get_zeth_address_file, pub_address_file, \
    write_zeth_address_secret, write_zeth_address_public
from commands.constants import USER_DIR, WALLET_DIR_DEFAULT
from click import command, pass_context, ClickException, Context, option
from os.path import exists
from zeth.wallet import _ensure_dir
ADDRESS_FILE_DEFAULT = "zeth-address.json"


def gen_address(username: str) :
    """
    Generate a new Zeth secret key and public address
    """
    #client_ctx = ctx.obj
    #addr_file_name = get_zeth_address_file(client_ctx)
    addr_file = "{}/{}/{}".format(USER_DIR, username, ADDRESS_FILE_DEFAULT)
    user_dir = "{}/{}/{}".format(USER_DIR, username, WALLET_DIR_DEFAULT)
    _ensure_dir(user_dir)
    pub_addr_file = pub_address_file(addr_file)
    if exists(pub_addr_file):
        raise ClickException(f"ZethAddress pub file {pub_addr_file} exists")

    zeth_address = generate_zeth_address()
    write_zeth_address_secret(zeth_address.addr_sk, addr_file)
    print(f"ZethAddress Secret key written to {addr_file}")
    write_zeth_address_public(zeth_address.addr_pk, pub_addr_file)
    print(f"Public ZethAddress written to {pub_addr_file}")
    return zeth_address.addr_pk
    
if __name__ == '__main__':
    gen_address()