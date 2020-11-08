import { createUser, userLogin } from "../components/FetchData";

class AuthService {
  login(username, password) {
    return userLogin({
      name: username,
      password: password,
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
        username: username,
        email: email,
        password: password
    });
  }

  getCurrentUser() {
    return JSON.parse(localStorage.getItem("user"));
  }
}

export default new AuthService();
