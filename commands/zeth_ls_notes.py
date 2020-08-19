# Copyright (c) 2015-2020 Clearmatics Technologies Ltd
#
# SPDX-License-Identifier: LGPL-3.0+

from commands.utils import load_zeth_address_secret, open_wallet
from zeth.utils import EtherValue
from click import Context, command, option, pass_context
#from contract.Groth16Mixer import Groth16Mixer


def ls_notes(username: str):
    """
    List the set of notes owned by this wallet
    """
    #client_ctx = ctx.obj
    #web3 = open_web3_from_ctx(client_ctx)
    #mixer_desc = load_mixer_description_from_ctx(client_ctx)
    #mixer_instance = mixer_desc.mixer.instantiate(web3)
    #mixer_instance = Groth16Mixer(mixer_addr)
    js_secret = load_zeth_address_secret(username)
    wallet = open_wallet(None, js_secret, username,None, None)

    total = EtherValue(0)
    commits = []
    values = []
    for addr, short_commit, value in wallet.note_summaries():
        #print(f"{short_commit}: value={value.ether()}, addr={addr}")
        values.append(value.ether())
        total = total + value
        commits.append(short_commit)

    #print(f"TOTAL BALANCE: {total.ether()}")

    #print("SPENT NOTES:")
    spend_commits = []
    for addr, short_commit, value in wallet.spent_note_summaries():
        #print(f"{short_commit}: value={value.ether()}, addr={addr}")
        spend_commits.append(short_commit)
    return total, commits, values, spend_commits
if __name__ == '__main__':
    ls_notes()
