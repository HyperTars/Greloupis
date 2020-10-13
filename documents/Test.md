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
    #00 | Permanent | Permanent Document for idempotent testing | `user_name=hypertars` | Data in MongoDB | `data[0]`
    #01 | Permanent | Permanent Document for idempotent testing | `user_name=eclipse` | Data in MongoDB | `data[1]`
    #02 | Permanent | Permanent Document for idempotent testing | `user_name=milvus` | Data in MongoDB | `data[2]`
    #03 | Create | Create user with full param | `user_name`, `user_email`,<br>`user_password`, `user_ip` | return User object | 
    #04 | Create | Create user with part param | `user_name`, `user_email`,<br>`user_password` | return User object (auto ip=0.0.0.0) | `query_user_create("test2", "test2@email.com", "testpasscode2")`
    #05 | Create | Create user with insufficient param | return `TypeError: query_user_create() missing 1 required positional argument: 'user_password'` | `query_user_create("test3", "test2@email.com")`
    #06 | Create | Create user with taken user name conflict | `user_name`, `user_email`, `user_password` | return `ErrorCode.MONGODB_USER_NAME_TAKEN` | `query_user_create("test2", "test3@email.com", "testpasscode3", "34.172.45.33)`
    #07 | Create | Create user with taken user email conflict | `user_name`, `user_email`, `user_password` | return `ErrorCode.MONGODB_USER_EMAIL_TAKEN` | `query_user_create("test3", "test2@email.com", "testpasscode4", "218.85.157.99)`
    #08 | Create | Create user with full param | `user_name`, `user_email`,<br>`user_password`, `user_ip` | return User object | `query_user_create("test3", "test3@email.com", "testpasscode3", "34.172.45.33)`
    #09 | Create | Create user with full param | `user_name`, `user_email`,<br>`user_password`, `user_ip` | return User object | `query_user_create("test4", "test4@email.com", "testpasscode4", "218.85.157.99)`
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
    #27 | Search | Search user id with contains
    #28 | Search | Search user name with contains
    #29 | Search | Search user email with contains
    #30 | Search | Search user first name with contains
    #31 | Search | Search user last name with contains
    #32 | Search | Search user phone with contains
    #33 | Search | Search user street1 with contains
    #34 | Search | Search user street2 with contains
    #35 | Search | Search user city with contains
    #36 | Search | Search user state with contains
    #37 | Search | Search user country with contains
    #38 | Search | Search user zip with contains
    #39 | Search | Search user status with contains
    #40 | Search | Search user with contains, invalid str type
    #41 | Search | Search user with contains, invalid param
    #42 | Search | Search user name with pattern
    #43 | Search | Search user email with pattern
    #44 | Search | Search user first name with pattern
    #45 | Search | Search user last name with pattern
    #46 | Search | Search user phone with pattern
    #47 | Search | Search user street1 with pattern
    #48 | Search | Search user street2 with pattern
    #49 | Search | Search user city with pattern
    #50 | Search | Search user state with pattern
    #51 | Search | Search user country with pattern
    #52 | Search | Search user zip with pattern
    #53 | Search | Search user status with pattern
    #54 | Search | Search user reg date with pattern
    #55 | Search | Search user with pattern, invalid pattern type
    #56 | Search | Search user with pattern, invalid param
    #57 | Search | Search user with aggregation
    
    
- **query_video**
    #Case | Operation | Description | Param | Expectation | Code
    --- | --- | --- | --- | --- | ---
    
- **query_video_op**
    #Case | Operation | Description | Param | Expectation | Code
    --- | --- | --- | --- | --- | ---
    
#### test_service
- **service_search**
    #Case | Operation | Description | Param | Expectation | Code
    --- | --- | --- | --- | --- | ---
    # | Search user by contains | 
    # | Search user by contains | 
    # | Search user by pattern | 
    # | Search user by pattern | 
    # | Search user by aggregate | 
    # | Search user by aggregate | 
    # | Search video by contains | 
    # | Search video by contains | 
    # | Search video by pattern custom| 
    # | Search video by pattern slice | 
    # | Search video by pattern case sensitive | 
    # | Search video by pattern exact | 
    # | Search video by aggregate | 
    # | Search video by aggregate | 
    
#### test_route