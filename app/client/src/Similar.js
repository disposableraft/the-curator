import React from 'react';
import axios from 'axios';
import Graph from './Graph.js';
import './App.css';

class Similar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      similar: {
        original_token: '',
        artists: [],
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
            similar: res.data,
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
    const { artists, original_token } = this.state.similar;
    const nodes = artists.map(a => {
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
        label: original_token,
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
    const { original_token } = this.state.similar;
    const { nodes, edges, options } = this.state.graph;

    return (
      <div className="Similar">
        <div className="Similar-header">{original_token}</div>
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
