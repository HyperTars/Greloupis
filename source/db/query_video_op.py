from source.models.model_video_op import VideoOp
from source.db.query_user import query_user_get_by_id
from source.db.query_video import query_video_get_by_id
from source.models.model_errors import ErrorCode
import bson
import datetime
import re


##########
# CREATE #
##########
def query_video_op_create(user_id: str, video_id: str, init_time=datetime.datetime.utcnow()):
    """
    :param user_id: user's unique id
    :param video_id: video's unique id
    :param init_time: op creation time (optional, default utc now)
    :return VideoOp model if succeeded, -1 if no such user, -2 if no such video, -3 if VideoOp exists
    """
    if len(query_user_get_by_id(user_id)) == 0:
        return ErrorCode.MONGODB_USER_NOT_FOUND

    if len(query_video_get_by_id(video_id)) == 0:
        return ErrorCode.MONGODB_VIDEO_NOT_FOUND

    if len(query_video_op_get_by_user_video(user_id, video_id)) > 0:
        return ErrorCode.MONGODB_VIDEOOP_EXISTS

    video_op = VideoOp(user_id=user_id, video_id=video_id, process=0, comment="", like=False,
                       dislike=False, star=False, process_date=init_time, comment_date=init_time,
                       like_date=init_time, dislike_date=init_time, star_date=init_time)

    return video_op.save()


############
# RETRIEVE #
############
def query_video_op_get_by_user_id(user_id: str):
    """
    :param: user_id, user's unique id
    :return: an array of such video_op, len == 0 if no such video_op
    """
    return VideoOp.objects(user_id=user_id)


def query_video_op_get_by_video_id(video_id: str):
    """
    :param: video_id, video's unique id
    :return: an array of such video_op, len == 0 if no such video_op
    """
    return VideoOp.objects(video_id=video_id)


def query_video_op_get_by_user_video(user_id: str, video_id: str):
    """
    :param: user_id, user's unique id
    :param: video_id, video's unique id
    :return: an array of such video_op (len == 0 or 1), len == 0 if no such video_op, len == 1 if found
    """
    return VideoOp.objects(user_id=user_id, video_id=video_id)


def query_video_op_get_by_op_id(op_id: str):
    """
    :param: op_id, video operation unique id
    :return: an array of such video_op (len == 0 or 1), len == 0 if no such video_op_id, len == 1 if found
    """
    return VideoOp.objects(_id=bson.ObjectId(op_id))


##########
# UPDATE #
##########
def query_video_op_update_process(op_id: str, process: int, process_date=datetime.datetime.utcnow()):
    """
    :param: op_id, video op unique id
    :param: process, video watching process
    :param: process_date (optional, default utc now)
    :return: 1 if succeeded, -1 if no such video_op
    """
    if len(query_video_op_get_by_op_id(op_id)) == 0:
        # No such video op
        return ErrorCode.MONGODB_VIDEOOP_NOT_FOUND

    return VideoOp.objects(_id=bson.ObjectId(op_id)).update(process=process, process_date=process_date)


def query_video_op_update_comment(op_id: str, comment: str, comment_date=datetime.datetime.utcnow()):
    """
    :param: op_id, video op unique id
    :param: comment, video comment
    :param: comment_date (optional, default utc now)
    :return: 1 if succeeded, -1 if no such video_op
    """
    if len(query_video_op_get_by_op_id(op_id)) == 0:
        # No such video op
        return ErrorCode.MONGODB_VIDEOOP_NOT_FOUND

    return VideoOp.objects(_id=bson.ObjectId(op_id)).update(comment=comment, comment_date=comment_date)


def query_video_op_update_like(op_id: str, like: bool, like_date=datetime.datetime.utcnow()):
    """
    :param: op_id, video op unique id
    :param: like, video like (boolean)
    :param: like_date (optional, default utc now)
    :return: 1 if succeeded, -1 if no such video_op
    """
    if len(query_video_op_get_by_op_id(op_id)) == 0:
        # No such video op
        return ErrorCode.MONGODB_VIDEOOP_NOT_FOUND

    return VideoOp.objects(_id=bson.ObjectId(op_id)).update(like=like, like_date=like_date)


def query_video_op_update_dislike(op_id: str, dislike: bool, dislike_date=datetime.datetime.utcnow()):
    """
    :param: op_id, video op unique id
    :param: dislike, video dislike (boolean)
    :param: dislike_date (optional, default utc now)
    :return: 1 if succeeded, -1 if no such video_op
    """
    if len(query_video_op_get_by_op_id(op_id)) == 0:
        # No such video op
        return ErrorCode.MONGODB_VIDEOOP_NOT_FOUND

    return VideoOp.objects(_id=bson.ObjectId(op_id)).update(dislike=dislike, dislike_date=dislike_date)


def query_video_op_update_star(op_id: str, star: bool, star_date=datetime.datetime.utcnow()):
    """
    :param: op_id, video op unique id
    :param: star, video star (boolean)
    :param: star_date (optional, default utc now)
    :return: 1 if succeeded, -1 if no such video_op
    """
    if len(query_video_op_get_by_op_id(op_id)) == 0:
        # No such video op
        return ErrorCode.MONGODB_VIDEOOP_NOT_FOUND

    return VideoOp.objects(_id=bson.ObjectId(op_id)).update(star=star, star_date=star_date)


##########
# DELETE #
##########
def query_video_op_delete(op_id: str):
    """
    :param video_id: video's unique id
    :return: 1 if succeeded, -1 if no such video
    """
    if len(query_video_op_get_by_op_id(op_id)) == 0:
        # No such video op
        return ErrorCode.MONGODB_VIDEOOP_NOT_FOUND

    return VideoOp.objects(_id=bson.ObjectId(op_id)).delete()


##########
# SEARCH #
##########
# Search by i-contains (ignore case)
def query_video_op_search_comment_by_contains(comment: str):
    """
    Search video op by comment keyword
    :param comment: comment keyword
    :return: result array of VideoOp Model
    """
    return VideoOp.objects.filter(comment__icontains=comment)


# Search by pattern
def query_video_op_search_comment_by_pattern(comment):
    """
    Search video op by comment pattern
    :param comment: comment pattern
    :return: result array of VideoOp Model
    """
    # Check input param
    if type(comment) != re.Pattern:
        return ErrorCode.MONGODB_RE_PATTERN_EXPECTED

    return VideoOp.Objects(comment=comment)
