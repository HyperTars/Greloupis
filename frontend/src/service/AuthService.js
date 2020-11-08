import { createUser, userLogin } from "../components/FetchData";

class AuthService {
  login(username, password) {
    return userLogin({
      // user_name: username,
      user: username, // support both name and email
      user_password: password,
    }).then((response) => {
      if (response.user_token && response.user_id) {
        localStorage.setItem("user_token", JSON.stringify(response.user_token));
        localStorage.setItem("user_id", JSON.stringify(response.user_id));
      }
      return response.user_token;
    });
  }

  logout() {
    localStorage.removeItem("user_token");
    localStorage.removeItem("user_id");
  }

  register(username, email, password) {
    return createUser({
        user_name: username,
        user_email: email,
        user_password: password
    });
  }

  getCurrentUser() {
    return JSON.parse(localStorage.getItem("user_token"));
  }
}

export default new AuthService();
