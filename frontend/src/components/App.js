import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Home from "./Home";
import Header from "./Header";
import SearchResult from "./SearchResult";
import Login from "./Login";
import Logout from "./Logout";
import Register from "./Register";
// import EmptyPage from "./EmptyPage";
import UserProfile from "./UserProfile";
import VideoUpload from "./VideoUpload";
import VideoUpdate from "./VideoUpdate";
import VideoPlay from "./VideoPlay";
import PrivateRoute from "./PrivateRoute";

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
                <div className="homePage">
                  <Header />
                  <Home />
                </div>
              )}
            />
            <Route
              exact
              path="/search"
              render={() => (
                <div className="searchPage">
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
              path="/video/update/:videoId"
              render={(props) => (
                <div>
                  <Header />
                  <VideoUpdate videoId={props.match.params.videoId} />
                </div>
              )}
            />
            <Route
              exact
              path="/user/:userId"
              render={(props) => (
                <div className="userProfilePage">
                  <Header />
                  <UserProfile userId={props.match.params.userId} />
                </div>
              )}
            />
            <Route
              exact
              path="/video/:videoId"
              render={(props) => (
                <div className="videoPlay">
                  <Header />
                  <VideoPlay videoId={props.match.params.videoId} />
                </div>
              )}
            />
            <Route
              exact
              path="/500"
              render={() => {
                window.location.href = "500.html";
              }}
            />
            <Route
              exact
              path="/403"
              render={() => {
                window.location.href = "403.html";
              }}
            />
            <Route
              render={() => {
                window.location.href = "404.html";
              }}
            />
            {/* <Route component={EmptyPage} render={() => <EmptyPage />} /> */}
          </Switch>
        </div>
      </Router>
    );
  }
}

export default App;
