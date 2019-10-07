import React from 'react';
import axios from 'axios';
import Graph from './Graph.js';
import './App.css';

class Similar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: {
        token: '',
        similar: [],
      },
      graph: [],
    };
  }

  componentDidMount() {
    const token = this.props.match.params.token;
    this.getData(token).then(success => {
      if (success) {
        this.setState(state => {
          state.graph = this.setupGraph();
          return state;
        });
      }
    }).catch(error => console.error(error));
  }

  getData(token) {
    return new Promise((resolve, reject) => {
      const req = axios.get(`http://127.0.0.1:8000/curator/similar/${token}`);

      req.then((res) => {
        this.setState(state => {
          return {
            data: res.data,
          };
        });
        resolve(true);
      });

      req.catch((error) => {
        console.error(error);
        reject(error);
      });
    });
  }

  setupGraph() {
    const { similar, token } = this.state.data;
    const nodes = similar.map(a => {
      return {
        id: a.token,
        label: a.display_name
      };
    });

    // Define edges between the exhibition title and the nodes.
    const edges = nodes.map(a => {
      return {
        from: a.id,
        to: 'originalToken',
      }
    });

    nodes.push(
      {
        id: 'originalToken',
        label: token,
        shape: 'circle',
      }
    );

    const options = {
      nodes: {
        shape: 'text',
      }
    };

    return { nodes, edges, options };
  }

  render() {
    const { token } = this.state.data;
    const { nodes, edges, options } = this.state.graph;

    return (
      <div className="Similar">
        <div className="Similar-header">{token}</div>
        <Graph
          nodes={nodes}
          edges={edges}
          options={options}
        />
      </div>
    );
  };
}

export default Similar;
