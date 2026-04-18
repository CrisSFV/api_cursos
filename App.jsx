import React, { useState } from 'react';
import './App.css';

function App() {
  const [devMessage, setDevMessage] = useState('');
  const [prodMessage, setProdMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const API_BASE_URL = "https://or9112xy9d.execute-api.us-east-1.amazonaws.com";

  const fetchDev = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/dev`);
      const data = await response.json();
      setDevMessage(data.body || JSON.stringify(data));
    } catch (error) {
      setDevMessage(`Error: ${error.message}`);
    }
    setLoading(false);
  };

  const fetchProd = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/prod`);
      const data = await response.json();
      setProdMessage(data.body || JSON.stringify(data));
    } catch (error) {
      setProdMessage(`Error: ${error.message}`);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <div className="container">
        <h1>API Gateway + React</h1>
        
        <div className="button-group">
          <button 
            className="btn btn-dev" 
            onClick={fetchDev}
            disabled={loading}
          >
            🔵 Dev: {devMessage ? 'Hola dev' : 'Click aquí'}
          </button>
          
          <button 
            className="btn btn-prod" 
            onClick={fetchProd}
            disabled={loading}
          >
            🟢 Prod: {prodMessage ? 'Hola prod' : 'Click aquí'}
          </button>
        </div>

        <div className="results">
          {devMessage && (
            <div className="result dev-result">
              <strong>DEV Response:</strong>
              <pre>{devMessage}</pre>
            </div>
          )}
          
          {prodMessage && (
            <div className="result prod-result">
              <strong>PROD Response:</strong>
              <pre>{prodMessage}</pre>
            </div>
          )}
        </div>

        {loading && <p className="loading">Loading...</p>}
      </div>
    </div>
  );
}

export default App;
