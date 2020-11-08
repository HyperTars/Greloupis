import { createUser, userLogin } from "../components/FetchData";

class AuthService {
  login(username, password) {
    return userLogin({
      user_name: username,
      user_password: password,
    }).then((response) => {
      if (response.token) {
        localStorage.setItem("user", JSON.stringify(response.token));
      }
      return response.token;
    });
  }

  logout() {
    localStorage.removeItem("user");
  }

  register(username, email, password) {
    return createUser({
        user_name: username,
        user_email: email,
        user_password: password
    });
  }

  getCurrentUser() {
    return JSON.parse(localStorage.getItem("user"));
  }
}

export default new AuthService();
