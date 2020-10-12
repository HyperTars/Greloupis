# Models Design
see our [latest online document - sheet: Models](https://docs.google.com/spreadsheets/d/1hoKAh89rNywF343tU5lzeamFmidxdYJ39CW_uUCCRLw/edit?usp=sharing)

## Basic Models
- **AddressDetail**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `street1` | string | street | user input
    `street2` | string | apartment, suite, building, floor, etc. | user input
    `city` | string | city | user input
    `state` | string | state | user input
    `country` | string | country | user input
    `zip` | string | zip code | user input

- **UserDetail**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `first_name` | string | user's first name | user input
    `last_name` | string | user's last name | user input
    `phone` | string | user's phone number | user input
    `address` | AddressDetail | user's address | user input

- **LoginDetail**
    AVP Name | type | Description | Data Source
    --- | --- | --- | ---
    `login_ip` | string | last login ip address | system generate
    `login_time` | date-type | last login timestamp | system generate

- **VideoURI**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `video_low` | string | URI of low quality video (480p) | system generate
    `video_mid` | string | URI of mid quality video (720p) | system generate
    `video_high` | string | URI of high quality video (1080p) | system generate
  - URI directed to Amazon S3 (storing video)

- **Thumbnail**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `thumbnail_uri` | string | URI of video's or user's thumbnail | system generate
    `thumbnail_type` | enum | thumbnail source<br>(e.g., system default, user upload, auto first frame) | default
    - URI directed to Amazon S3 (storing thumbnail)

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
    `user_thumbnail` | Thumbnail | user's thumbnail | default
    `user_follower` | big int | count of user's followers | system generated
    `user_reg_date` | date-type | user's registration date | system generated
    `user_recent_login` | LoginDetail[] | array of user's recent login details | system generated

- **Follow**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `follow_uploader` | string | user who is followed | api dev key
    `follow_by` | string | follower's user_id | api dev key
    `follow_date` | date-type | date of following | system generate

## Video Models
- **Video**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `video_id` | string | video's unique id | system generated
    `user_id` | string | user who uploads the video | api dev key
    `video_title` | string | video title | user input
    `video_raw_content` | stream | video uploading stream | system generated
    `video_raw_status` | enum | content uploading & releasing status<br>(e.g., pending, processing, succeeded, failed, rejected) | system generated
    `video_raw_size` | float | size of the video | system generated
    `video_duration` | int | duration of video in second | system generated
    `video_channel` | string | channel of video, default self-made
    `video_tag` | string[] | array of video tags | user input
    `video_category` | string[] | array of video category<br>(e.g., Movie, Vlog, Game, Technology, News, Song, etc.) | user input
    `video_description` | string | video description | user input
    `video_language` | enum | video language<br>(e.g., English, Mandarin, Hindi, etc.) | user input
    `video_status` | enum | video status<br>(e.g., public, private, limited share, deleted) | default
    `video_view` | big int | count of video views | system generated
    `video_comment` | big int | count of video comments | system generated
    `video_like` | big int | count of video likes | system generated
    `video_dislike` | big int | count of video dislikes | system generated
    `video_star` | big int | count of video stars | system generated
    `video_share` | big int | count of video shares | system generated
    `video_thumbnail` | Thumbnail | video thumbnail | system generated
    `video_upload_date` | date-type | video upload date | system generated
    `video_uri` | VideoURI | uploaded video URI | system generated

- **Comment**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `comment_id` | string | comment's unique id | system generated
    `user_id` | string | user's uniq id (indexed) | api dev key
    `video_id` | string | video's unique id (indexed) | api dev key
    `comment` | string | comment content | user input
    `comment_date` | date-type | comment date | system generated

- **Like**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | --- 
    `like_id` | string | like's unique id | system generated
    `user_id` | string | user's uniq id (indexed) | api dev key
    `video_id` | string | video's unique id (indexed) | api dev key
    `like_date` | date-type | like date | system generated

- **Dislike**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `dislike_id` | string | dislike's unique id | system generated
    `user_id` | string | user's uniq id (indexed) | api dev key
    `video_id` | string | video's unique id (indexed) | api dev key
    `dislike_date` | date-type | dislike date | system generated

- **Star**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `star_id` | string | star's unique id | system generated
    `user_id` | string | user's uniq id (indexed) | api dev key
    `video_id` | string | video's unique id (indexed) | api dev key
    `star_date` | date-type | star date | system generated

- **History**
    AVP Name | Type | Description | Data Source
    --- | --- | --- | ---
    `history_id` | string | history's unique id | system generated
    `user_id` | string | user's uniq id (indexed) | api dev key
    `video_id` | string | video's unique id (indexed) | api dev key
    `process` | time | user watching process (player's last position) | api dev key
    `history_date` | date-type | history date | system generated