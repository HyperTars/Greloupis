import React from "react";
import { Redirect, withRouter } from "react-router-dom";
import AuthService from "../service/AuthService";

class Logout extends React.Component {
  render() {
    AuthService.logout();
    return <Redirect to={{ pathname: "/" }} />;
  }
}

export default withRouter(Logout);
