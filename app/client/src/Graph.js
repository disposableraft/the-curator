import React from 'react';
import vis from 'vis';

class Graph extends React.Component {
  constructor(props) {
    super(props);
    this.graphRef = React.createRef();
  }

  componentDidUpdate() {
    const data = {
      nodes: new vis.DataSet(this.props.nodes),
      edges: new vis.DataSet(this.props.edges),
    };
    new vis.Network(this.graphRef.current, data, this.props.options);
  }

  render() {
    return (
      <div className="vis-graph" ref={this.graphRef}>
        No content
      </div>
    );
  }
}

export default Graph;
