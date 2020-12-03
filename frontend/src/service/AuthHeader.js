export function authHeader() {
  const user_token = JSON.parse(localStorage.getItem("user_token"));
  const user_id = JSON.parse(localStorage.getItem("user_id"));

  if (user_token && user_id) {
    return {
      "Content-Type": "application/json",
      Authorization: "Bearer " + user_token,
    };
  } else {
    return {};
  }
}
