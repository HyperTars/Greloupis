import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { TEST_ENDPOINT } from "./Endpoint";
import Dashboard from "./Dashboard";

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Switch>
            <Route
              path=""
              render={() => <Dashboard endpoint={TEST_ENDPOINT} />}
            />
          </Switch>
        </div>
      </Router>
    );
  }
}

export default App;
