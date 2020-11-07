import React, { Component } from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css"
import { TEST_ENDPOINT /*, LOCAL_ENDPOINT*/ } from "./Endpoint";
import Dashboard from "./Dashboard";
import Header from "./Header";
import SearchResult from "./SearchResult";
import Login from "./Login";
import Register from "./Register";

const CURRENT_ENDPOINT = TEST_ENDPOINT;

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Switch>
            <Route
              path="/home"              
              render={() => (
                <div>
                  <Header />
                  <Dashboard endpoint={CURRENT_ENDPOINT} />
                </div>
              )}
            />
            <Route
              path="/search"
              render={(props) => (
                <div>
                  <Header />
                  <SearchResult endpoint={CURRENT_ENDPOINT} />
                </div>
              )}
            />
            <Route
              exact path="/login"
              component={Login}
              render={(props) => <Login endpoint={CURRENT_ENDPOINT} />}
            />
            <Route
              path="/register"
              component={Register}
              render={(props) => <Register endpoint={CURRENT_ENDPOINT} />}
            />
            <Route path="/" render={() => <Redirect to="/home"></Redirect>} />
          </Switch>
        </div>
      </Router>
    );
  }
}

export default App;
