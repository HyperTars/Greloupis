# Models Design

## Basic Models
- **UserDetail**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `user_first_name` | string | user's first name | user input
    `user_last_name` | string | user's last name | user input
    `user_phone` | string | user's phone number | user input
    `user_street1` | string | street | user input
    `user_street2` | string | apartment, suite, building, floor, etc. | user input
    `user_city` | string | city | user input
    `user_state` | string | state | user input
    `user_country` | string | country | user input
    `user_zip` | string | zip code | user input

- **LoginDetail**
    AVP Name | type | Description | Data Source
    --- | --- | --- | ---
    `user_login_ip` | string | last login ip address | system generate
    `user_login_time` | date-type | last login timestamp | system generate

- **VideoURI**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `video_low` | string | URI of low quality video (540p) | system generate
    `video_mid` | string | URI of mid quality video (720p) | system generate
    `video_high` | string | URI of high quality video (1080p) | system generate
  - URI directed to CloudFront streaming

## User Models
- **User**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `user_id` | string | user's uniq ID | system generate
    `user_name` | string | user's nickname | user input
    `user_email` | string | user's email | user input
    `user_password` | string | user's password (encrypted) | user input
    `user_detail` | UserDetail | user's personal information in detail | user input
    `user_status` | enum | user's account status<br>(e.g., public, private, closed) | default
    `user_thumbnail` | string | user's thumbnail URL on S3 | default
    `user_following` | string[] | list of user's following users | system generated
    `user_follower` | string[] | list of user's followers | system generated
    `user_reg_date` | date-type | user's registration date | system generated
    `user_login` | LoginDetail[] | array of user's recent login details | system generated

## Video Models
- **Video**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `video_id` | string | video's unique id | system generated
    `user_id` | string | user who uploads the video | system generated
    `video_title` | string | video title | user input
    `video_raw_content` | string | uploaded video storing URL on S3  | system generated
    `video_raw_status` | enum | content uploading & releasing status<br>(e.g., pending, processing, streaming) | system generated
    `video_raw_size` | float | size of the video | system generated
    `video_duration` | int | duration of video in second | system generated
    `video_channel` | enum | channel of video, default self-made | user input
    `video_tag` | string[] | array of video tags | user input
    `video_category` | string[] | array of video category<br>(e.g., Movie, Vlog, Game, Technology, News, Song, etc.) | user input
    `video_description` | string | video description | user input
    `video_language` | enum | video language<br>(e.g., English, Mandarin, Hindi, etc.) | user input
    `video_status` | enum | video status<br>(e.g., public, private, deleted) | default
    `video_view` | big int | count of video views | system generated
    `video_comment` | big int | count of video comments | system generated
    `video_like` | big int | count of video likes | system generated
    `video_dislike` | big int | count of video dislikes | system generated
    `video_star` | big int | count of video stars | system generated
    `video_share` | big int | count of video shares | system generated
    `video_thumbnail` | string | video thumbnail URL, under AWS S3 | system generated
    `video_upload_date` | date-type | video upload date | system generated
    `video_uri` | VideoURI | uploaded video URI | system generated

- **Video Op**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `user_id` | string | user's uniq id (indexed) | system generated
    `video_id` | string | video's unique id (indexed) | system generated
    `comment` | string | comment content | user input
    `comment_date` | date-type | comment date | system generated
    `like` | boolean | whether like or not | system generated
    `like_date` | date-type | like date | system generated
    `dislike` | boolean | whether dislike or not | system generated
    `dislike_date` | date-type | dislike date | system generated
    `star` | boolean | whether star or not | system generated
    `star_date` | date-type | star date | system generated
    `process` | big int | user's video watching process | system generated
    `process_date` | date-type | last watching date | system generated
