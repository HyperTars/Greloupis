import React from 'react';
import {Redirect,withRouter} from 'react-router-dom';
import PropTypes from 'prop-types';
import AuthService from "../service/AuthService";

class Logout extends React.Component {
    render() {
        AuthService.logout();
        return <Redirect to={{pathname: "/",}}/>;
    }
}

export default withRouter(Logout);