import React, { Component } from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import Dashboard from "./Dashboard";
import Header from "./Header";
import SearchResult from "./SearchResult";
import Login from "./Login";
import Register from "./Register";
import EmptyPage from "./EmptyPage";

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Switch>
            <Route
              exact
              path="/home"
              render={() => (
                <div>
                  <Header />
                  <Dashboard />
                </div>
              )}
            />
            <Route
              exact
              path="/search"
              render={(props) => (
                <div>
                  <Header />
                  <SearchResult />
                </div>
              )}
            />
            <Route
              exact
              path="/login"
              component={Login}
              render={(props) => <Login />}
            />
            <Route
              exact
              path="/register"
              component={Register}
              render={(props) => <Register />}
            />
            <Route exact path="/404" render={() => <EmptyPage />} />
            <Route path="*" render={() => <Redirect to="/404"></Redirect>} />
          </Switch>
        </div>
      </Router>
    );
  }
}

export default App;
