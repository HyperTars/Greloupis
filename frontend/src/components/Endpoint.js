export const HEROKU_ENDPOINT = "https://greloupis-backend.herokuapp.com";
export const LOCAL_ENDPOINT = "http://localhost:5000";

export function backendPoint() {
    if (!process.env.PROFILE || process.env.PROFILE === "prod")
        return HEROKU_ENDPOINT;
    return LOCAL_ENDPOINT;
}