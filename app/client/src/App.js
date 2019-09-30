import React from 'react';
import axios from 'axios';
import './App.css';

class App extends React.Component {
  constructor(props){
    super(props);
    this.getData = this.getData.bind(this);
    this.state = {
      exhibition: {
        title: '',
        artists: [],
      },
    };
  }

  componentDidMount(){
    this.getData()
  }

  getData() {
    axios.get('http://127.0.0.1:8000/curator/exhibition/23/')
    .then((res) => {
      this.setState(state => {
        return {
          exhibition: res.data,
        };
      })
    })
    .catch((error) => {
      console.error(error);
    })
  }

  render() {
    const {title, artists} = this.state.exhibition;
    return (
      <div className="App">
        <div className="App-header">{title}</div>
        <div className="App-artists">
          <ul>
            {artists.map(a => {
              return (
                <li key={a.token} className="artist">{a.display_name}</li>
              );
            })}
          </ul>
        </div>
      </div>
    );
  };
}

export default App;
