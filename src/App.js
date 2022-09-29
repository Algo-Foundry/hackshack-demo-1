import './App.css';
import { useState } from 'react';
import algosdk from 'algosdk';

function App() {
  const [response, setResponse] = useState("");

  const createTxn = async () => {
    console.log("create txn....");

    const token = process.env.REACT_APP_ALGOD_TOKEN;
    const server = process.env.REACT_APP_ALGOD_ADDRESS;
    const port = process.env.REACT_APP_ALGOD_PORT;
    const client = new algosdk.Algodv2(token, server, port);

    try {
      let creatorAccount = algosdk.mnemonicToSecretKey(process.env.REACT_APP_CREATOR_MNEMONIC);
      let sender = creatorAccount.addr;
      let params = await client.getTransactionParams().do();
      let index = process.env.REACT_APP_INDEX_APP_ID
      let newOwner = process.env.REACT_APP_OWNER

      // create unsigned transaction
      const appArgs = [new Uint8Array(Buffer.from("updateOwner"))];
      let txn = algosdk.makeApplicationNoOpTxn(sender, params, Number(index), appArgs, [newOwner])
      let txId = txn.txID().toString();

      // sign, send, await
      // Sign the transaction
      let signedTxn = txn.signTxn(creatorAccount.sk);
      console.log("Signed transaction with txID: %s", txId);

      // Submit the transaction
      await client.sendRawTransaction(signedTxn).do();

      // Wait for transaction to be confirmed
      let confirmedTxn = await algosdk.waitForConfirmation(client, txId, 4);
      setResponse("Transaction " + txId + " confirmed in round " + confirmedTxn["confirmed-round"]);
    } catch (error) {
      console.log(error);
      setResponse(error.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <button className="btn" onClick={createTxn}>
          Create txn
        </button>

        <p>
          { response }
        </p>
      </header>
    </div>
  );
}

export default App;
