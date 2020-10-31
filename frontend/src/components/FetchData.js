export class GatewayTimeout extends Error {}
export class NotFoundError extends Error {}
export class ServerError extends Error {}
export class ClientError extends Error {}

function fetchWithErrorHandling(url, options = {}) {
  let retryCount = 3;

  function handleErrors(response) {
    if (
      response == null ||
      response.status == null ||
      response.status === 504
    ) {
      if (retryCount > 0) {
        // retry for gateway timeout
        retryCount -= 1;

        return fetch(url, {
          ...options,
          credentials: "include",
        }).then(handleErrors);
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

  return fetch(url, {
    ...options,
    credentials: "include", // include, *same-origin, omit
  })
    .then(handleErrors)
    .catch((error) => {
      throw error;
    });
}

function fetchJsonWithErrorHandling(url, options = {}) {
  return fetchWithErrorHandling(url, options).then(
    (response) => response && response.json()
  );
}

export function getUserInfoById(endpoint, id) {
  const url = `${endpoint}/user/${id}`;
  return fetchJsonWithErrorHandling(url);
}

export function searchVideoByKeyword(endpoint, keyword) {
  const url = `${endpoint}/search/video?keyword=${keyword}`;
  return fetchJsonWithErrorHandling(url);
}
