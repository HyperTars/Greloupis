# Database Design

- Database: MongoDB 4.4.0
- Database name: online_video_platform
- Database Endpoint: "mongodb+srv://devops:DevOps@mongodbcluster.v4vtj.mongodb.net/online_video_platform?retryWrites=true&w=majority"

## Table / Collection (MongoDB)

### Collection: user
- **Document**
    Attr1 | Type | Attr2 | Type | Data Source | Nullable | Description
    --- | --- | --- | --- | --- | --- | --- | --- | ---
    user_id / `_id` | ObjectId | - | - |MongoDB generate | NO | user's unique id
    user_email | String | - | - | user input | NO | user's email
    user_name | String | - | - | user input | NO | user's nick name
    user_password | String | - | - | user input | NO | user's password, encoded
    user_detail | Object | first_name | string | user input | NO | user's first name
     | | | last_name | String | user input | NO | user's last name
     | | | phone | String | user input | NO | user's phone number
     | | | street1 | string| usre input | YES | user's detail address
     | | | street2 | String|  user input | YES |
     | | | city | String|  user input | YES |
     | | | state | String|  user input | YES |
     | | | country | String|  user inpu | YES |
     | | | zip | String |  user input | YES |
    user_status | String | - | - | user input | NO | user's profile status (default public) 
    user_thumbnail | Object | thumbnail_uri | String | system generate | YES | user's thumbnail URI
     | | | thumbnail_type | String | user input | NO | default: system auto
    user_reg_date | Date | - | - | system generate | NO | user's registration date 
    user_recent_login | Array | `index` | (Object)<br>login_ip - String /<br>login_time - Date | user input /<br>system generate | NO | array of user's recent logins
    user_following | Array | `index` | String | user input | YES | array of following uploaders' ids
    user_follower | Array | `index` | String | system generated | YES | array of user's followers

- **Sample**
    ```json
    {
        "_id": {
            "$oid": "5f812ca71ded3bab106faa3a"
        },
        "user_email": "hypertars@gmail.com",
        "user_name": "hypertars",
        "user_password": "hypertars",
        "user_detail": {
            "first_name": "Brian",
            "last_name": "Lee",
            "phone": "+13474051241",
            "street1": "343 Gold St",
            "street2": "Apt 3810",
            "city": "Brooklyn",
            "state": "New York",
            "country": "United States",
            "zip": "11201"
        },
        "user_status": "public",
        "user_thumbnail": {
            "thumbnail_uri": "https://xxx.png",
            "thumbnail_type": "user_specified"
        },
        "user_reg_date": {
            "$date": {
                "$numberLong": "1601143002000"
            }
        },
        "user_recent_login": [{
            "login_ip": "8.8.8.8",
            "login_time": {
                "$date": {
                    "$numberLong": "1601195652000"
                }
            }
        }, {
            "login_ip": "4.4.4.4",
            "login_time": {
                "$date": {
                    "$numberLong": "1601323927000"
                }
            }
        }],
        "user_following": ["46a5sd465as4d56as4", "7asdas654das98da8as"],
        "user_follower": []
    }
    ```

    Sample2
    ```json
    {
        "_id": {
            "$oid": "5f812cda1ded3bab106faa3b"
        },
        "user_email": "xx.gmail.com",
        "user_name": "test_user",
        "user_password": "askdkj091",
        "user_detail": {
            "first_name": "test_user",
            "last_name": "test_user",
            "phone": "+1xxxxxx",
            "street1": "str1",
            "street2": "str2",
            "city": "cty",
            "state": "stt",
            "country": "ctry",
            "zip": "zip"
        },
        "user_status": "active",
        "user_thumbnail": {
            "thumbnail_uri": "test_uri",
            "thumbnail_type": "test_type"
        },
        "user_reg_date": {
            "$date": {
                "$numberLong": "1602166351000"
            }
        },
        "user_recent_login": [{
            "login_ip": "1.1.1.1",
            "login_time": {
                "$date": {
                    "$numberLong": "1602171008000"
                }
            }
        }],
        "user_following": ["kl12j3lk12j3l12k"],
        "user_follower": ["89889a7d98as789d", "1h312jj3h12kj312h"]
    }
    ```


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
    video_thumbnail | Object | thumbnail_uri | String | system generate | YES | thumbnail URI
     | | | thumbnail_type | String | user input | NO | auto, user_upload, first frame (default auto)
    video_upload_date | Date | - | - | system generate | NO | video upload date
    video_uri | Object | video_low | String | system generate | YES | 480p video URI
     | | | video_mid | String | system generate | YES | 720p video URI
     | | | video_high | String | system generate | YES | 1080p video URI

- **Sample**
    ```json
    {
        "_id": {
            "$oid": "5f812dc41ded3bab106faa3c"
        },
        "user_id": "5f808f79c2ac20387eb8f3c9",
        "video_title": "test film",
        "video_raw_content": "https://s3.amazon.com/test_film.mp4",
        "video_raw_status": "pending",
        "video_raw_size": {
            "$numberDouble": "0"
        },
        "video_tag": ["movie"],
        "video_category": ["funny", "action"],
        "video_description": "",
        "video_language": "",
        "video_status": "public",
        "video_view": {
            "$numberLong": "0"
        },
        "video_comment": {
            "$numberLong": "0"
        },
        "video_like": {
            "$numberLong": "0"
        },
        "video_dislike": {
            "$numberLong": "0"
        },
        "video_star": {
            "$numberLong": "0"
        },
        "video_share": {
            "$numberLong": "0"
        },
        "video_thumbnail": {
            "thumbnail_uri": "",
            "thumbnail_type": "default"
        },
        "video_upload_date": {
            "$date": {
                "$numberLong": "1602296420019"
            }
        },
        "video_uri": {
            "video_low": "",
            "video_mid": "",
            "video_high": ""
        }
    }
    ```
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

- **Sample**
    ```json
    {
        "_id": {
            "$oid": "5f812e0b1ded3bab106faa3d"
        },
        "user_id": "5f808f79c2ac20387eb8f3c9",
        "video_id": "5f72999541bc583c4819d915",
        "process": {
            "$numberInt": "142"
        },
        "comment": "Interesting.",
        "like": false,
        "dislike": false,
        "star": false,
        "process_date": {
            "$date": {
                "$numberLong": "1602298353872"
            }
        },
        "comment_date": {
            "$date": {
                "$numberLong": "1602298353872"
            }
        },
        "like_date": {
            "$date": {
                "$numberLong": "1602298353872"
            }
        },
        "dislike_date": {
            "$date": {
                "$numberLong": "1602298353872"
            }
        },
        "star_date": {
            "$date": {
                "$numberLong": "1602298353872"
            }
        }
    }
    ```


### Wasted Collection Samples (No Longer Used)
- **Sample: follow**
    ```json
    {
        "_id": {
            "$oid": "5f728e4541bc583c4819d911"
        },
        "follow_uploader": "5f72894b41bc583c4819d90b",
        "follow_by": "a1d56as4d56as1d32as",
        "follow_date": {
            "$date": {
                "$numberLong": "1601420162000"
            }
        }
    }
    ```

- **Sample: history**
    ```json
    {
        "_id": {
            "$oid": "5f7289e841bc583c4819d90c"
        },
        "user_id": "5f72894b41bc583c4819d90b",
        "video_id": "adasdasfasfas4d3a5s",
        "process": {
            "$numberInt": "59"
        },
        "history_date": {
            "$date": {
                "$numberLong": "1601342048000"
            }
        }
    }
    ```
