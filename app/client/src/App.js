import React from 'react';
import axios from 'axios';
import vis from 'vis';
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.myRef = React.createRef();
    this.state = {
      exhibition: {
        title: '',
        artists: [],
      },
    };
  }

  componentDidMount() {
    this.getData().then(success => {
      if (success) {
        this.drawGraph();
      }
    }).catch(error => console.error(error));
  }

  getData() {
    return new Promise((resolve, reject) => {
      const req = axios.get('http://127.0.0.1:8000/curator/exhibition/23/');

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

  drawGraph() {
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
        label: title
      }
    );

    const data = {
      nodes: new vis.DataSet(nodes),
      edges: new vis.DataSet(edges)
    };
    const options = {};
    return new vis.Network(this.myRef.current, data, options);
  }

  render() {
    const { title, artists } = this.state.exhibition;

    return (
      <div className="App">
        <div className="App-header">{title}</div>
        <div className="App-graph" ref={this.myRef} />
        <div className="App-artists">
          <ul>
            {artists.map(a => {
              return (
                <li key={a.token} className="artist">
                  {a.display_name}
                </li>
              );
            })}
          </ul>
        </div>
      </div>
    );
  };
}

export default App;
