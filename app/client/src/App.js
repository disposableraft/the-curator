import React from 'react';
import axios from 'axios';
import vis from 'vis';
import './App.css';
import Exhibition from './Exhibition.js';

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <Exhibition />
      </div>
    );
  };
}

export default App;
