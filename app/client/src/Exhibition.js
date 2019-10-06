import React from 'react';
import axios from 'axios';
import Graph from './Graph.js';
import './App.css';

class Exhibition extends React.Component {
  constructor(props) {
    super(props);
    this.myRef = React.createRef();
    this.state = {
      exhibition: {
        title: '',
        artists: [],
      },
      graph: [],
    };
  }

  setupGraph() {
    const { artists, title } = this.state.exhibition;
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
        to: 'exhibitionTitle',
      }
    });

    nodes.push(
      {
        id: 'exhibitionTitle',
        label: title,
        shape: 'circle',
      }
    );

    const options = {
      nodes: {
        shape: 'text',
      }
    }

    return {
      nodes: nodes,
      edges: edges,
      options: options,
    }
  }

  componentDidMount() {
    const id = this.props.match.params.id;

    this.getData(id).then(success => {
      if (success) {
        this.setState((state) => {
          state.graph = this.setupGraph();
          return state;
        });
      }
    }).catch(error => console.error(error));
  }

  getData(id) {
    return new Promise((resolve, reject) => {
      const req = axios.get(`http://127.0.0.1:8000/curator/exhibition/${id}`);

      req.then((res) => {
        this.setState(state => {
          return {
            exhibition: res.data,
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

  render() {
    const { title } = this.state.exhibition;
    const { nodes, edges, options } = this.state.graph;

    return (
      <div className="Exhibition">
        <div className="Exhibition-header">
          {title}
        </div>
        <Graph
          nodes={nodes}
          edges={edges}
          options={options}
        />
      </div>
    );
  };
}

export default Exhibition;
