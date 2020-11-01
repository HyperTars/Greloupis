export class GatewayTimeout extends Error {}
export class NotFoundError extends Error {}
export class ServerError extends Error {}
export class ClientError extends Error {}

function fetchWithErrorHandling(url, method, data) {
  let retryCount = 3;

  function handleErrors(response, method, data) {
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
          })
            .then(handleErrors)
            .catch((error) => {
              throw error;
            });
        } else if (method === "POST" || method === "PUT") {
          return fetch(url, {
            method: method,
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
            body: data,
          })
            .then(handleErrors)
            .catch((error) => {
              throw error;
            });
        }
      } else {
        throw new GatewayTimeout(response.statusText);
      }
    } else if (response.status >= 500) {
      throw new ServerError(response.statusText);
    } else if (response.status === 404) {
      throw new NotFoundError(response.statusText);
    } else if (response.status >= 400) {
      throw new ClientError(response.statusText);
    } else if (!response.ok) {
      throw Error(response.statusText);
    } else {
      return response;
    }
  }
  if (method === "GET" || method === "DELETE") {
    return fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
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
      headers: {
        "Content-Type": "application/json",
      },
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
export function createUser(endpoint, data = {}) {
  const url = `${endpoint}/user`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function userLogin(endpoint, data = {}) {
  const url = `${endpoint}/user/login`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function userLogout(endpoint, data = {}) {
  const url = `${endpoint}/user/logout`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function updateUserInfo(endpoint, id, data = {}) {
  const url = `${endpoint}/user/${id}`;
  return fetchJsonWithErrorHandling(url, "PUT", data);
}

export function getUserInfo(endpoint, id, data = {}) {
  const url = `${endpoint}/user/${id}`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function deleteUser(endpoint, id, data = {}) {
  const url = `${endpoint}/user/${id}`;
  return fetchJsonWithErrorHandling(url, "DELETE", data);
}

export function getUserComments(endpoint, id, data = {}) {
  const url = `${endpoint}/user/${id}/comment`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function getUserDislikes(endpoint, id, data = {}) {
  const url = `${endpoint}/user/${id}/dislike`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function getUserLikes(endpoint, id, data = {}) {
  const url = `${endpoint}/user/${id}/like`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function getUserProcesses(endpoint, id, data = {}) {
  const url = `${endpoint}/user/${id}/process`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function getUserStars(endpoint, id, data = {}) {
  const url = `${endpoint}/user/${id}/star`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

// video related APIs
export function createVideo(endpoint, data = {}) {
  const url = `${endpoint}/video`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function updateVideoInfo(endpoint, id, data = {}) {
  const url = `${endpoint}/video/${id}`;
  return fetchJsonWithErrorHandling(url, "PUT", data);
}

export function getVideoInfo(endpoint, id, data = {}) {
  const url = `${endpoint}/video/${id}`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function deleteVideo(endpoint, id, data = {}) {
  const url = `${endpoint}/video/${id}`;
  return fetchJsonWithErrorHandling(url, "DELETE", data);
}

export function getVideoComments(endpoint, id, data = {}) {
  const url = `${endpoint}/video/${id}/comment`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function getVideoDislikes(endpoint, id, data = {}) {
  const url = `${endpoint}/video/${id}/dislike`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function getVideoLikes(endpoint, id, data = {}) {
  const url = `${endpoint}/video/${id}/like`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function getVideoStars(endpoint, id, data = {}) {
  const url = `${endpoint}/video/${id}/star`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function getVideoViews(endpoint, id, data = {}) {
  const url = `${endpoint}/video/${id}/view`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function updateVideoViews(endpoint, id, data = {}) {
  const url = `${endpoint}/video/${id}/view`;
  return fetchJsonWithErrorHandling(url, "PUT", data);
}

// video & user related APIs
export function updateUserVideoComment(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/comment/${userId}`;
  return fetchJsonWithErrorHandling(url, "PUT", data);
}

export function getUserVideoComment(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/comment/${userId}`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function createUserVideoComment(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/comment/${userId}`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function deleteUserVideoComment(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/comment/${userId}`;
  return fetchJsonWithErrorHandling(url, "DELETE", data);
}

export function createUserVideoDislike(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/dislike/${userId}`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function deleteUserVideoDislike(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/dislike/${userId}`;
  return fetchJsonWithErrorHandling(url, "DELETE", data);
}

export function createUserVideoLike(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/like/${userId}`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function deleteUserVideoLike(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/like/${userId}`;
  return fetchJsonWithErrorHandling(url, "DELETE", data);
}

export function createUserVideoProcess(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/process/${userId}`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function deleteUserVideoProcess(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/process/${userId}`;
  return fetchJsonWithErrorHandling(url, "DELETE", data);
}

export function getUserVideoProcess(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/process/${userId}`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function updateUserVideoProcess(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/process/${userId}`;
  return fetchJsonWithErrorHandling(url, "PUT", data);
}

export function createUserVideoStar(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/star/${userId}`;
  return fetchJsonWithErrorHandling(url, "POST", data);
}

export function deleteUserVideoStar(endpoint, videoId, userId, data = {}) {
  const url = `${endpoint}/video/${videoId}/star/${userId}`;
  return fetchJsonWithErrorHandling(url, "DELETE", data);
}

// search related APIs
export function searchUser(endpoint, keyword, data = {}) {
  const url = `${endpoint}/search/user?keyword=${keyword}`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}

export function searchVideo(endpoint, keyword, data = {}) {
  const url = `${endpoint}/search/video?keyword=${keyword}`;
  return fetchJsonWithErrorHandling(url, "GET", data);
}
