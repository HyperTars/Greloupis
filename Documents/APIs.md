# APIs Design

  In this document, we list our all APIs for quick overview. The full API endpoints list and description can be seen in
 [Swagger YML file](https://github.com/HyperTars/Online-Video-Platform/blob/master/Documents/swagger.yml).

## User Auth
### Overview
Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
user_create | Create user account | POST | /user
user_login | Logs user into the system | POST | /user/login
user_logout | Logs out current user session | POST | /user/logout
user_get | Get user by user name | GET | /user/{user_id}
user_update | Update user account | PUT | /user/{user_id}
user_delete | Delete user account | DELETE | /user/{user_id}

### User Create
- **Function**
  - user_create (user_name, user_email, user_password, first_name, last_name, phone)

- **Parameters**
  ```
  "body": {
    "user_name": string,
    "user_email": string,
    "user_password": string,
    "user_details": UserDetail {
        "first_name": string,
        "last_name": string,
        "phone": string
      }
  }
  ```
  
- **Returns**
  - 200 (default): successful operation
    ```
    "body": {
      "user_id": string,
      "user_name": string,
      "user_email": string,
      "user_password": string,
      "user_status": enum,
      "user_thumbnail": Thumbnail {
        "thumbnail_uri": string,
        "thumbnail_type": enum
      }
      "user_details": UserDetail {
        "first_name": string,
        "last_name": string,
        "phone": string
      }
      "user_followers": big int,
      "user_reg_date": date-type,
      "user_recent_login": LoginDetail {
        "login_ip": string,
        "login_time": date-type
      }
    }
    ```
  - 400: bad request
  - 50x: internal server error

### User Login
- **Function**
  - user_login (api_dev_key, user_name, user_email, user_password)
  - Either `user_name` or `user_email` must exist

- **Parameters**
  ```
  "body": {
    "user_name": string,
    "user_email": string,
    "user_password": string
  }
  ```
  Either `user_name` or `email` must be input; `password` is required.

- **Returns**
  - 200 (default): successful operation
    - `X-Rate-Limit`: integer
    - `X-Expires-After`: string
  - 400: invalid username/email/password supplied
  - 50x: internal server error

### User Logout
- **Function**
  - user_logout (api_dev_key)

- **Parameters**
  - None

- **Returns**
  - 200 (default): successful operation
  - 400: bad request
  - 50x: internal server error

### User Get
- **Function**
  - user_get (api_dev_key, user_id)

- **Parameters**
  - "body": {
      "user_id": string
    }

- **Returns**
  - 200 (default): successful operation
    ```
    "body": {
      "user_id": string,
      "user_name": string,
      "user_email": string,
      "user_password": string,
      "user_status": enum,
      "user_thumbnail": Thumbnail {
        "thumbnail_uri": string,
        "thumbnail_type": enum
      }
      "user_details": UserDetail {
        "first_name": string,
        "last_name": string,
        "phone": string
      }
      "user_followers": big int,
      "user_reg_date": date-type,
      "user_recent_login": LoginDetail {
        "login_ip": string,
        "login_time": date-type
      }
    }
    ```
  - 400: invalid username supplied
  - 404: user not found
  - 50x: internal server error

### User Update
- **Function**
  - user_update(api_dev_key, user_id, user_name, user_email, user_password, first_name, last_name, phone)

- **Parameters**
  ```
  "user_id": string,
  "body": {
    "user_name": string,
    "user_email": string,
    "user_password": string,
    "user_details": UserDetail {
        "first_name": string,
        "last_name": string,
        "phone": string
      }
  }
  ```
- **Returns**
  - 200 (default): successful operation
    ```
    "body": {
      "user_id": string,
      "user_name": string,
      "user_email": string,
      "user_password": string,
      "user_status": enum,
      "user_thumbnail": Thumbnail {
        "thumbnail_uri": string,
        "thumbnail_type": enum
      }
      "user_details": UserDetail {
        "first_name": string,
        "last_name": string,
        "phone": string
      }
      "user_followers": big int,
      "user_reg_date": date-type,
      "user_recent_login": LoginDetail {
        "login_ip": string,
        "login_time": date-type
      }
    }
    ```
  - 400: invalid username supplied
  - 404: user not found
  - 405: method not allowed
  - 50x: internal server error

### User Delete
- **Function**
  - user_delete(api_dev_key)

- **Parameters**
  - None

- **Returns**
  - 200 (default): successful operation
    ```
    "body": {
      "message": "..."
    }
    ```
  - 400: invalid username supplied
  - 404: user not found
  - 405: method not allowed
  - 50x: internal server error

## Video
### Overview
Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
video_upload | upload video | POST | /user/{user_id}/video
video_update | update video information | PUT | /user/{user_id}/video/{video_id}
video_delete | delete video | DELETE | /user/{user_id}/video/{video_id}
video_get | get video content cache | GET | /video/{video_id}

### Video Upload
- **Function**
  - video_upload (api_dev_key, video_title, video_tag, video_category, video_description, video_language, video_status, video_contents)

- **Parameters**
  Name | Type | Description
    --- | --- | ---
    api_dev_key | string | This will be used to, among other things, throttle users based on their allocated quota.
    video_title | string | video title
    video_tag | string[] | (optional) video tags
    video_category | string | category of video, e.g., Movie, Vlog, Song, News, Tech, etc.
    video_description | string | (optional) video description
    video_language | string | e.g., English, Mandarin, Hindi, etc.
    video_status | string | (optional, default public) e.g., public, private, limited share.
    video_contents | stream | video to be uploaded.

- **Returns**
  - (default) 202 (request accepted), once the video encoding is completed the user is notified through email with a link to access the video. We can also expose a queryable API to let users know the current status of their uploaded video.

### Video Get
- **Function**
  - video_get(api_dev_key, video_id, offset, codec, resolution)

- **Parameters**
  - api_dev_key (string): The API developer key of a registered account of our service.
  - video_id (string): A string to identify the video.
  - offset (number): We should be able to stream video from any offset; this offset would be a time in seconds from the beginning of the video. If we support playing/pausing a video from multiple devices, we will need to store the offset on the server. This will enable the users to start watching a video on any device from the same point where they left off. 
  - codec (string) & resolution(string): We should send the codec andresolution info in the API from the client to support play/pause from multiple devices. Imagine you are watching a video on your TV’s Netflix app, paused it, and started watching it on your phone’s Netflix app. In this case, you would need codec and resolution, as both these devices have a different resolution and use a different codec.

- **Returns: (STREAM)**
  - A media stream (a video chunk) from the given offset.

### Video Update
- **Function**
  - video_update (api_dev_key, video_title, video_tag, video_category, video_description, video_language, video_status)

- **Parameters**
  ```
  "body": {
    "video_title": string,
    "video_tag": string[],
    "video_category": string[],
    "video_description": string,
    "video_language": enum,
    "video_status": enum
  }
  ```
- **Returns**
  - 200 (default): successful operation
    ```
      "body": {
        "video_id": string,
        "user_id": string,
        "video_title": string,
        "video_tag": string[],
        "video_category": string[],
        "video_description": string,
        "video_language": enum,
        "video_status": enum,
        "video_contents": stream,
        "video_content_status": enum,
        "video_size": float,
        "video_views": big int,
        "video_likes": big int,
        "video_dislikes": big int,
        "video_comments": big int,
        "video_stars": big int,
        "video_shares": big int,
        "video_thumbnail": Thumbnail,
        "video_upload_date": date-type,
        "video_uri": VideoURI
    }
    ```
  - 400: bad request
  - 405: method not allowed
  - 50x: internal server error

### Video Delete
- **Function**
  - video_delete (api_dev_key, video_id)

- **Parameters**
  ```
  "body": {
    "video_id": string
  }
  ```
- **Returns**
  
  Need to check if user has permission to delete video. Returns:

  - HTTP response 200 (OK)
  - 202 (Accepted) if the action has been queued
  - 204 (No Content) based on your response
  - 400: bad request
  - 404: `user_id` or `video_id` not found
  - 405: method not allowed
  - 50x: internal server error

## Search
### Overview
Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
search_video | Search video list by keyword | GET | /search/video?q={keyword}
search_user | Search user list by keyword | GET | /search/user?q={keyword}

### Search Video
- **Function**
  - search_video (api_dev_key, search_query, user_location, maximum_videos_to_return, page_token)
    - api_dev_key (string): The API developer key of a registered account of our service.
    - search_query (string): A string containing the search terms. 
    - user_location (string): Optional location of the user performing the search.
    - maximum_videos_to_return (number): Maximum number of results returned in one request.
    - page_token (string): This token will specify a page in the result set that should be returned.

- **Parameters**
  ```
  "body": {
    "keyword": string
  }
  ```

- **Returns**
  - 200: successful operation
  - 400: bad request
  - 50x: internal server error

### Search User
- **Function**
  - search_user ()

- **Parameters**
  ```
  "body": {
    "keyword": string
  }
  ```
- **Returns**
  - 200: successful operation
  - 400: bad request
  - 50x: internal server error
  
## Watch History
### Overview
Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
history_create | Add a video to history list | POST | /user/{user_id}/history/{video_id}
history_update | Update history list | PUT | /user/{user_id}/history/{video_id}
history_get | Get history list by user id | GET | /user/{user_id}/history/
history_delete | Delete a video from history list | DELETE | /user/{user_id}/history/{video_id}

### History Create
- **Function**
  - history_create()

- **Parameters**
  ```
  "body": {
    "user_id": string,
    "video_id": string
  }
  ```
- **Returns**
  - 200 (default): successful operation
    ```
    "body": {
      "message": "..."
    }
    ```
  - 400: invalid `user_id` or `video_id` supplied
  - 404: `user_id` or `video_id` not found
  - 405: method not allowed
  - 50x: internal server error

### History Update
- **Function**
  - history_update()

- **Parameters**
  ```
  "body": {
    "user_id": string,
    "video_id": string
  }
  ```
- **Returns**
  - 200 (default): successful operation
    ```
    "body": {
      "message": "..."
    }
    ```
  - 400: invalid `user_id` or `video_id` supplied
  - 404: `user_id` or `video_id` not found
  - 405: method not allowed
  - 50x: internal server error

### History Get
- **Function**
  - history_get()

- **Parameters**
  ```
  "body": {
    "user_id": string
  }
  ```
- **Returns**
  - 200 (default): successful operation
    ```
    "body": {
      "message": "..."
    }
    ```
  - 400: invalid `user_id` supplied
  - 404: `user_id` not found
  - 50x: internal server error

### History Delete
- **Function**
  - history_delete()

- **Parameters**
  ```
  "body": {
    "user_id": string,
    "video_id": string
  }
  ```
- **Returns**
  - 200 (default): successful operation
    ```
    "body": {
      "message": "..."
    }
    ```
  - 400: invalid `user_id` or `video_id` supplied
  - 404: `user_id` or `video_id` not found
  - 405: method not allowed
  - 50x: internal server error


## Video Op
### Overview
Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
like_post | Post video like | POST | /video/{video_id}/like/{user_id}
like_list_by_video | Get like list by video | GET | /video/{video_id}/like/
like_list_by_user | Get like list by user | GET | /user/{user_id}/like/
like_delete | Delete specified like by video and user | DELETE | /video/{video_id}/like/{user_id}
  | | | 
dislike_post | Post video dislike | POST | /video/{video_id}/dislike/{user_id}
dislike_list_by_video | Get dislike list by video | GET | /video/{video_id}/dislike/
dislike_list_by_user | Get dislike list by user | GET | /user/{user_id}/dislike/
dislike_delete | Delete specified dislike by video and user | DELETE | /video/{video_id}/dislike/{user_id}
  | | |  
comment_post | Post video comment | POST | /video/{video_id}/comment/{user_id}
comment_list_by_video | Get comment list by video | GET | /video/{video_id}/comment/
comment_list_by_user | Get comment list by user | GET | /user/{user_id}/comment/
comment_get | Get specified comment by video and user | GET | /video/{video_id}/comment/{user_id}
comment_update | Update specified comment by video and user | PUT | /video/{video_id}/comment/{user_id}
comment_delete | Delete specified comment by video and user | DELETE | /video/{video_id}/comment/{user_id}
  | | |
star_post | Post video star by video and user | POST | /video/{video_id}/star/{user_id}
star_list_by_video | Get star list by video | GET | /video/{video_id}/star/
star_list_by_user | Get star list by user | GET | /user/{user_id}/star/
star_delete | Delete star by video and user | DELETE | /video/{video_id}/star/{user_id}
  | | |
view_add | Add video views | PUT | /video/{video_id}/view/
view_get | Get video views | GET | /video/{video_id}/view/

## Follow
### Overview
Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
follow | Follow an uploader | POST | /{user_id}`(follower)`/follow/{user_id}`(uploader)`
unfollow | Unfollow an uploader | DELETE | /{user_id}`(follower)`/follow/{user_id}`(uploader)`
following_list | Get all following uploader | GET | /{user_id}/follow/following
followers_list | Get all followers list | GET | /{user_id}/follow/followers

## (TBD) Recommendation
