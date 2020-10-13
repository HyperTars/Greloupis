- [Test Cases](https://docs.google.com/spreadsheets/d/1hoKAh89rNywF343tU5lzeamFmidxdYJ39CW_uUCCRLw/edit?usp=sharing)

## Test Code

### Unit Test

#### test_models

- **User**
    - To test model, we use `user = User(**test_load_data)` to trans our data from json file to dict, then to Use Model, and validate the Model.
    - If succeed, we will get a User Model with valid data.
    
    - Test case:
        ```json
        [
            {
                "_id": {
                    "$oid": "5f84c6597a6a702235948b84"
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
            },
            {
                "user_name": "test_minimum_info",
                "user_email": "missing@gmail.com",
                "user_password": "minimum"
            }
        ]
        ```

- **Video**

- **VideoOp**

#### test_db
- **query_user**
    - To test database query, we designed a series of sentences to ensure the idempotence of each test result.
    - Usually, we store part of data in [data: query_user](../source/tests/test_data/query_user.json) as a json array

    #Case | Operation | Description | Param | Expectation | Code
    --- | --- | --- | --- | --- | ---
    #00 | PERMANENT | Permanent Document for idempotent testing | `user_name=hypertars` | Data in MongoDB | `data[0]`
    #01 | PERMANENT | Permanent Document for idempotent testing | `user_name=eclipse` | Data in MongoDB | `data[1]`
    #02 | PERMANENT | Permanent Document for idempotent testing | `user_name=milvus` | Data in MongoDB | `data[2]`
    #03 | CREATE | Create user with full param | `user_name`, `user_email`,<br>`user_password`, `user_ip` | return User object | 
    #04 | CREATE | Create user with part param | `user_name`, `user_email`,<br>`user_password` | return User object (auto ip=0.0.0.0) | `query_user_create("test2", "test2@email.com", "testpasscode2")`
    #05 | CREATE | Create user with insufficient param | return `TypeError: query_user_create() missing 1 required positional argument: 'user_password'` | `query_user_create("test3", "test2@email.com")`
    #06 | CREATE | Create user with taken user name conflict | `user_name`, `user_email`, `user_password` | return `ErrorCode.MONGODB_USER_NAME_TAKEN` | `query_user_create("test2", "test3@email.com", "testpasscode3", "34.172.45.33)`
    #07 | CREATE | Create user with taken user email conflict | `user_name`, `user_email`, `user_password` | return `ErrorCode.MONGODB_USER_EMAIL_TAKEN` | `query_user_create("test3", "test2@email.com", "testpasscode4", "218.85.157.99)`
    #08 | CREATE | Create user with full param | `user_name`, `user_email`,<br>`user_password`, `user_ip` | return User object | `query_user_create("test3", "test3@email.com", "testpasscode3", "34.172.45.33)`
    #09 | CREATE | Create user with full param | `user_name`, `user_email`,<br>`user_password`, `user_ip` | return User object | `query_user_create("test4", "test4@email.com", "testpasscode4", "218.85.157.99)`
    #00 | RETRIEVE | 
    #00 | RETRIEVE |
    #10 | Update | Add user login | `query_user_add_login("5f80bef29342f187a0fa2d70", ip="127.0.1.1")`
    #11 | Update | Add user login (trigger clean when up to 10) | `query_user_add_login("5f80bef29342f187a0fa2d70", ip="127.0.1.1")`
    #12 | Update | Add user following | `query_user_add_follow("5f80bef29342f187a0fa2d70", "5f808f045e03b2165ca4275a")`
    #13 | Update | Delete user following | `query_user_delete_follow("5f80bef29342f187a0fa2d70", "5f808f045e03b2165ca4275a")`
    #14 | Update | Update user name with conflict name | `query_user_update_name("5f80bef29342f187a0fa2d70", "test4")`
    #15 | Update | Update user name as current conflict | `query_user_update_name("5f80bef29342f187a0fa2d70", "test2")`
    #16 | Update | Update user name successfully | `query_user_update_name("5f80bef29342f187a0fa2d70", "test1")`
    #17 | Update | Update user name (update back) | `query_user_update_name("5f80bef29342f187a0fa2d70", "test2")`
    #18 | Update | Update user password as current conflict | `query_user_update_password("5f80bef29342f187a0fa2d70", "testpasscode")`
    #19 | Update | Update user password successfully | `query_user_update_password("5f80bef29342f187a0fa2d70", "testpasscode")`
    #20 | Update | Update user password (update back) | `query_user_update_password("5f80bef29342f187a0fa2d70", "testpasscode")`
    #21 | Update | Update user thumbnail with supported type: `['default', 'user', 'system']` | `user_id`, `user_thumbnail_uri`, `user_thumbnail_type` | return 1 | `query_user_update_thumbnail("#TODO", user_thumbnail_uri="s3.amazon.com/aidjasjds",user_thumbnail_type="default")`
    #22 | Update | Update user thumbnail with invalid type | `user_id`, `user_thumbnail_uri`, `user_thumbnail_type` | return `ErrorCode.MONGODB_INVALID_THUMBNAIL` | `query_user_update_thumbnail("#TODO", user_thumbnail_uri="s3.amazon.com/aidjasjds",user_thumbnail_type="origin")`
    #23 | Update | Update user detail | `query_user_update_details("5f808f79c2ac20387eb8f3c9", user_first_name="fffff", user_last_name="kkk",user_phone="+1313123123", user_zip="11201")`
    #24 | Update | Update user status with invalid status | `query_user_update_status("5f808f79c2ac20387eb8f3c9", "active")`
    #25 | Update | Update user with supported status `["public", "private", "closed"]` | `query_user_update_status("5f808f79c2ac20387eb8f3c9", "public")`
    #26 | Update | Update user with supported status (update back) | `query_user_update_status("5f808f79c2ac20387eb8f3c9", "private")`
    #27 | SEARCH | Search user id with contains
    #28 | SEARCH | Search user name with contains
    #29 | SEARCH | Search user email with contains
    #30 | SEARCH | Search user first name with contains
    #31 | SEARCH | Search user last name with contains
    #32 | SEARCH | Search user phone with contains
    #33 | SEARCH | Search user street1 with contains
    #34 | SEARCH | Search user street2 with contains
    #35 | SEARCH | Search user city with contains
    #36 | SEARCH | Search user state with contains
    #37 | SEARCH | Search user country with contains
    #38 | SEARCH | Search user zip with contains
    #39 | SEARCH | Search user status with contains
    #40 | SEARCH | Search user with contains, invalid str type
    #41 | SEARCH | Search user with contains, invalid param
    #42 | SEARCH | Search user name with pattern
    #43 | SEARCH | Search user email with pattern
    #44 | SEARCH | Search user first name with pattern
    #45 | SEARCH | Search user last name with pattern
    #46 | SEARCH | Search user phone with pattern
    #47 | SEARCH | Search user street1 with pattern
    #48 | SEARCH | Search user street2 with pattern
    #49 | SEARCH | Search user city with pattern
    #50 | SEARCH | Search user state with pattern
    #51 | SEARCH | Search user country with pattern
    #52 | SEARCH | Search user zip with pattern
    #53 | SEARCH | Search user status with pattern
    #54 | SEARCH | Search user reg date with pattern
    #55 | SEARCH | Search user with pattern, invalid pattern type
    #56 | SEARCH | Search user with pattern, invalid param
    #57 | SEARCH | Search user with aggregation
    
    
- **query_video**

    #Case | Operation | Description | Param | Expectation | Code
    --- | --- | --- | --- | --- | ---
    #0 | CREATE | `query_video_op_create("5f808f79c2ac20387eb8f3c9", "5f72999541bc583c4819d915")`
    #0 | RETRIEVE | `query_video_op_get_by_user_id("5f808f79c2ac20387eb8f3c9")`
    #0 | RETRIEVE | `query_video_op_get_by_video_id("5f72999541bc583c4819d915")`
    #0 | RETRIEVE | `query_video_op_get_by_user_video("5f808f79c2ac20387eb8f3c9", "5f72999541bc583c4819d915")`
    #0 | RETRIEVE | `query_video_op_get_by_op_id("5f80fd775490b2aef73d6315")`
    #0 | UPDATE | `query_video_op_update_process("5f80fd775490b2aef73d6315", 142)`
    #0 | UPDATE | `query_video_op_update_comment("5f80fd775490b2aef73d6315", "Interesting.")`
    #0 | UPDATE | `query_video_op_update_like("5f80fd775490b2aef73d6315", True)`
    #0 | UPDATE | `query_video_op_update_dislike("5f80fd775490b2aef73d6315", True)`
    #0 | UPDATE | `query_video_op_update_star("5f80fd775490b2aef73d6315", True)`
    #0 | UPDATE | `query_video_op_update_like("5f80fd775490b2aef73d6315", False)`
    #0 | UPDATE | `query_video_op_update_dislike("5f80fd775490b2aef73d6315", False)`
    #0 | UPDATE | `query_video_op_update_star("5f80fd775490b2aef73d6315", False)`
    #0 | DELETE | ``

- **query_video_op**

    #Case | Operation | Description | Param | Expectation | Code
    --- | --- | --- | --- | --- | ---
    #0 | CREATE | `query_video_create("5f808f79c2ac20387eb8f3c9", "test video", "https://s3.amazon.com/test_video.mp4")`
    #0 | CREATE | `query_video_create("5f808f79c2ac20387eb8f3c9", "test film", "https://s3.amazon.com/test_film.mp4", video_tag=['movie'], video_category=['funny', 'action'])`
    #0 | RETRIEVE | `query_video_get_by_title("XiXiHaHa")[0].to_dict()`
    #0 | RETRIEVE | `query_video_get_by_id("5f72999541bc583c4819d915")[0].to_dict()`
    #0 | UPDATE | `query_video_update("5f72999541bc583c4819d915", video_uri_low="https://s3.amazon.com/test_low_quality.mp4")`
    #0 | UPDATE | `query_video_cnt_incr_by_one("5f72999541bc583c4819d915", "view")`
    #0 | UPDATE | `query_video_cnt_incr_by_one("5f72999541bc583c4819d915", "comments")`
    #0 | UPDATE | `query_video_cnt_incr_by_one("5f72999541bc583c4819d915", "likes")`
    #0 | UPDATE | `query_video_cnt_incr_by_one("5f72999541bc583c4819d915", "video_dislike")`
    #0 | UPDATE | `query_video_cnt_incr_by_one("5f72999541bc583c4819d915", "video_star")`
    #0 | UPDATE | `query_video_cnt_incr_by_one("5f72999541bc583c4819d915", "share")`
    #0 | UPDATE | `query_video_cnt_decr_by_one("5f72999541bc583c4819d915", "video_star")`
    #0 | UPDATE | decr stop at zero |`query_video_cnt_decr_by_one("5f72999541bc583c4819d915", "video_star")`
    #0 | DELETE | `query_video_delete("5f810903cd3d45e0e5989891")`
    
#### test_service
- **service_search**

    #Case | Operation | Description | Param | Expectation | Code
    --- | --- | --- | --- | --- | ---
    #0 | Search user by contains | 
    #0 | Search user by contains | 
    #0 | Search user by pattern | 
    #0 | Search user by pattern | 
    #0 | Search user by aggregate | 
    #0 | Search user by aggregate | 
    #0 | Search video by contains | 
    #0 | Search video by contains | 
    #0 | Search video by pattern custom| 
    #0 | Search video by pattern slice | 
    #0 | Search video by pattern case sensitive | 
    #0 | Search video by pattern exact | 
    #0 | Search video by aggregate | 
    #0 | Search video by aggregate | 
    
#### test_route