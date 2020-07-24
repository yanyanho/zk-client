# Copyright (c) 2015-2020 Clearmatics Technologies Ltd
#
# SPDX-License-Identifier: LGPL-3.0+

from commands.utils import \
    create_zeth_client_and_mixer_desc, load_zeth_address, open_wallet
from zeth.utils import short_commitment
from click import Context, command, pass_context, option


@command()
@option("--mixer-addr", help="The Groth16Mixer contract address you want to use")
@option("--password", help="the password of you keystore")
@pass_context
def ls_commits(ctx: Context, mixer_addr:str, password: str) -> None:
    """
    List all commitments in the joinsplit contract
    """
    client_ctx = ctx.obj
    zeth_client = create_zeth_client_and_mixer_desc(client_ctx, mixer_addr, password)
    zeth_address = load_zeth_address(client_ctx)
    wallet = open_wallet(
        zeth_client.mixer_instance, zeth_address.addr_sk, client_ctx)
    print("COMMITMENTS:")
    for commit in wallet.merkle_tree.get_leaves():
        print(f"  {short_commitment(commit)}")
