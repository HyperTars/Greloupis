import React, { Component } from 'react';
import {BrowserRouter as Router} from 'react-router-dom';

class App extends Component {
  
  render() {
    // let LOCAL_BASE_URL = "127.0.0.1"
    let TEST_BASE_URL = "0.0.0.0"

    let url1 = `http://${TEST_BASE_URL}:5000/user/5f88f883e6ac4f89900ac983`

    fetch(url1, {credentials: "include"})
        .then(response => response.json())
        .then((responseData) => {
              console.log(responseData);
              return responseData;
            });

    let url2 = `http://${TEST_BASE_URL}:5000/search/video?keyword=ih`

    fetch(url2, {credentials: "include"})
        .then(response => response.json())
        .then((responseData) => {
              console.log(responseData);
              return responseData;
            });

    return (
      <Router>
        <div className="App">
            <h1>Frontend under construction</h1>
            <div> check console </div>
            <div>{this.res}</div>
        </div>
      </Router>
    );
  }
}

export default App;
