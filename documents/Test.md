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

- **query_video**

- **query_video_op**

#### test_service
- **service_search**

#### test_route