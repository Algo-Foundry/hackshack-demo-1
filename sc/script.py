
import pprint
from base64 import b64decode
from typing import Any, Dict, List, Optional

from algosdk import account, mnemonic
from algosdk.future import transaction
from algosdk.logic import get_application_address
from algosdk.v2client.algod import AlgodClient

from smart_contract import contracts

ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ALGOD_ADDRESS = "http://localhost:4001"

MNEMONIC = "payment brisk fit helmet hold drop pink robot cargo border glare attract finish token wire asthma split satisfy two abandon gesture truth message able noble"

class PendingTxnResponse:
    def __init__(self, response: Dict[str, Any]) -> None:
        self.poolError: str = response["pool-error"]
        self.txn: Dict[str, Any] = response["txn"]

        self.applicationIndex: Optional[int] = response.get("application-index")
        self.assetIndex: Optional[int] = response.get("asset-index")
        self.closeRewards: Optional[int] = response.get("close-rewards")
        self.closingAmount: Optional[int] = response.get("closing-amount")
        self.confirmedRound: Optional[int] = response.get("confirmed-round")
        self.globalStateDelta: Optional[Any] = response.get("global-state-delta")
        self.localStateDelta: Optional[Any] = response.get("local-state-delta")
        self.receiverRewards: Optional[int] = response.get("receiver-rewards")
        self.senderRewards: Optional[int] = response.get("sender-rewards")

        self.innerTxns: List[Any] = response.get("inner-txns", [])
        self.logs: List[bytes] = [b64decode(l) for l in response.get("logs", [])]

class App:
    def __init__(self) -> None:
        self.client = AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

        self.pk = mnemonic.to_private_key(MNEMONIC)
        self.sender_addr = account.address_from_private_key(self.pk)

    def waitForTransaction(self, txID: str, timeout: int=10) -> PendingTxnResponse:
        lastStatus = self.client.status()
        lastRound = lastStatus["last-round"]
        startRound = lastRound
    
        while lastRound < startRound + timeout:
            pending_txn = self.client.pending_transaction_info(txID)
    
            if pending_txn.get("confirmed-round", 0) > 0:
                return PendingTxnResponse(pending_txn)
    
            if pending_txn["pool-error"]:
                raise Exception("Pool error: {}".format(pending_txn["pool-error"]))
    
            lastStatus = self.client.status_after_block(lastRound + 1)
    
            lastRound += 1
    
        raise Exception("Transaction {} not confirmed after {} rounds".format(txID, timeout))

    def create_app(self) -> int:
        approval, clear = contracts(self.client)

        txn = transaction.ApplicationCreateTxn(
            sender=self.sender_addr,
            on_complete=transaction.OnComplete.NoOpOC,
            approval_program=b64decode(approval["result"]),
            clear_program=b64decode(clear["result"]),
            global_schema=transaction.StateSchema(num_uints=0, num_byte_slices=1),
            local_schema=transaction.StateSchema(num_uints=0, num_byte_slices=0),
            sp=self.client.suggested_params(),
        )

        signedTxn = txn.sign(self.pk)

        self.client.send_transaction(signedTxn)
        
        response = self.waitForTransaction(signedTxn.get_txid())

        assert response.applicationIndex is not None and response.applicationIndex > 0

        return response.applicationIndex

    def main(self):
        print("Deploying SC...")

        app_id = self.create_app()

        pprint.pprint({"App ID": str(app_id), "App Address": get_application_address(app_id)})

if __name__ == "__main__":
    app = App()
    app.main()
