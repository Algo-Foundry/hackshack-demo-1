import './App.css';
import { useState } from 'react';
import algosdk from 'algosdk';

function App() {
  const [response, setResponse] = useState("response");

  const createTxn = async () => {
    console.log("create txn....");

    const token = process.env.REACT_APP_ALGOD_TOKEN;
    const server = process.env.REACT_APP_ALGOD_ADDRESS;
    const port = process.env.REACT_APP_ALGOD_PORT;
    const client = new algosdk.Algodv2(token, server, port);

    try {
      const status = await client.status().do();
      console.log(status);
      // setResponse(await client.status().do());
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
