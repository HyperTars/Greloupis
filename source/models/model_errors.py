from flask_mongoengine import MongoEngine
from enum import Enum, unique
import datetime
import sys

db = MongoEngine()


# Error Model
class Error(db.Document):
    call = db.DictField(required=True)
    response = db.DictField(required=True)
    date = db.DateTimeField(default=datetime.datetime.now(), required=True)


@unique
class ErrorCode(Enum):
    # General 1 Series
    ERR_INCORRECT_CODE = {1001: "Error Code: Incorrect Error Code"}

    # Routes 2 Series
    ROUTE_INVALID_REQUEST_PARAM = {2001: "Route Error: Invalid Request Parameters"}

    # Service 3 Series
    SERVICE_PARAM_SLICE_NOT_SUPPORT = {3001: "Service Error: Current Param Does Not Support Slice"}
    SERVICE_PATTERN_SEARCH_NOT_SUPPORT = {3002: "Service Error: Current Param Does Not Support Pattern Search"}
    SERVICE_MISSING_PARAM = {3003: "Service Error: Missing Essential Param"}
    SERVICE_USER_NOT_FOUND = {3004: "Service Error: User Not Found"}
    SERVICE_USER_CREATION_FAILURE = {3005: "Service Error: User Creation Failure"}
    SERVICE_USER_AUTH_FAILURE = {3006: "Service Error: User Auth Failure"}

    # Database 4 Series
    MONGODB_CONNECTION_FAILURE = {4000: "MongoDB Connection Failure"}
    MONGODB_USER_NOT_FOUND = {4101: "MongoDB Error: User Not Found"}
    MONGODB_VIDEO_NOT_FOUND = {4102: "MongoDB Error: Video Not Found"}
    MONGODB_VIDEO_OP_NOT_FOUND = {4103: "MongoDB Error: VideoOp Not Found"}
    MONGODB_USER_NAME_TAKEN = {4104: "MongoDB Error: User Name Already Taken"}
    MONGODB_VIDEO_TITLE_TAKEN = {4105: "MongoDB Error: Video Title Already Taken"}
    MONGODB_THUMBNAIL_MISS_ONE = {4106: "MongoDB Error: Thumbnail missing one argument, must provide both"}
    MONGODB_LIST_EXPECTED = {4107: "MongoDB Error: type <list> expected"}
    MONGODB_INVALID_VIDEO_CNT_PARAM = {4108: "MongoDB Error: Invalid Video Count Param"}
    MONGODB_VIDEO_CNT_ZERO = {4109: "MongoDB Error: Video Count Param Already Down To Zero"}
    MONGODB_INVALID_SEARCH_PARAM = {4110: "MongoDB Error: Invalid Searching Param"}
    MONGODB_EMPTY_PARAM = {4111: "MongoDB Error: Empty Input Param"}
    MONGODB_VIDEO_OP_EXISTS = {4112: "MongoDB Error: Video Op Already Exists"}
    MONGODB_USER_EMAIL_TAKEN = {4113: "MongoDB Error: User Email Already Taken"}
    MONGODB_USER_INVALID_STATUS = {4114: "MongoDB Error: Invalid User Status"}
    MONGODB_UPDATE_SAME_NAME = {4115: "MongoDB Error: Update To Same Name"}
    MONGODB_UPDATE_SAME_PASS = {4116: "MongoDB Error: Update To Same Password"}
    MONGODB_INVALID_THUMBNAIL = {4117: "MongoDB Error: Invalid Thumbnail Type"}
    MONGODB_LOGIN_INFO_EXISTS = {4118: "MongoDB Error: Login Info Already Exists"}
    MONGODB_FOLLOW_REL_EXISTS = {4119: "MongoDB Error: Following Relationship Already Exists"}
    MONGODB_FOLLOWER_NOT_FOUND = {4120: "MongoDB Error: User Follower Not Found"}
    MONGODB_FOLLOWED_NOT_FOUND = {4121: "MongoDB Error: User To Be Followed Not Found"}
    MONGODB_RE_PATTERN_EXPECTED = {4122: "MongoDB Error: type <re:Pattern> Expected"}
    MONGODB_STR_EXPECTED = {4123: "MongoDB Error: type <str> Expected"}
    MONGODB_USER_CREATE_FAILURE = {4124: "MongoDB Error: User Creation Failure"}
    MONGODB_USER_CREATE_FOLLOW_FAILURE = {4125: "MongoDB Error: User Create Follow Relationship Failure"}
    MONGODB_USER_DELETE_FOLLOW_FAILURE = {4126: "MongoDB Error: User Delete Follow Relationship Failure"}
    MONGODB_VIDEO_CREATE_FAILURE = {4127: "MongoDB Error: Video Creation Failure"}
    MONGODB_VIDEO_INVALID_STATUS = {4128: "MongoDB Error: Video Invalid Status"}
    MONGODB_DICT_EXPECTED = {4129: "MongoDB Error: type <dict> Expected"}
    MONGODB_VIDEO_UPDATE_FAILURE = {4130: "MongoDB Error: Video Update Failure"}
    MONGODB_VIDEO_DELETE_FAILURE = {4131: "MongoDB Error: Video Delete Failure"}
    MONGODB_VIDEO_COMMENT_UPDATE_FAILURE = {4132: "MongoDB Error: Video Comment Update Failure"}
    MONGODB_VIDEO_COMMENT_DELETE_FAILURE = {4133: "MongoDB Error: Video Comment Delete Failure"}
    MONGODB_VIDEO_PROCESS_UPDATE_FAILURE = {4134: "MongoDB Error: Video Process Update Failure"}
    MONGODB_VIDEO_PROCESS_DELETE_FAILURE = {4135: "MongoDB Error: Video Process Delete Failure"}
    MONGODB_VIDEO_LIKE_UPDATE_FAILURE = {4136: "MongoDB Error: Video Like Update Failure"}
    MONGODB_VIDEO_DISLIKE_UPDATE_FAILURE = {4137: "MongoDB Error: Video Dislike Update Failure"}
    MONGODB_VIDEO_STAR_UPDATE_FAILURE = {4138: "MongoDB Error: Video Star Update Failure"}

    # Model Error 5 Series
    MODEL_PASS_NOT_READABLE = {5001: "Password Is Not Readable"}

    # Util 6 Series
    UTIL_INVALID_PATTERN_PARAM = {6001: "Util Error: Pattern Compile Param Not Supported"}

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


