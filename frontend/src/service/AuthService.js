import { createUser, userLogin } from "../components/FetchData";

class AuthService {
  login(username, password) {
    return userLogin({
      user: username, // support both name and email
      user_password: password,
    }).then((response) => {
      console.log(response);
      if (response.user_token) {
        localStorage.setItem("user_token", JSON.stringify(response.user_token));
      }
      if (response.user_id) {
        localStorage.setItem("user_id", JSON.stringify(response.user_id));
      }
      if (response.user_name) {
        localStorage.setItem("user_name", JSON.stringify(response.user_name));
      }
      if (response.user_thumbnail) {
        localStorage.setItem(
          "user_thumbnail",
          JSON.stringify(response.user_thumbnail)
        );
      }
      return response.user_token;
    });
  }

  isAuth() {
    return (
      !!localStorage.getItem("user_token") && !!localStorage.getItem("user_id")
    );
  }

  register(username, email, password) {
    return createUser({
      user_name: username,
      user_email: email,
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
      if (response.user_thumbnail) {
        localStorage.setItem(
          "user_thumbnail",
          JSON.stringify(response.user_thumbnail)
        );
      }
      return response.user_token;
    });
  }

  getCurrentUser() {
    return JSON.parse(localStorage.getItem("user_token"));
  }
}

export default new AuthService();
