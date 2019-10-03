import React from 'react';
import { BrowserRouter as Router, Link, Route, Switch } from 'react-router-dom';
import './App.css';
import Exhibition from './Exhibition.js';

class App extends React.Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Switch>
            <Route path="/exhibition/:id" component={Exhibition} />
            <Route path="/exhibition">
              <h3>Please select an exhibition ID.</h3>
            </Route>
            <Route path="/">
              <div>
                <Link to="/exhibition">Exhibitions</Link>
              </div>
            </Route>
          </Switch>
        </div>
      </Router>
    );
  };
}

export default App;
