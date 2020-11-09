import React, { Component } from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  // Redirect,
} from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import Dashboard from "./Dashboard";
import Header from "./Header";
import SearchResult from "./SearchResult";
import Login from "./Login";
import Register from "./Register";
import EmptyPage from "./EmptyPage";
import UserProfile from "./UserProfile";
import VideoPlay from "./VideoPlay";
import VideoUpload from "./VideoUpload";

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
            <Route
              exact
              path="/video/upload"
              render={(props) => <VideoUpload />}
            />
            <Route
              exact
              path="/user/:userId"
              render={(props) => (
                <UserProfile userId={props.match.params.userId} />
              )}
            />
            <Route
              exact
              path="/video/:videoId"
              render={(props) => (
                <VideoPlay videoId={props.match.params.videoId} />
              )}
            />
            <Route exact path="/404" render={() => <EmptyPage />} />
            {/* <Route path="*" render={() => <Redirect to="/404"></Redirect>} /> */}
          </Switch>
        </div>
      </Router>
    );
  }
}

export default App;
