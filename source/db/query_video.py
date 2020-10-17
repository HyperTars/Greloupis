from source.models.model_video import *
from source.db.query_user import query_user_get_by_id
from source.models.model_errors import *
from source.utils.util_time import get_time_now_utc
import bson
import datetime
import re


VALID_VIDEO_STATUS = ['public', 'private', 'processing', 'deleted']
VALID_VIDEO_CNT = ['view', 'views', 'video_view',
                   'comment', 'comments', 'video_comment',
                   'like', 'likes', 'video_like',
                   'dislike', 'dislikes', 'video_dislike',
                   'star', 'stars', 'video_star',
                   'share', 'shares', 'video_share']


##########
# CREATE #
##########
def query_video_create(user_id: str, video_title: str, video_raw_content: str, **kw):

    """
    :param user_id: (required) user's unique id
    :param video_title: (required) video's title
    :param video_raw_content: (required) URI of raw video data (in temp space, to be transcode)
    :param video_channel: (optional) channel of video (default self-made)
    :param video_duration: (optional) duration of video in second
    :param video_raw_status: (optional) status of raw video data, default: pending
    :param video_raw_size: (optional) size of raw video data
    :param video_tag: (optional) array of video's tags
    :param video_category: (optional) array of video's categories
    :param video_description: (optional) video's description
    :param video_language: (optional) video's language
    :param video_status: (optional) video's status, default: public
    :param video_thumbnail: (optional) video's thumbnail uri
    :param video_upload_date: (optional) video's upload date
    :return: video created (Video Model)

    video_raw_content: user will get a raw video URI after uploading raw video to cache
    (temp storage space where videos waiting for trans-coding)
    user is allowed to create video info before trans-coding completed
    """

    if len(query_user_get_by_id(user_id)) == 0:
        raise MongoError(ErrorCode.MONGODB_USER_NOT_FOUND)

    if len(query_video_get_by_title(video_title)) > 0:
        raise MongoError(ErrorCode.MONGODB_VIDEO_TITLE_TAKEN)

    # Default
    video_raw_status = "pending"
    video_raw_size = 0.00
    video_channel = "self-made"
    video_duration = 0
    video_tag = []
    video_category = []
    video_description = ""
    video_language = ""
    video_status = "public"
    video_thumbnail = ""
    video_upload_date = get_time_now_utc()

    # Fill if exist
    if 'video_raw_status' in kw:
        video_raw_status = kw['video_raw_status']
    if 'video_raw_size' in kw:
        video_raw_size = kw['video_raw_size']
    if 'video_channel' in kw:
        video_channel = kw['video_channel']
    if 'video_duration' in kw:
        video_duration = kw['video_duration']
    if 'video_tag' in kw:
        video_tag = kw['video_tag']
    if 'video_category' in kw:
        video_category = kw['video_category']
    if 'video_description' in kw:
        video_description = kw['video_description']
    if 'video_language' in kw:
        video_language = kw['video_language']
    if 'video_status' in kw:
        video_status = kw['video_status']
    if 'video_thumbnail' in kw:
        video_thumbnail = kw['video_thumbnail'],
    if 'video_upload_date' in kw:
        video_upload_date = kw['upload_date']

    # Construct Video Model
    try:
        video = Video(user_id=user_id, video_title=video_title, video_raw_content=video_raw_content,
                      video_raw_status=video_raw_status, video_raw_size=video_raw_size, video_duration=video_duration,
                      video_channel=video_channel, video_tag=video_tag, video_category=video_category,
                      video_description=video_description, video_language=video_language, video_status=video_status,
                      video_view=0, video_comment=0, video_like=0, video_dislike=0, video_star=0, video_share=0,
                      video_thumbnail=video_thumbnail, video_upload_date=video_upload_date, video_uri=VideoURI())
    except Exception:
        raise MongoError(ErrorCode.MONGODB_VIDEO_CREATE_FAILURE)

    return video.save()


############
# RETRIEVE #
############
def query_video_get_by_video_id(video_id: str):
    """
    :param video_id: video's unique id
    :return: an array of such Video (len == 0 or 1), len == 0 if no such video_id, len == 1 if found
    """
    return Video.objects(_id=bson.ObjectId(video_id))


def query_video_get_by_user_id(user_id: str):
    """
    :param user_id: user's unique id
    :return: an array of such Video (videos created by the user)
    """
    return Video.objects(user_id=user_id)


def query_video_get_by_title(video_title: str):
    """
    :param video_title: video's unique title
    :return: an array of such Video (len == 0 or 1), len == 0 if no such video_id, len == 1 if found
    """
    return Video.objects(video_title=video_title)


