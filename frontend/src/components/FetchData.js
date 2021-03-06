import { backendPoint } from "./Endpoint";
import { authHeader } from "../service/AuthHeader";
import AuthService from "../service/AuthService";
import logout from "./Logout";

export class GatewayTimeout extends Error {}
export class NotFoundError extends Error {}
export class ServerError extends Error {}
export class ClientError extends Error {}

const CURRENT_ENDPOINT = backendPoint();

function fetchWithErrorHandling(url, method, data) {
  let retryCount = 3;

  async function handleErrors(response, method, data) {
    let responseJson = await response.clone().json();

    if (
      response == null ||
      response.status == null ||
      response.status === 504
    ) {
      if (retryCount > 0) {
        // retry for gateway timeout
        retryCount -= 1;

        if (method === "GET" || method === "DELETE") {
          return fetch(url, {
            method: method,
            credentials: "include",
            headers: authHeader(),
          })
            .then(handleErrors)
            .catch((error) => {
              throw error;
            });
        } else if (method === "POST" || method === "PUT") {
          return fetch(url, {
            method: method,
            headers: authHeader(),
            credentials: "include",
            body: data,
          })
            .then(handleErrors)
            .catch((error) => {
              throw error;
            });
        }
      } else {
        throw new GatewayTimeout(response.status + responseJson["message"]);
      }
    } else if (response.status >= 500) {
      throw new ServerError(response.status + responseJson["message"]);
    } else if (response.status === 404) {
      throw new NotFoundError(response.status + responseJson["message"]);
    } else if (response.status >= 400) {
      throw new ClientError(response.status + responseJson["message"]);
    } else if (!response.ok) {
      throw Error(response.status + responseJson["message"]);
    } else {
      if (responseJson.code === -10000) {
        if (AuthService.isAuth()) {
          alert("Local user token has expired!");
          logout();
        }
      }

      return response;
    }
  }
  if (method === "GET" || method === "DELETE") {
    return fetch(url, {
      method: method,
      headers: authHeader(),
      credentials: "include",
    })
      .then(handleErrors)
      .catch((error) => {
        throw error;
      });
  } else if (method === "POST" || method === "PUT") {
    if (data === {}) return {};
    return fetch(url, {
      method: method,
      headers: authHeader(),
      credentials: "include",
      body: JSON.stringify(data),
    })
      .then(handleErrors)
      .catch((error) => {
        throw error;
      });
  }
}

function fetchJsonWithErrorHandling(url, method, data) {
  return fetchWithErrorHandling(url, method, data).then(
    (response) => response && response.json()
  );
}

// user related APIs
export function createUser(data = {}) {
  const url = `${CURRENT_ENDPOINT}/user`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function userLogin(data = {}) {
  const url = `${CURRENT_ENDPOINT}/user/login`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function updateUserInfo(id, data = {}) {
  const url = `${CURRENT_ENDPOINT}/user/${id}`;
  return fetchJsonWithErrorHandling(url, "PUT", data);
}

export function getUserInfo(id, data = {}) {
  const url = `${CURRENT_ENDPOINT}/user/${id}`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function deleteUser(id, data = {}) {
  const url = `${CURRENT_ENDPOINT}/user/${id}`;
  return fetchJsonWithErrorHandling(url, "DELETE", data);
}

// video related APIs
export function createVideo(data = {}) {
  const url = `${CURRENT_ENDPOINT}/video`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function updateVideoInfo(id, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${id}`;
  return fetchJsonWithErrorHandling(url, "PUT", data);
}

export function getVideoInfo(id, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${id}`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function deleteVideo(id, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${id}`;
  return fetchJsonWithErrorHandling(url, "DELETE", data);
}

export function getVideoComments(id, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${id}/comment`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function getVideoDislikes(id, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${id}/dislike`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function getVideoLikes(id, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${id}/like`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function getVideoStars(id, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${id}/star`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function getVideoViews(id, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${id}/view`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function updateVideoViews(id, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${id}/view`;
  return fetchJsonWithErrorHandling(url, "PUT", data);
}

// video & user related APIs
export function createUserVideoComment(videoId, userId, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${videoId}/comment/${userId}`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function deleteUserVideoComment(videoId, userId, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${videoId}/comment/${userId}`;
  return fetchJsonWithErrorHandling(url, "DELETE", data);
}

export function createUserVideoDislike(videoId, userId, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${videoId}/dislike/${userId}`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function deleteUserVideoDislike(videoId, userId, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${videoId}/dislike/${userId}`;
  return fetchJsonWithErrorHandling(url, "DELETE", data);
}

export function createUserVideoLike(videoId, userId, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${videoId}/like/${userId}`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function deleteUserVideoLike(videoId, userId, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${videoId}/like/${userId}`;
  return fetchJsonWithErrorHandling(url, "DELETE", data);
}

export function createUserVideoProcess(videoId, userId, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${videoId}/process/${userId}`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function getUserVideoProcess(videoId, userId, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${videoId}/process/${userId}`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function updateUserVideoProcess(videoId, userId, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${videoId}/process/${userId}`;
  return fetchJsonWithErrorHandling(url, "PUT", data);
}

export function createUserVideoStar(videoId, userId, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${videoId}/star/${userId}`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function deleteUserVideoStar(videoId, userId, data = {}) {
  const url = `${CURRENT_ENDPOINT}/video/${videoId}/star/${userId}`;
  return fetchJsonWithErrorHandling(url, "DELETE", data);
}

// search related APIs
export function searchUser(keyword, data = {}) {
  const url = `${CURRENT_ENDPOINT}/search/user?keyword=${keyword}`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function searchVideo(keyword, data = {}) {
  const url = `${CURRENT_ENDPOINT}/search/video?keyword=${keyword}`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function searchTopVideo(keyword, data = {}) {
  const url = `${CURRENT_ENDPOINT}/search/video/top?keyword=${keyword}`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}
