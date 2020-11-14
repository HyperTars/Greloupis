import React, { Component } from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  // Redirect,
} from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import Home from "./Home";
import Header from "./Header";
import SearchResult from "./SearchResult";
import Login from "./Login";
import Logout from "./Logout";
import Register from "./Register";
import EmptyPage from "./EmptyPage";
import UserProfile from "./UserProfile";
import VideoUpload from "./VideoUpload";
import VideoPlay from "./VideoPlay";
import PrivateRoute from "./PrivateRoute";
import Dashboard from "./Dashboard";

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Switch>
            <Route
              exact
              path="/"
              render={() => (
                <div>
                  <Header />
                  <Home />
                </div>
              )}
            />
            <Route
              exact
              path="/search"
              render={() => (
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
              path="/logout"
              component={Logout}
              render={(props) => <Logout />}
            />
            <Route
              exact
              path="/register"
              component={Register}
              render={(props) => <Register />}
            />
            <PrivateRoute
              exact
              path="/video/upload"
              component={VideoUpload}
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
                <div>
                  <Header />
                  <VideoPlay videoId={props.match.params.videoId} />
                </div>
              )}
            />
            <Route exact path="/404" render={() => <EmptyPage />} />
            <PrivateRoute
              exact
              path="/dashboard"
              component={Dashboard}
              render={(props) => <Dashboard />}
            />
            {/* <Route path="*" render={() => <Redirect to="/404"></Redirect>} /> */}
          </Switch>
        </div>
      </Router>
    );
  }
}

export default App;
