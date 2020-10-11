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
    # Database 3 Series
    MONGODB_CONNECTION_FAILURE = {"3000": "MongoDB Connection Failure"}
    MONGODB_USER_NOT_FOUND = {"3101": "MongoDB Error: User Not Found"}
    MONGODB_VIDEO_NOT_FOUND = {"3102": "MongoDB Error: Video Not Found"}
    MONGODB_VIDEOOP_NOT_FOUND = {"3103": "MongoDB Error: VideoOp Not Found"}
    MONGODB_USER_NAME_TAKEN = {"3104": "MongoDB Error: User Name Already Taken"}
    MONGODB_VIDEO_TITLE_TAKEN = {"3105": "MongoDB Error: Video Title Already Taken"}
    MONGODB_THUMBNAIL_MISS_ONE = {"3106": "MongoDB Error: Thumbnail missing one argument, must provide both"}
    MONGODB_LIST_EXPECTED = {"3107": "MongoDB Error: type <list> expected"}
    MONGODB_INVALID_VIDEO_CNT_PARAM = {"3108": "MongoDB Error: Invalid Video Count Param"}
    MONGODB_VIDEO_CNT_ZERO = {"3109": "MongoDB Error: Video Count Param Already Down To Zero"}
    MONGODB_INVALID_SEARCH_PARAM = {"3110": "MongoDB Error: Invalid Searching Param"}
    MONGODB_EMPTY_PARAM = {"3111": "MongoDB Error: Empty Input Param"}
    MONGODB_VIDEOOP_EXISTS = {"3112": "MongoDB Error: Video Op Alrady Exists"}
    MONGODB_USER_EMAIL_TAKEN = {"3113": "MongoDB Error: User Email Already Taken"}
    MONGODB_INVALID_USER_STATUS = {"3114": "MongoDB Error: Invalid User Status"}
    MONGODB_UPDATE_SAME_NAME = {"3115": "MongoDB Error: Update To Same Name"}
    MONGODB_UPDATE_SAME_PASS = {"3116": "MongoDB Error: Update To Same Password"}
    MONGODB_INVALID_THUMBNAIL = {"3117": "MongoDB Error: Invalid Thumbnail Type"}
    MONGODB_LOGIN_INFO_EXISTS = {"3118": "MongoDB Error: Login Info Already Exists"}
    MONGODB_FOLLOW_REL_EXISTS = {"3119": "MongoDB Error: Following Relationship Already Exists"}
    MONGODB_FOLLOWER_NOT_FOUND = {"3120": "MongoDB Error: User Follower Not Found"}
    MONGODB_FOLLOWED_NOT_FOUND = {"3121": "MongoDB Error: User To Be Followed Not Found"}
    MONGODB_RE_PATTERN_EXPECTED = {"3122": "MongoDB Error: type <re:Pattern> Expected"}
    MONGODB_INVALID_PATTERN_PARAM = {"3123": "MongoDB Error: Pattern Compile Param Not Supported"}

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
