import React from "react";
import AuthService from "../service/AuthService";
import { Redirect, Route } from "react-router-dom";

const PrivateRoute = ({ component: Component, ...rest }) => {
  const isAuth = AuthService.isAuth();

  return (
    <Route
      {...rest}
      render={(props) =>
        isAuth ? (
          <Component {...props} />
        ) : (
          <Redirect
            to={{
              pathname: "/login",
              state: { from: props.location.pathname, reason: "Login First." },
            }}
          />
        )
      }
    />
  );
};

export default PrivateRoute;
