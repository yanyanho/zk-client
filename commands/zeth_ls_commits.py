# Copyright (c) 2015-2020 Clearmatics Technologies Ltd
#
# SPDX-License-Identifier: LGPL-3.0+

from commands.utils import \
    create_zeth_client_and_mixer_desc, load_zeth_address, open_wallet
from zeth.utils import short_commitment
from click import Context, command, pass_context, option
from commands.constants import PROVER_SERVER_ENDPOINT_DEFAULT

@command()
#@option("--mixer-addr", help="The Groth16Mixer contract address you want to use")
@option("--username", help="The account you want to use")
@option("--password", help="the password of you keystore")
def ls_commits(username: str, password: str) -> None:
    """
    List all commitments in the joinsplit contract
    """
    #zeth_client = create_zeth_client_and_mixer_desc(PROVER_SERVER_ENDPOINT_DEFAULT, mixer_addr, username, password)
    zeth_address = load_zeth_address(username)
    wallet = open_wallet(
        None, zeth_address.addr_sk, username)
    print("COMMITMENTS:")
    for commit in wallet.merkle_tree.get_leaves():
        print(f"  {short_commitment(commit)}")

if __name__ == '__main__':
    ls_commits()
