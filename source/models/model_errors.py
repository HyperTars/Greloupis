from flask_mongoengine import MongoEngine
from enum import Enum, unique
import datetime

db = MongoEngine()


# Error Model
class Error(db.Document):
    call = db.DictField(required=True)
    response = db.DictField(required=True)
    date = db.DateTimeField(default=datetime.datetime.now(), required=True)


class ErrorCode(Enum):
    # Routes 2 Series
    ROUTE_INVALID_REQUEST_PARAM = {"2001": "Route Error: Invalid Request Parameters"}

    # Service 3 Series
    SERVICE_PARAM_SLICE_NOT_SUPPORT = {"3001": "Service Error: Current Param Does Not Support Slice"}
    SERVICE_PATTERN_SEARCH_NOT_SUPPORT = {"3002": "Service Error: Current Param Does Not Support Pattern Search"}
    SERVICE_MISSING_PARAM = {"3003": "Service Error: Missing Essential Param"}

    # Database 4 Series
    MONGODB_CONNECTION_FAILURE = {"4000": "MongoDB Connection Failure"}
    MONGODB_USER_NOT_FOUND = {"4101": "MongoDB Error: User Not Found"}
    MONGODB_VIDEO_NOT_FOUND = {"4102": "MongoDB Error: Video Not Found"}
    MONGODB_VIDEOOP_NOT_FOUND = {"4103": "MongoDB Error: VideoOp Not Found"}
    MONGODB_USER_NAME_TAKEN = {"4104": "MongoDB Error: User Name Already Taken"}
    MONGODB_VIDEO_TITLE_TAKEN = {"4105": "MongoDB Error: Video Title Already Taken"}
    MONGODB_THUMBNAIL_MISS_ONE = {"4106": "MongoDB Error: Thumbnail missing one argument, must provide both"}
    MONGODB_LIST_EXPECTED = {"4107": "MongoDB Error: type <list> expected"}
    MONGODB_INVALID_VIDEO_CNT_PARAM = {"4108": "MongoDB Error: Invalid Video Count Param"}
    MONGODB_VIDEO_CNT_ZERO = {"4109": "MongoDB Error: Video Count Param Already Down To Zero"}
    MONGODB_INVALID_SEARCH_PARAM = {"4110": "MongoDB Error: Invalid Searching Param"}
    MONGODB_EMPTY_PARAM = {"4111": "MongoDB Error: Empty Input Param"}
    MONGODB_VIDEOOP_EXISTS = {"4112": "MongoDB Error: Video Op Alrady Exists"}
    MONGODB_USER_EMAIL_TAKEN = {"4113": "MongoDB Error: User Email Already Taken"}
    MONGODB_INVALID_USER_STATUS = {"4114": "MongoDB Error: Invalid User Status"}
    MONGODB_UPDATE_SAME_NAME = {"4115": "MongoDB Error: Update To Same Name"}
    MONGODB_UPDATE_SAME_PASS = {"4116": "MongoDB Error: Update To Same Password"}
    MONGODB_INVALID_THUMBNAIL = {"4117": "MongoDB Error: Invalid Thumbnail Type"}
    MONGODB_LOGIN_INFO_EXISTS = {"4118": "MongoDB Error: Login Info Already Exists"}
    MONGODB_FOLLOW_REL_EXISTS = {"4119": "MongoDB Error: Following Relationship Already Exists"}
    MONGODB_FOLLOWER_NOT_FOUND = {"4120": "MongoDB Error: User Follower Not Found"}
    MONGODB_FOLLOWED_NOT_FOUND = {"4121": "MongoDB Error: User To Be Followed Not Found"}
    MONGODB_RE_PATTERN_EXPECTED = {"4122": "MongoDB Error: type <re:Pattern> Expected"}

    # Util 5 Series
    UTIL_INVALID_PATTERN_PARAM = {"4001": "Util Error: Pattern Compile Param Not Supported"}

    # Model Error 6 Series

    def get_code(self):
        """
        retrive error code based on enum key
        :return: error code
        """
        return list(self.value.keys())[0]

    def get_msg(self):
        """
        retrive error message based on enum name
        :return: error message
        """
        return list(self.value.values())[0]


if __name__ == '__main__':
    # print error code
    code = ErrorCode.MONGODB_CONNECTION_FAILURE.get_code()
    print("code:", code)
    # print error message
    msg = ErrorCode.MONGODB_CONNECTION_FAILURE.get_msg()
    print("msg:", msg)

    print()

    # Traverse enum
    for status in ErrorCode:
        print(status.name, ":", status.value)
