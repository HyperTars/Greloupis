# Database Design

- Database: MongoDB 4.4.0
- Database name: online_video_platform
- Database Endpoint: "mongodb+srv://devops:DevOps@mongodbcluster.v4vtj.mongodb.net/online_video_platform?retryWrites=true&w=majority"

## Table / Collection (MongoDB)

### Collection: user
- **Document**
    Attr1 | Type | Attr2 | Type | Attr3 | Type | Data Source | Nullable | Description
    --- | --- | --- | --- | --- | --- | --- | --- | ---
    user_id / `_id` | ObjectId | - | - | - | - | Mongo generate | NO | user's unique id
    user_email | String | - | - | - | - |  user input | NO | user's email
    user_name | String | - | - | - | - | user input | NO | user's nick name
    user_password | String | - | - | - | - | user input | NO | user's password, encoded
    user_detail | Object | first_name | string | - | - | user input | NO | user's first name
     | | | last_name | String | - | - | user input | NO | user's last name
     | | | phone | String | - | - | user input | NO | user's phone number
     | | | address | Object | street1 | string | usre input | YES | user's detail address
     | | | | | street2 | String | user input | YES |
     | | | | | city | String | user input | YES |
     | | | | | state | String | user input | YES |
     | | | | | country | String | user inpu | YES |
     | | | | | zip | String | user input | YES |
    user_status | String | - | - | - | - | user input | NO | user's profile status (default public) 
    user_thumbnail | Object | thumbnail_uri | String | - | - | system generate | YES | user's thumbnail URI
     | | | thumbnail_type | String | - | - | user input | NO | default: system auto
    user_reg_date | Date | - | - | - | - | system generate | NO | user's registration date 
    user_recent_login | Array | `index` | Object | login_ip | String | user input | NO |
     | | | | | login_time | Date | - | - | system generate | NO | 
    user_following | Array | `index` | String | - | - | user input | YES | array of following uploaders' ids
    user_follower | Array | `index` | String | - | - | system generated | YES | array of user's followers

- **Sample**
    ```json
    {
        "_id": {
            "$oid": "5f72894b41bc583c4819d90b"
        },
        "user_email": "hypertars@gmail.com",
        "user_name": "hypertars",
        "user_password": "hypertars",
        "user_detail": {
            "first_name": "Brian",
            "last_name": "Lee",
            "phone": "+13474051241",
            "address": {
                "street1": "343 Gold St",
                "street2": "Apt 3810",
                "city": "Brooklyn",
                "state": "New York",
                "country": "United States",
                "zip": "11201"
            }
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


### Collection: video
- **Document**

- **Sample**

### Collection: video_op (including watch history, comment, like, dislike, star)
- **Document**
    Attr | Type | Data Source | Nullable | Description
    --- | --- | --- | --- | ---
    video_op_id / `_id` | ObjectId | Mongo Generate | NO | video_op's unique id (user-video)
    user_id | String | user input | NO | user's id
    video_id | String | user input | NO | video's id
    process | Int32 | user input | YES | latest watch process (in second)
    comment | String | user input | YES | comment content, default NULL (inactive)
    like | Boolean | user input | NO | default false (inactive)
    dislike | Boolean | user input | NO | default false (inactive)
    star | Boolean | user input | NO | default false (inactive)
    history_date | Date | system generate | YES | latest watch history date
    comment_date | Date | system generate | YES | comment date
    like_date | Date | system generate | YES | like date
    dislike_date | Date | system generate | YES | dislike date
    star_date | Date | system generate | YES | star date

- **Sample**
    ```json
    {
        "_id": {
            "$oid": "5f72921641bc583c4819d912"
        },
        "user_id": "5f72894b41bc583c4819d90b",
        "video_id": "4a5s6d4as56d5a64sd56a4d",
        "process": {
            "$numberInt": "59"
        },
        "comment": "Very interesting.",
        "like": false,
        "dislike": true,
        "star": true,
        "history_date": {
            "$date": {
                "$numberLong": "1601477078000"
            }
        },
        "comment_date": {
            "$date": {
                "$numberLong": "1601407862000"
            }
        },
        "like_date": {
            "$date": {
                "$numberLong": "0"
            }
        },
        "dislike_date": {
            "$date": {
                "$numberLong": "1601422364000"
            }
        },
        "star_date": {
            "$date": {
                "$numberLong": "1601421798000"
            }
        }
    }
    ```


### Wasted Collection Samples
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