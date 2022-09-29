#!/usr/bin/python3

from typing import Tuple
from algosdk.v2client.algod import AlgodClient
from pyteal.ast import *
from pyteal.compiler import *
from pyteal.ir import *
from pyteal.types import *

def clear_app():
    return Int(1)

def approve_app():
    on_create = Seq( [
        App.globalPut(Bytes("owner"), Global.creator_address()),
        Return(Int(1))
    ])

    on_update = Seq(Reject())

    on_delete = Seq(Reject())

    on_optin = Seq(Approve())

    on_closeout = Seq(
            # If user has important info stored on their local state, reject close out
            Reject()
        )

    def nop():
        return Seq([Approve()])

    def updateOwner():
        return Seq(
            Assert(And(
                Txn.sender() == App.globalGet(Bytes("owner")),
                Global.group_size() == Int(1),
                Txn.rekey_to() == Global.zero_address(),
                Txn.accounts.length() == Int(1),
                Txn.accounts[1] != Global.zero_address(),
            )),

            App.globalPut(Bytes("owner"), Txn.accounts[1]),

            Approve()
        )

    METHOD = Txn.application_args[0]

    router = Cond(
        [METHOD == Bytes("nop"), nop()],
        [METHOD == Bytes("updateOwner"), updateOwner()],
    )

    return Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.UpdateApplication, on_update],
        [Txn.on_completion() == OnComplete.DeleteApplication, on_delete],
        [Txn.on_completion() == OnComplete.OptIn, on_optin],
        [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
        [Txn.on_completion() == OnComplete.NoOp, router]
    )

def compile(client: AlgodClient, contract: Expr, file_name) -> bytes:
    teal = compileTeal(contract, mode=Mode.Application, version=6, assembleConstants=True)
    with open(file_name, "w") as f:
        f.write(teal)

    response = client.compile(teal)
    return response

def contracts(client: AlgodClient) -> Tuple[bytes, bytes]:
    approval = compile(client, approve_app(), "approval.teal")
    clear = compile(client, clear_app(), "clear.teal")

    return approval, clear
