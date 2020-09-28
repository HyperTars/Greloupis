# APIs Design
- [API Design](https://docs.google.com/spreadsheets/d/1hoKAh89rNywF343tU5lzeamFmidxdYJ39CW_uUCCRLw/edit?usp=sharing)

### User Auth
#### Overview
Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
user_create | Create user account | POST | /user
user_login | Logs user into the system | POST | /user/login
user_logout | Logs out current user session | DELETE | /user/logout
user_get | Get user by user name | GET | /user/{user_id}
user_update | Update user account | PUT | /user/{user_id}
user_delete | Delete user account | DELETE | /user/{user_id}

#### User Create
- **Function**
  - user_create()

- **Parameters**

- **Returns**

#### User Login
- **Function**
  - user_login()

- **Parameters**

- **Returns**

#### User Logout
- **Function**
  - user_logout()

- **Parameters**

- **Returns**

#### User Get
- **Function**
  - user_get()

- **Parameters**

- **Returns**

#### User Update
- **Function**
  - user_update()

- **Parameters**

- **Returns**

#### User Delete
- **Function**
  - user_delete()

- **Parameters**

- **Returns**

### Video
#### Overview
Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
video_upload | upload video | POST | /user/{user_id}/video
video_update | update video information | PUT | /user/{user_id}/video/{video_id}
video_delete | delete video | DELETE | /user/{user_id}/video/{video_id}
video_get | get video content cache | GET | /video/{video_id}

#### Video Upload
- **Function**
  - video_upload(api_key, title, ...)

- **Parameters**
  - Name | Type | Note
    --- | --- | ---
    apiKey | string | This will be used to, among other things, throttle users based on their allocated quota.
    videoTitle | string | video title
    videoDesc | string | (optional) video description
    videoTags | string[] | (optional) video tags
    videoCategory | string | category of video, e.g., Movie, Vlog, Song, News, Tech, etc.
    videoLanguage | string | e.g., English, Mandarin, Hindi, etc.
    videoStatus | string | e.g., public, private, limited share.
    videoContents | stream | video to be uploaded.

- **Returns**
  - (default) 202 (request accepted), once the video encoding is completed the user is notified through email with a link to access the video. We can also expose a queryable API to let users know the current status of their uploaded video.

#### Video Get
- **Function**
  - video_get(api_dev_key, video_id, offset, codec, resolution)

- **Parameters**
  - api_dev_key (string): The API developer key of a registered account of our service.
  video_id (string): A string to identify the video.
  offset (number): We should be able to stream video from any offset; this offset would be a time in seconds from the beginning of the video. If we support playing/pausing a video from multiple devices, we will need to store the offset on the server. This will enable the users to start watching a video on any device from the same point where they left off. codec (string) & resolution(string): We should send the codec andresolution info in the API from the client to support play/pause from multiple devices. Imagine you are watching a video on your TV’s Netflix
  app, paused it, and started watching it on your phone’s Netflix app. In this case, you would need codec and resolution, as both these devices have a different resolution and use a different codec.

- **Returns: (STREAM)**
  - A media stream (a video chunk) from the given offset.

#### Video Update
- **Function**
  - video_update ()

- **Parameters**

- **Returns**

#### Video Delete
- **Function**
  - video_delete (apiKey, videoID)

- **Parameters**

- **Returns**
  - Check if user has permission to delete video. It will return HTTP response 200 (OK), 202 (Accepted) if the action has been queued, or 204 (No Content) based on your response.



### Search
#### Overview
Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
search_video | Search video list by keyword | GET | /search/video
search_user | Search user list by keyword | GET | /search/user

#### Search Video
- **Function**
  - search_video (api_dev_key, search_query, user_location, maximum_videos_to_return, page_token)

- **Parameters**
  api_dev_key (string): The API developer key of a registered account of our service.
  search_query (string): A string containing the search terms. user_location (string): Optional location of the user performing the search.
  maximum_videos_to_return (number): Maximum number of results returned in one request.
  page_token (string): This token will specify a page in the result set that should be returned.

- **Returns**
  - A JSON containing information about the list of video resources matching the search query. Each video resource will have a video title, a thumbnail, a video creation date, and a view count.

#### Search User
- **Function**
  - search_user ()

- **Parameters**

- **Returns**

### Watch History
#### Overview
Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
history_create | Add a video to history list | POST | /user/{user_id}/history/{video_id}
history_update | Update history list | PUT | /user/{user_id}/history/{video_id}
history_get | Get history list by user id | GET | /user/{user_id}/history/
history_delete | Delete a video from history list | DELETE | /user/{user_id}/history/{video_id}

### Video Op
#### Overview
Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
rate_post | Post video rate | POST | /video/{video_id}/rate/{user_id}
rate_list_by_video | Get rate list by video | GET | /video/{video_id}/rate/
rate_list_by_user | Get rate list by user | GET | /user/{user_id}/rate/
rate_get | Get specified rate by video and user | GET | /video/{video_id}/rate/{user_id}
rate_update | Update specified rate by video and user | PUT | /video/{video_id}/rate/{user_id}
rate_delete | Delete specified rate by video and user | DELETE | /video/{video_id}/rate/{user_id}
  | | |  
review_post | Post video review | POST | /video/{video_id}/review/{user_id}
review_list_by_video | Get review list by video | GET | /video/{video_id}/review/
review_list_by_user | Get review list by user | GET | /user/{user_id}/review/
review_get | Get specified review by video and user | GET | /video/{video_id}/review/{user_id}
review_update | Update specified review by video and user | PUT | /video/{video_id}/review/{user_id}
review_delete | Delete specified review by video and user | DELETE | /video/{video_id}/review/{user_id}
  | | |
star_post | Post video star by video and user | POST | /video/{video_id}/star/{user_id}
star_count_by_video | Get star count by video | GET | /video/{video_id}/star/
star_list_by_user | Get star list by user | GET | /user/{user_id}/star/
star_delete | Delete star by video and user | DELETE | /video/{video_id}/star/{user_id}
  | | |
view_add | Add video views | PUT | /video/{video_id}/view/
view_get | Get video views | GET | /video/{video_id}/view/

### Follow
#### Overview
Function | Description | Type | Path (Endpoint)
--- | --- | --- | ---
follow | Follow an uploader | POST | /{user_id}`(follower)`/follow/{user_id}`(uploader)`
unfollow | Unfollow an uploader | DELETE | /{user_id}`(follower)`/follow/{user_id}`(uploader)`
following_list | Get all following uploader | GET | /{user_id}/follow/following
followers_list | Get all followers list | GET | /{user_id}/follow/followers



### (TBD) Recommendation