class ModelError(Exception):
    pass


class MongoError(Exception):
    def __init__(self, error_code, message='', *args, **kwargs):
        if not isinstance(error_code, ErrorCode):
            msg = "Error code passed in the error_code param must be of type ErrorCode"
            raise MongoError(ErrorCode.ERR_INCORRECT_CODE)

        self.error_code = error_code
        self.traceback = sys.exc_info()
        try:
            msg = '[{0}], {1}'.format(error_code.name, message.format(*args, **kwargs))
        except (IndexError, KeyError):
            msg = '[{0}] {1}'.format(error_code.name, message)

        super().__init__(msg)

    def get_code(self):
        return self.error_code.get_code()

    def get_msg(self):
        return self.error_code.get_msg()

    def __str__(self):
        return repr(self.error_code)


class ServiceError(Exception):
    def __init__(self, error_code, message='', *args, **kwargs):
        if not isinstance(error_code, ErrorCode):
            msg = "Error code passed in the error_code param must be of type ErrorCode"
            raise ServiceError(ErrorCode.ERR_INCORRECT_CODE)

        self.error_code = error_code
        self.traceback = sys.exc_info()
        try:
            msg = '[{0}], {1}'.format(error_code.name, message.format(*args, **kwargs))
        except (IndexError, KeyError):
            msg = '[{0}] {1}'.format(error_code.name, message)

        super().__init__(msg)

    def get_code(self):
        return self.error_code.get_code()

    def get_msg(self):
        return self.error_code.get_msg()

    def __str__(self):
        return repr(self.error_code)


class RouteError(Exception):
    def __init__(self, error_code, message='', *args, **kwargs):
        if not isinstance(error_code, ErrorCode):
            msg = "Error code passed in the error_code param must be of type ErrorCode"
            raise RouteError(ErrorCode.ERR_INCORRECT_CODE)

        self.error_code = error_code
        self.traceback = sys.exc_info()
        try:
            msg = '[{0}], {1}'.format(error_code.name, message.format(*args, **kwargs))
        except (IndexError, KeyError):
            msg = '[{0}] {1}'.format(error_code.name, message)

        super().__init__(msg)

    def get_code(self):
        return self.error_code.get_code()

    def get_msg(self):
        return self.error_code.get_msg()

    def __str__(self):
        return repr(self.error_code)


class UtilError(Exception):
    def __init__(self, error_code, message='', *args, **kwargs):
        if not isinstance(error_code, ErrorCode):
            msg = "Error code passed in the error_code param must be of type ErrorCode"
            raise UtilError(ErrorCode.ERR_INCORRECT_CODE)

        self.error_code = error_code
        self.traceback = sys.exc_info()
        try:
            msg = '[{0}], {1}'.format(error_code.name, message.format(*args, **kwargs))
        except (IndexError, KeyError):
            msg = '[{0}] {1}'.format(error_code.name, message)

        super().__init__(msg)

    def get_code(self):
        return self.error_code.get_code()

    def get_msg(self):
        return self.error_code.get_msg()

    def __str__(self):
        return repr(self.error_code)


# print error code
# code = ErrorCode.MONGODB_CONNECTION_FAILURE.get_code()
# print("code:", code)
# print error message
# msg = ErrorCode.MONGODB_CONNECTION_FAILURE.get_msg()
# print("msg:", msg)
# Traverse enum
# for status in ErrorCode:
#    print(status.name, ":", status.value)
