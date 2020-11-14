import React from 'react';
import {Route,Redirect,withRouter} from 'react-router-dom';
import PropTypes from 'prop-types';
//私有路由，只有登录的用户才能访问
class PrivateRoute2 extends React.Component{
    componentWillMount(){
        let  isAuthenticated =  sessionStorage.getItem("userName") ? true :false;
        this.setState({isAuthenticated:isAuthenticated})
        if(!isAuthenticated){
            const {history} = this.props;
            setTimeout(() => {
                history.replace("/");
            }, 1000)
        }
    }
    render(){
        let { component: Component,path="/",exact=false,strict=false} = this.props;
        return this.state.isAuthenticated ?  (
            <Route  path={path} exact={exact}  strict={strict}  render={(props)=>( <Component {...props} /> )} />
        ) :  <Redirect
            to={{
                pathname: "/",
            }}    //这里必须使用redireact不能和上面一样使用<Route/>  因为会出现页面先跳转到myOption然后再跳转到首页的状况，这样用户体验不好
        /> ;
    }
}
PrivateRoute2.propTypes  ={
    path:PropTypes.string.isRequired,
    exact:PropTypes.bool,
    strict:PropTypes.bool,
    component:PropTypes.func.isRequired
}
export default withRouter(PrivateRoute2);