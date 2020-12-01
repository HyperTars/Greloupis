export const HEROKU_ENDPOINT = "https://greloupis-backend.herokuapp.com";
export const LOCAL_ENDPOINT = "http://localhost:5000";

export function backendPoint() {
  if (process.env.NODE_ENV === "development") return LOCAL_ENDPOINT;
  return HEROKU_ENDPOINT;
}
