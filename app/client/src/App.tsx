import React from 'react';
import './App.css';

class App extends React.Component<any, any> {
  constructor(props: any) {
    super(props);
    this.state = {
      subject: 'Foonori Barokoo',
      images: [
        'https://www.moma.org/media/W1siZiIsIjkyODUiXSxbInAiLCJjb252ZXJ0IiwiLXJlc2l6ZSA1MTJ4NTEyXHUwMDNlIl1d.jpg?sha=bcbbfb73f150d6e2',
        'https://www.moma.org/media/W1siZiIsIjkyOTAiXSxbInAiLCJjb252ZXJ0IiwiLXJlc2l6ZSA1MTJ4NTEyXHUwMDNlIl1d.jpg?sha=a6282babc21b9ca9',
        'https://www.moma.org/media/W1siZiIsIjkzMDEiXSxbInAiLCJjb252ZXJ0IiwiLXJlc2l6ZSA1MTJ4NTEyXHUwMDNlIl1d.jpg?sha=233e53a69ab4f422',
      ]
    };

  }
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h3>{this.state.subject}</h3>
        </header>
        <div className="Images">
          <img className="picture__img--static" src={this.state.images[0]} />
          <img className="picture__img--static" src={this.state.images[1]} />
          <img className="picture__img--static" src={this.state.images[2]} />
        </div>
      </div>
    );
  }
}

export default App;
