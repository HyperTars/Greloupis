[![logo](greloupis-horizontal.png)](https://greloupis-frontend.herokuapp.com/)

# Database Design

- Database: MongoDB 4.4.0
- Database name: greloupis

## Table / Collection (MongoDB)

### Collection: user
- **Document**

    Attr1 | Type | Attr2 | Type | Data Source | Nullable | Description
    --- | --- | --- | --- | --- | --- | ---
    user_id / `_id` | ObjectId | - | - |MongoDB generate | NO | user's unique id
    user_email | String | - | - | user input | NO | user's email
    user_name | String | - | - | user input | NO | user's nick name
    user_password | String | - | - | user input | NO | user's password, encoded
    user_detail | Object | user_first_name | string | user input | NO | user's first name
     | | | user_last_name | String | user input | NO | user's last name
     | | | user_phone | String | user input | NO | user's phone number
     | | | user_street1 | string| usre input | YES | user's detail address
     | | | user_street2 | String|  user input | YES | user's detail address
     | | | user_city | String|  user input | YES |  user's detail address
     | | | user_state | String|  user input | YES | user's detail address
     | | | user_country | String|  user inpu | YES | user's detail address
     | | | user_zip | String |  user input | YES | user's detail address
    user_status | String | - | - | user input | NO | user's profile status (default public) 
    user_thumbnail | String | - | - | system generate | YES | user's thumbnail URI
    user_reg_date | Date | - | - | system generate | NO | user's registration date 
    user_login | Array | `index` | (Object)<br>user_login_ip - String /<br>user_login_time - Date | user input /<br>system generate | NO | array of user's recent logins
    user_following | Array | `index` | String | user input | YES | array of following uploaders' ids
    user_follower | Array | `index` | String | system generated | YES | array of user's followers

- **Model Design**
    - [User Model](../backend/models/model_user.py)

- **Sample**
    - [User Sample - Constant](../backend/tests/test_data/const_user.json)
    - [User Sample - Temporary](../backend/tests/test_data/temp_user.json)


### Collection: video
- **Document**

    Attr1 | Type | Attr2 | Type | Data Source | Nullable | Description
    --- | --- | --- | --- | --- | --- | ---
    video_id / `_id` | ObjectId | - | - | Mongo generate | NO | video's unique id
    user_id | String | - | - | user input | NO | uploader's user id
    video_title | String | - | - | user input | NO | video's title
    video_raw_content | String | - | - | system generate | YES | upload raw video address (temp storage space, to be transcoded)
    video_raw_status | String | - | - | system generate | YES | default pending
    video_raw_size | Double | - | - | system generate | YES | video size in MB
    video_duration | Int | - | - | system generate | YES | video duration in second
    video_channel | String | - | - | user input | YES | video's channel, default: user-made
    video_tag | Array | `index` | String | user input | YES | array of video's tags
    video_category | Array | `index` | String | user input | YES | array of video's categories
    video_description | String | - | - | user input | YES | video's description
    video_language | String | - | - | user input | YES | video's language
    video_status | String | - | - | user input | NO | default public, private, deleted
    video_view | Int64 | - | - | system generate | NO | count of video views (default 0)
    video_comment | Int64 | - | - | system generate | NO | count of video comments (default 0)
    video_like | Int64 | - | - | system generate | NO | count of video likes (default 0)
    video_dislike | Int64 | - | - | system generate | NO | count of video dislikes (default 0)
    video_star | Int64 | - | - | system generate | NO | count of video stars (default 0)
    video_share | Int64 | - | - | system generate | NO | count of video shares (default 0)
    video_thumbnail | String | - | - | system generate | YES | thumbnail URI
    video_upload_date | Date | - | - | system generate | NO | video upload date
    video_uri | Object | video_low | String | system generate | YES | 480p video URI
     | | | video_uri_mid | String | system generate | YES | 720p video URI
     | | | video_uri_high | String | system generate | YES | 1080p video URI

- **Model Design**
    - [Video Model](../backend/models/model_video.py)
    
- **Sample**
    - [Video Sample - Const](../backend/tests/test_data/const_video.json)
    - [Video Sample - Temp](../backend/tests/test_data/temp_video.json)
    
### Collection: video_op (including watch history, comment, like, dislike, star)
- **Document**

    Attr | Type | Data Source | Nullable | Description
    --- | --- | --- | --- | ---
    video_op_id / `_id` | ObjectId | Mongo Generate | NO | video_op's unique id (user-video)
    user_id | String | user input | NO | user's id
    video_id | String | user input | NO | video's id
    process | Int32 | user input | YES | latest watch process (in second, default 0)
    comment | String | user input | YES | comment content, default NULL (inactive)
    like | Boolean | user input | NO | default false (inactive)
    dislike | Boolean | user input | NO | default false (inactive)
    star | Boolean | user input | NO | default false (inactive)
    process_date | Date | system generate | YES | latest watching process date
    comment_date | Date | system generate | YES | comment date
    like_date | Date | system generate | YES | like date
    dislike_date | Date | system generate | YES | dislike date
    star_date | Date | system generate | YES | star date

- **Model Design**
    - [VideoOp Model](../backend/models/model_video_op.py)
    
- **Sample**
    - [VideoOp Sample - Const](../backend/tests/test_data/const_video_op.json)
    - [VideoOp Sample - Temp](../backend/tests/test_data/temp_video_op.json)

