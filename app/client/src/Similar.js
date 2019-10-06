import React from 'react';
import axios from 'axios';
import vis from 'vis';
import './App.css';

class Similar extends React.Component {
  constructor(props) {
    super(props);
    this.myRef = React.createRef();
    this.state = {
      similar: {
        original_token: '',
        artists: [],
      },
    };
  }

  componentDidMount() {
    const token = this.props.match.params.token;
    this.getData(token).then(success => {
      if (success) {
        this.drawGraph();
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

  drawGraph() {
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

    const data = {
      nodes: new vis.DataSet(nodes),
      edges: new vis.DataSet(edges)
    };

    const options = {
      nodes: {
        shape: 'text',
      }
    };

    return new vis.Network(this.myRef.current, data, options);
  }

  render() {
    const { original_token } = this.state.similar;

    return (
      <div className="Similar">
        <div className="Similar-header">{original_token}</div>
        <div className="Similar-graph" ref={this.myRef} />
      </div>
    );
  };
}

export default Similar;