##########
# UPDATE #
##########
def query_video_cnt_incr_by_one(video_id: str, video_cnt: str):
    """
    This is for incrementing total number of views/comments/likes/dislikes/stars/shares
    :param video_id: video's unique id
    :param video_cnt: can choose from (view/comment/like/dislike/star/share)
    :return: 1 if succeeded
    """

    if len(query_video_get_by_video_id(video_id)) == 0:
        raise MongoError(ErrorCode.MONGODB_VIDEO_NOT_FOUND)

    _id = bson.ObjectId(video_id)

    if video_cnt == 'view' or video_cnt == 'views' or video_cnt == 'video_view':
        Video.objects(_id=_id).update(inc__video_view=1)
    elif video_cnt == 'comment' or video_cnt == 'comments' or video_cnt == 'video_comment':
        Video.objects(_id=_id).update(inc__video_comment=1)
    elif video_cnt == 'like' or video_cnt == 'likes' or video_cnt == 'video_like':
        Video.objects(_id=_id).update(inc__video_like=1)
    elif video_cnt == 'dislike' or video_cnt == 'dislikes' or video_cnt == 'video_dislike':
        Video.objects(_id=_id).update(inc__video_dislike=1)
    elif video_cnt == 'star' or video_cnt == 'stars' or video_cnt == 'video_star':
        Video.objects(_id=_id).update(inc__video_star=1)
    elif video_cnt == 'share' or video_cnt == 'shares' or video_cnt == 'video_share':
        Video.objects(_id=_id).update(inc__video_share=1)
    else:
        raise MongoError(ErrorCode.MONGODB_INVALID_VIDEO_CNT_PARAM)

    return 1


def query_video_cnt_decr_by_one(video_id: str, video_cnt: str):
    """
    This is for decrementing total number of views/comments/likes/dislikes/stars/shares
    :param video_id: video's unique id
    :param video_cnt: can choose from (view/comment/like/dislike/star/share)
    :return: 1 if succeeded
    """

    videos = query_video_get_by_video_id(video_id)
    if len(videos) == 0:
        raise MongoError(ErrorCode.MONGODB_VIDEO_NOT_FOUND)

    if video_cnt not in VALID_VIDEO_CNT:
        raise MongoError(ErrorCode.MONGODB_INVALID_VIDEO_CNT_PARAM)

    _id = bson.ObjectId(video_id)
    video = videos[0].to_dict()

    if video_cnt == 'view' or video_cnt == 'views' or video_cnt == 'video_view':
        if video['video_view'] <= 0:
            raise MongoError(ErrorCode.MONGODB_VIDEO_CNT_ZERO)
        Video.objects(_id=_id).update(dec__video_view=1)
    if video_cnt == 'comment' or video_cnt == 'comments' or video_cnt == 'video_comment':
        if video['video_comment'] <= 0:
            raise MongoError(ErrorCode.MONGODB_VIDEO_CNT_ZERO)
        Video.objects(_id=_id).update(dec__video_comment=1)
    if video_cnt == 'like' or video_cnt == 'likes' or video_cnt == 'video_like':
        if video['video_like'] <= 0:
            raise MongoError(ErrorCode.MONGODB_VIDEO_CNT_ZERO)
        Video.objects(_id=_id).update(dec__video_like=1)
    if video_cnt == 'dislike' or video_cnt == 'dislikes' or video_cnt == 'video_dislike':
        if video['video_dislike'] <= 0:
            raise MongoError(ErrorCode.MONGODB_VIDEO_CNT_ZERO)
        Video.objects(_id=_id).update(dec__video_dislike=1)
    if video_cnt == 'star' or video_cnt == 'stars' or video_cnt == 'video_star':
        if video['video_star'] <= 0:
            raise MongoError(ErrorCode.MONGODB_VIDEO_CNT_ZERO)
        Video.objects(_id=_id).update(dec__video_star=1)
    if video_cnt == 'share' or video_cnt == 'shares' or video_cnt == 'video_share':
        if video['video_share'] <= 0:
            raise MongoError(ErrorCode.MONGODB_VIDEO_CNT_ZERO)
        Video.objects(_id=_id).update(dec__video_share=1)

    return 1


