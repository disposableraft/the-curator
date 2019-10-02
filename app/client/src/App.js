import React from 'react';
import './App.css';
import Exhibition from './Exhibition.js';

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <Exhibition id={24} />
      </div>
    );
  };
}

export default App;
