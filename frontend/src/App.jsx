import React from 'react'; 
import './App.css';       // Import do CSS principal
import ChatWindow from './components/ChatWindow';

function App() {
  return (
    <div className="App">
      <h1>Chatbot Verzel SDR</h1>
      <ChatWindow />
    </div>
  );
}

export default App;