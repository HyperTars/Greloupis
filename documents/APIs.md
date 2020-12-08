[![logo](greloupis-horizontal.png)](https://greloupis-frontend.herokuapp.com/)

# APIs Design

In this document, we list our all APIs for quick overview. 

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
  - user_create (user_name, user_email, user_password)

- **Parameters**
  ```
  "user_name": string,
  "user_email": string,
  "user_password": string,
  ```
  
- **Returns**
  - 200 (default): successful operation
    ```
    {
      "code": "string",
      "body": {
        "user_id": "string",
        "user_name": "string",
        "user_email": "string",
        "user_password": "string",
        "user_detail": {
          "user_first_name": "string",
          "user_last_name": "string",
          "user_phone": "string",
          "user_street1": "string",
          "user_street2": "string",
          "user_city": "string",
          "user_state": "string",
          "user_country": "string",
          "user_zip": "string"
        },
        "user_status": "string",
        "user_thumbnail": "string",
        "user_follower": 0,
        "user_reg_date": "2020-12-02T20:46:49.404Z",
        "user_recent_login": [
          "string"
        ]
      }
    }
    ```
  - 400: bad request
  - 50x: internal server error

### User Login
- **Function**
  - user_login (user_name, user_email, user_password)
  - Either `user_name` or `user_email` must exist

- **Parameters**
  ```
  "user_name": string,
  "user_email": string,
  "user_password": string
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
  - user_logout (jwt_token)

- **Parameters**
  ```
  "jwt_token": string
  ```

- **Returns**
  - 200 (default): successful operation
  - 400: bad request
  - 50x: internal server error

### User Get
- **Function**
  - user_get (user_id)

- **Parameters**
  ```
  "user_id": string
  ```

- **Returns**
  - 200 (default): successful operation
    ```
    {
      "code": "string",
      "body": {
        "user_id": "string",
        "user_name": "string",
        "user_email": "string",
        "user_password": "string",
        "user_detail": {
          "user_first_name": "string",
          "user_last_name": "string",
          "user_phone": "string",
          "user_street1": "string",
          "user_street2": "string",
          "user_city": "string",
          "user_state": "string",
          "user_country": "string",
          "user_zip": "string"
        },
        "user_status": "string",
        "user_thumbnail": "string",
        "user_follower": 0,
        "user_reg_date": "2020-12-02T20:46:49.404Z",
        "user_recent_login": [
          "string"
        ]
      }
    }
    ```
  - 400: invalid username supplied
  - 404: user not found
  - 50x: internal server error

### User Update
- **Function**
  - user_update(jwt_token, user_id, user_name, user_email, user_password, user_first_name, user_last_name, user_phone, user_street1, user_street2, user_city, user_state, user_country, user_zip, user_status)

- **Parameters**
  ```
  "user_id": string,
  "user_name": string,
  "user_email": string,
  "user_password": string,
  "user_first_name": string,
  "user_last_name": string,
  "user_phone": string,
  "user_street1": string,
  "user_street2": string,
  "user_city": string,
  "user_state": string,
  "user_country": string,
  "user_zip": string,
  "user_status": string,
  ```

  `user_id` is required, while others are optional.

- **Returns**
  - 200 (default): successful operation
    ```
    {
      "code": "string",
      "body": {
        "user_id": "string",
        "user_name": "string",
        "user_email": "string",
        "user_password": "string",
        "user_detail": {
          "user_first_name": "string",
          "user_last_name": "string",
          "user_phone": "string",
          "user_street1": "string",
          "user_street2": "string",
          "user_city": "string",
          "user_state": "string",
          "user_country": "string",
          "user_zip": "string"
        },
        "user_status": "string",
        "user_thumbnail": "string",
        "user_follower": 0,
        "user_reg_date": "2020-12-02T20:46:49.404Z",
        "user_recent_login": [
          "string"
        ]
      }
    }
    ```
  - 400: invalid username supplied
  - 404: user not found
  - 405: method not allowed
  - 50x: internal server error

### User Delete
- **Function**
  - user_delete(jwt_token, user_id)

- **Parameters**
  ```
  "jwt_token": string,
  "user_id": string,
  ```

- **Returns**
  - 200 (default): successful operation
    ```
    "body": {
      "message": "Successfully deleted user"
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
video_aws | AWS update video status after transcoding and streaming | POST | /video/{video_id}

### Video Upload
- **Function**
  - video_upload (jwt_token)

- **Parameters**
  Name | Type | Description
    --- | --- | ---
    jwt_token | string | Verify which user is currently logged in

- **Returns**
  - (default) 200 (request accepted), return the ID of the video.

### Video Get
- **Function**
  - video_get(video_id)

- **Parameters**

  ```
  "video_id": A string to identify the video.
  ```

- **Returns**
  
  - 200 (default): successful operation
  ```
  {
    "video_id": "string",
    "user_id": "string",
    "video_title": "string",
    "video_raw_content": "string",
    "video_raw_status": "string",
    "video_raw_size": 0,
    "video_duration": 0,
    "video_channel": "string",
    "video_tag": [
      "string"
    ],
    "video_category": [
      "string"
    ],
    "video_description": "string",
    "video_language": "string",
    "video_status": "string",
    "video_view": 0,
    "video_comment": 0,
    "video_like": 0,
    "video_dislike": 0,
    "video_star": 0,
    "video_thumbnail": "string",
    "video_upload_date": "2020-12-02T21:06:32.485Z",
    "video_uri": {
      "video_low": "string",
      "video_mid": "string",
      "video_high": "string"
    }
  }
  ```

### Video Update
- **Function**
  - video_update (jwt_token, video_title, video_thumbnail, video_channel, video_tag, video_category, video_description, video_language, video_status)

- **Parameters**
  ```
  "video_title": string,
  "video_thumbnail": string,
  "video_channel": enum,
  "video_tag": string[],
  "video_category": string[],
  "video_description": string,
  "video_language": enum,
  "video_status": enum
  ```
- **Returns**
  - 200 (default): successful operation
    ```
    {
      "video_id": "string",
      "user_id": "string",
      "video_title": "string",
      "video_raw_content": "string",
      "video_raw_status": "string",
      "video_raw_size": 0,
      "video_duration": 0,
      "video_channel": "string",
      "video_tag": [
        "string"
      ],
      "video_category": [
        "string"
      ],
      "video_description": "string",
      "video_language": "string",
      "video_status": "string",
      "video_view": 0,
      "video_comment": 0,
      "video_like": 0,
      "video_dislike": 0,
      "video_star": 0,
      "video_thumbnail": "string",
      "video_upload_date": "2020-12-02T21:06:32.485Z",
      "video_uri": {
        "video_low": "string",
        "video_mid": "string",
        "video_high": "string"
      }
    }
    ```
  - 400: bad request
  - 405: method not allowed
  - 50x: internal server error

### AWS Update

- **Function**
  - aws_update (jwt_token, video_status)

- **Parameters**
  ```
  "video_status": enum
  ```
- **Returns**
  - 200 (default): successful operation
    ```
    {
      "video_id": "string",
      "user_id": "string",
      "video_title": "string",
      "video_raw_content": "string",
      "video_raw_status": "string",
      "video_raw_size": 0,
      "video_duration": 0,
      "video_channel": "string",
      "video_tag": [
        "string"
      ],
      "video_category": [
        "string"
      ],
      "video_description": "string",
      "video_language": "string",
      "video_status": "string",
      "video_view": 0,
      "video_comment": 0,
      "video_like": 0,
      "video_dislike": 0,
      "video_star": 0,
      "video_thumbnail": "string",
      "video_upload_date": "2020-12-02T21:06:32.485Z",
      "video_uri": {
        "video_low": "string",
        "video_mid": "string",
        "video_high": "string"
      }
    }
    ```
  - 400: bad request
  - 405: method not allowed
  - 50x: internal server error

### Video Delete
- **Function**
  - video_delete (jwt_token, video_id)

- **Parameters**
  ```
  "video_id": string
  ```
- **Returns**
  
  Need to check if user has permission to delete video. Returns:

  - HTTP response 200 (OK)
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
search_top_videos | Search top videos by keyword | GET | /search/video/top

### Search Video
- **Function**
  - search_video (keyword)
    - keyword (string): A string containing the search terms, can be video title, channels, tags, categories, etc.

- **Parameters**
  ```
  "keyword": string
  ```

- **Returns**
  - 200: successful operation
  - 400: bad request
  - 50x: internal server error

### Search User
- **Function**
  - search_user (keyword)
    - keyword (string): A string containing the search terms, can be user name, email, etc.

- **Parameters**
  ```
  "keyword": string
  ```
- **Returns**
  - 200: successful operation
  - 400: bad request
  - 50x: internal server error

### Search Top Videos
- **Function**
  - search_top_video (keyword)
    - keyword (string): A default string which specifies the top search result soring indicators. Defaultly set as "video_view".

- **Parameters**
  ```
  "keyword": string
  ```
- **Returns**
  - 200: successful operation
  - 400: bad request
  - 50x: internal server error

## Video Op

### Comment

Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
comment_post | Post video comment | POST | /video/{video_id}/comment/{user_id}
comment_list_by_video | Get comment list by video | GET | /video/{video_id}/comment
comment_get | Get specified comment by video and user | GET | /video/{video_id}/comment/{user_id}
comment_update | Update specified comment by video and user | PUT | /video/{video_id}/comment/{user_id}
comment_delete | Delete specified comment by video and user | DELETE | /video/{video_id}/comment/{user_id}

### Like

Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
like_post | Post video like | POST | /video/{video_id}/like/{user_id}
like_list_by_video | Get like list by video | GET | /video/{video_id}/like/
like_delete | Delete specified like by video and user | DELETE | /video/{video_id}/like/{user_id}

### Dislike

Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
dislike_post | Post video dislike | POST | /video/{video_id}/dislike/{user_id}
dislike_list_by_video | Get dislike list by video | GET | /video/{video_id}/dislike/
dislike_delete | Delete specified dislike by video and user | DELETE | /video/{video_id}/dislike/{user_id}

### Star

Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
star_post | Post video star by video and user | POST | /video/{video_id}/star/{user_id}
star_list_by_video | Get star list by video | GET | /video/{video_id}/star/
star_delete | Delete star by video and user | DELETE | /video/{video_id}/star/{user_id}

### Process

Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
process_create | Add a video to process list | POST | /user/{user_id}/process/{video_id}
process_update | Update a video's process | PUT | /user/{user_id}/process/{video_id}
process_get | Get process list by user id | GET | /user/{user_id}/process/
process_delete | Delete a video's process | DELETE | /user/{user_id}/process/{video_id}

### View

Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
view_add | Add video views by 1 | PUT | /video/{video_id}/view/
view_get | Get video views by 1 | GET | /video/{video_id}/view/
