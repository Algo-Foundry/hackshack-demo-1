import './App.css';
import { useState } from 'react';

function App() {
  const createTxn = () => {
    console.log("create txn....");
  };
  
  const [response, setResponse] = useState("response");

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