def query_video_update(video_id: str, **kw):
    """
    :param video_id: video's unique id
    :param video_title (optional): video's new title
    :param video_raw_content (optional): new URI of raw video data (in temp space, to be transcode)
    :param video_raw_status (optional): new status of raw video data, default
    :param video_raw_size (optional): new size of raw video data
    :param video_duration: (optional) duration of video in second
    :param video_channel: (optional) channel of video (default self-made)
    :param video_tag (optional): array of video's new tags
    :param video_category (optional): array of video's new categories
    :param video_description (optional): video's new description
    :param video_language (optional): video's new language
    :param video_status (optional): video's new status, default: public
    :param video_thumbnail (optional): video's new thumbnail uri
    :param video_uri_low (optional): video's new final uri (480p low resolution)
    :param video_uri_mid (optional): video's new final uri (720p mid resolution)
    :param video_uri_high (optional): video's new final uri (1080p high resolution)
    :return 1 if succeeded
    """

    if len(query_video_get_by_video_id(video_id)) == 0:
        raise MongoError(ErrorCode.MONGODB_VIDEO_NOT_FOUND)

    _id = bson.ObjectId(video_id)

    if 'video_title' in kw:
        videos = query_video_get_by_title(kw['video_title'])
        if len(videos) == 0:
            raise MongoError(ErrorCode.MONGODB_VIDEO_TITLE_TAKEN)
        Video.objects(_id=_id).update(video_title=kw['video_title'])
    if 'video_raw_content' in kw:
        Video.objects(_id=_id).update(video_raw_content=kw['video_raw_content'])
    if 'video_raw_status' in kw:
        Video.objects(_id=_id).update(video_status=kw['video_raw_status'])
    if 'video_raw_size' in kw:
        Video.objects(_id=_id).update(video_raw_size=kw['video_raw_size'])
    if 'video_duration' in kw:
        Video.objects(_id=_id).update(video_duration=kw['video_duration'])
    if 'video_channel' in kw:
        Video.objects(_id=_id).update(video_channel=kw['video_channel'])
    if 'video_tag' in kw:
        if type(kw['video_tag']) is not list:
            raise MongoError(ErrorCode.MONGODB_LIST_EXPECTED)
        Video.objects(_id=_id).update(video_tag=kw['video_tag'])
    if 'video_category' in kw:
        if type(kw['video_category']) is not list:
            raise MongoError(ErrorCode.MONGODB_LIST_EXPECTED)
        Video.objects(_id=_id).update(video_categoty=kw['video_category'])
    if 'video_description' in kw:
        Video.objects(_id=_id).update(video_description=kw['video_description'])
    if 'video_language' in kw:
        Video.objects(_id=_id).update(video_language=kw['video_language'])
    if 'video_status' in kw:
        if kw['video_status'] not in VALID_VIDEO_STATUS:
            raise MongoError(ErrorCode.MONGODB_INVALID_USER_STATUS)
        Video.objects(_id=_id).update(video_language=kw['video_status'])
    if 'video_thumbnail' in kw:
        Video.objects(_id=_id).update(video_thumbnail=kw['video_thumbnail'])
    if 'video_uri_low' in kw:
        Video.objects(_id=_id).update(set__video_uri__video_uri_low=kw['video_uri_low'])
    if 'video_uri_mid' in kw:
        Video.objects(_id=_id).update(set__video_uri__video_uri_mid=kw['video_uri_mid'])
    if 'video_uri_high' in kw:
        Video.objects(_id=_id).update(set__video_uri__video_uri_high=kw['video_uri_high'])

    return 1


##########
# DELETE #
##########
def query_video_delete(video_id: str):
    """
    :param video_id: video's unique id
    :return: 1 if succeeded, -1 if no such video
    """
    videos = query_video_get_by_video_id(video_id)
    if len(videos) == 0:
        raise MongoError(ErrorCode.MONGODB_VIDEO_NOT_FOUND)

    return Video.objects(_id=bson.ObjectId(video_id)).delete()


##########
# Search #
##########
# Search by i-contains
def query_video_search_by_contains(**kw):
    """
    Search video by i-contains (ignore case)
    :param video_id: (optional) video's unique id
    :param user_id: (optional) user's unique id
    :param video_title: (optional) string of video title to be searched
    :param video_channel: (optional) channel of videos
    :param video_category: (optional) category of videos
    :return: array of searching results (Video Model)
    """
    if 'video_id' in kw:
        return query_video_get_by_video_id(kw['video_id'])
    elif 'user_id' in kw:
        return query_video_get_by_user_id(kw['user_id'])
    elif 'video_title' in kw:
        return Video.objects.filter(video_title__icontains=kw['video_title'])
    elif 'video_channel' in kw:
        return Video.objects.filter(video_channel__icontains=kw['video_channel'])
    elif 'video_category' in kw:
        return Video.objects.filter(video_category__icontains=kw['video_category'])
    elif 'video_tag' in kw:
        return Video.objects.filter(video_tag__icontains=kw['video_tag'])
    elif 'video_description' in kw:
        return Video.objects.filter(video_description__icontains=kw['video_description'])

    raise MongoError(ErrorCode.MONGODB_INVALID_SEARCH_PARAM)


# Search by pattern
def query_video_search_by_pattern(**kw):
    """
    :param pattern_title: (optional) search title pattern
    :param pattern description: (optional) search description pattern
    :return: array of searching results (Video Model)
    """
    # Check input param
    if len(kw) == 0:
        raise MongoError(ErrorCode.MONGODB_EMPTY_PARAM)

    for arg in kw:
        if type(kw[arg]) != re.Pattern:
            raise MongoError(ErrorCode.MONGODB_RE_PATTERN_EXPECTED)

    if 'pattern_title' in kw:
        return Video.objects(video_title=kw['pattern_title'])
    elif 'pattern_channel' in kw:
        return Video.objects(video_channel=kw['pattern_channel'])
    elif 'pattern_description' in kw:
        return Video.objects(video_description=kw['pattern_description'])

    raise MongoError(ErrorCode.MONGODB_INVALID_SEARCH_PARAM)


# Search by aggregate
def query_video_search_by_aggregate(aggr: dict):
    """
    :param aggr: dict of searching param
    :return: array of searching results in dict
    """
    return list(Video.objects.aggregate(aggr))
