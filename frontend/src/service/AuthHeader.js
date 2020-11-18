import { getSubstr } from "../util";

export function authHeader() {
  const user_token = getSubstr(localStorage.getItem("user_token"));
  const user_id = getSubstr(localStorage.getItem("user_id"));

  if (user_token && user_id) {
    return "Bearer " + user_token;
  } else {
    return "";
  }
}
