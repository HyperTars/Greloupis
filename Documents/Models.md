# Models Design

### Basic Models
- **AddressDetails**
  - AVP Name | Type | Description
    --- | --- | ---
    `street1` | string | -
    `street2` | string | -
    `city` | string | -
    `state` | string | -
    `country` | string | -
    `zip` | string | -

- **LoginDetails**
  - AVP Name | type | Description
    --- | --- | ---
    `login_ip` | string | -
    `login_time` | date-type | -

- **VideoURI**
  - URI directed to Amazon S3 (storing video)
  - AVP Name | Type | Description
    --- | --- | ---
    `low` | string | URI of low quality video (480p)
    `mid` | string | URI of mid quality video (720p)
    `high` | string | URI of high quality video (1080p)

- **Thumbnail**
  - URI directed to Amazon S3 (storing thumbnail)
  - AVP Name | Type | Description
    --- | --- | ---
    `thumbnail_uri` | string | URI of video's thumbnail
    `thumbnail_type` | enum | (default auto, user specified, user upload)

### User Model
- **User**
  - AVP Name | Type | Description
    --- | --- | ---
    `user_id` | string | user's uniq ID (sys generated)
    `user_name` | string | user's nickname (requried)
    `first_name` | string | user's first name (required)
    `last_name` | string | user's last name (required)
    `email` | string | user's email (required)
    `password` | string | user's password (required, encrypted)
    `phone` | string | user's phone number (required)
    `address` | AddressDetails | user's address (optional)
    `user_status` | enum | user's account status (default public, private, closed)
    `reg_date` | date-type | user's registration date (sys generated)
    `recent_login` | LoginDetails[] | user's recent login details (sys generated)

- **Follow**
  - AVP Name | Type | Description
    --- | --- | ---
    `follower` | string | follower's user_id
    `followed` | string | user who is followed
    `follow_date` | date-type | date of following

### Video Model
- **Video**
  - AVP Name | Type | Description
    --- | --- | ---
    `video_id` | string | video's unique id (sys generated)
    `user_id` | string | user who uploads the video
    `video_title` | string | video title (required)
    `video_tags` | string[] | video tags (optional)
    `video_category` | string[] | video category, e.g., Movie, Vlog, Game, Technology, News, Song, etc. (required)
    `video_description` | string | video description (optional)
    `video_language` | string | e.g., English, Mandarin, Hindi, etc. (optional)
    `video_status` | enum | video status (default public, private, limited share, deleted)
    `video_contents` | stream | video uploading stream (sys generated)
    `video_content_status` | enum | content uploading & releasing status (default pending, processing, succeeded, failed, rejected)
    `video_size` | float | size of the video (sys generated)
    `video_views` | big int | count of video views (sys generated)
    `video_likes` | big int | count of video likes (sys generated)
    `video_dislikes` | big int | count of video dislikes (sys generated)
    `video_comments` | big int | count of video comments (sys generated)
    `video_stars` | big int | count of video stars (sys generated)
    `video_shares` | big int | count of video shares (sys generated)
    `video_thumbnail` | Thumbnail | video thumbnail (sys generated)
    `video_upload_date` | date-type | video upload date (sys generated)
    `video_uri` | VideoURI | uploaded video URI (sys generated)

### Video Op Model
- **Comment**
  - AVP Name | Type | Description
    --- | --- | ---
    `comment_id` | string | comment's unique id (sys generated)
    `user_id` | string | user's uniq id (required)
    `video_id` | string | video's unique id (required)
    `comment` | string | comment content (required)
    `comment_date` | date-type | comment date (sys generated)

- **Like**
  - AVP Name | Type | Description
    --- | --- | ---
    `like_id` | string | like's unique id (sys generated)
    `user_id` | string | user's uniq id (required)
    `video_id` | string | video's unique id (required)
    `comment_date` | date-type | like date (sys generated)

- **Dislike**
  - AVP Name | Type | Description
    --- | --- | ---
    `dislike_id` | string | dislike's unique id (sys generated)
    `user_id` | string | user's uniq id (required)
    `video_id` | string | video's unique id (required)
    `dislike_date` | date-type | like date (sys generated)

- **Star**
  - AVP Name | Type | Description
    --- | --- | ---
    `star_id` | string | star's unique id (sys generated)
    `user_id` | string | user's uniq id (required)
    `video_id` | string | video's unique id (required)
    `star_date` | date-type | star date (sys generated)

### Watch History Model
- **History**
  - AVP Name | Type | Description
    --- | --- | ---
    `user_id` | string | user's unique id
    `video_id` | string | video's unique id
    `process` | time | user watching process (last position)
    `hisoty_date` | date-type | history date