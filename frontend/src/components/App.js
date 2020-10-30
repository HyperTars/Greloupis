import React, { Component } from 'react';
import {BrowserRouter as Router} from 'react-router-dom';

class App extends Component {
  
  render() {
    // let LOCAL_BASE_URL = "127.0.0.1"
    let TEST_BASE_URL = "0.0.0.0"

    let url = `http://${TEST_BASE_URL}:5000/user/5f88f883e6ac4f89900ac983`

    fetch(url, {credentials: "include"})
      .then(response => response.json());

    return (
      <Router>
        <div className="App">
          <h1>Frontend under construction</h1>
        </div>
      </Router>
    );
  }
}

export default App;
