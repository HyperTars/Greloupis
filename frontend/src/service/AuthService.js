import { createUser, userLogin } from "../components/FetchData";

class AuthService {
  login(username, password) {
    return userLogin({
      // user_name: username,
      user: username, // support both name and email
      user_password: password,
    }).then((response) => {
      if (response.user_token) {
        localStorage.setItem("user_token", JSON.stringify(response.user_token));
      }
      if (response.user_id) {
        localStorage.setItem("user_id", JSON.stringify(response.user_id));
      }
      if (response.user_name) {
        localStorage.setItem("user_name", JSON.stringify(response.user_name));
      }
      return response.user_token;
    });
  }

  isAuth() {
    return !!localStorage.getItem("user_token") 
      && !!localStorage.getItem("user_id");
  }

  logout() {
    localStorage.removeItem("user_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_name");
  }

  register(username, email, password) {
    return createUser({
        user_name: username,
        user_email: email,
        user_password: password
    }).then((response) => {
      if (response.user_token) {
        localStorage.setItem("user_token", JSON.stringify(response.user_token));
      }
      if (response.user_id) {
        localStorage.setItem("user_id", JSON.stringify(response.user_id));
      }
      if (response.user_name) {
        localStorage.setItem("user_name", JSON.stringify(response.user_name));
      }
      return response.user_token;
    });
  }

  getCurrentUser() {
    return JSON.parse(localStorage.getItem("user_token"));
  }
}

export default new AuthService();
