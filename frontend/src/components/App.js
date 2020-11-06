import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { TEST_ENDPOINT /*, LOCAL_ENDPOINT*/ } from "./Endpoint";
import Dashboard from "./Dashboard";
import Header from "./Header";
import SearchResult from "./SearchResult";

const CURRENT_ENDPOINT = TEST_ENDPOINT;

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Header />
          <Switch>
            <Route
              path="/home"
              render={() => <Dashboard endpoint={CURRENT_ENDPOINT} />}
            />
            <Route
              path="/search"
              render={(props) => <SearchResult endpoint={CURRENT_ENDPOINT} />}
            />
          </Switch>
        </div>
      </Router>
    );
  }
}

export default App;
