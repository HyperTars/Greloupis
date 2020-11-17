import React from "react";
import { withRouter } from "react-router-dom";
import AuthService from "../service/AuthService";

class Logout extends React.Component {
  render() {
    AuthService.logout();
    window.location.replace("/");
    return;
  }
}

export default withRouter(Logout);
