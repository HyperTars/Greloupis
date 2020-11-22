from models.model_video import Video, VideoURI
from db.query_user import query_user_get_by_id
from models.model_errors import MongoError, ErrorCode
from utils.util_time import get_time_now_utc
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
def query_video_create(user_id: str):
    """
    Create Video
    :param user_id: (required) user's unique id
    :return: video uuid
    """
    if len(query_user_get_by_id(user_id)) == 0:
        raise MongoError(ErrorCode.MONGODB_USER_NOT_FOUND)

    # Construct Video Model
    video = Video(user_id=user_id, video_title="", video_raw_content="",
                  video_raw_status="pending", video_status="processing",
                  video_raw_size=0, video_duration=0,
                  video_channel="", video_tag=[], video_category=[],
                  video_description="", video_language="",
                  video_view=0, video_comment=0, video_like=0, video_dislike=0,
                  video_star=0, video_share=0, video_thumbnail="",
                  video_upload_date=get_time_now_utc(), video_uri=VideoURI())
    video.save()
    return str(video.id)


############
# RETRIEVE #
############
def query_video_get_by_video_id(video_id: str):
    """
    :param video_id: video's unique id
    :return: an array of such Video (len == 0 or 1), len == 0 if no such
    video_id, len == 1 if found
    """
    return Video.objects(id=video_id)


def query_video_get_by_user_id(user_id: str):
    """
    :param user_id: user's unique id
    :return: an array of such Video (videos created by the user)
    """
    return Video.objects(user_id=user_id)


def query_video_get_by_title(video_title: str):
    """
    :param video_title: video's unique title
    :return: an array of such Video (len == 0 or 1), len == 0 if no such
    video_id, len == 1 if found
    """
    return Video.objects(video_title=video_title)


##########
# UPDATE #
##########
def query_video_cnt_incr_by_one(video_id: str, video_cnt: str):
    """
    This is for incrementing total number of
    views/comments/likes/dislikes/stars/shares
    :param video_id: video's unique id
    :param video_cnt: can choose from (view/comment/like/dislike/star/share)
    :return: 1 if succeeded
    """

    if len(query_video_get_by_video_id(video_id)) == 0:
        raise MongoError(ErrorCode.MONGODB_VIDEO_NOT_FOUND)

    if video_cnt == 'view' or video_cnt == 'views' or video_cnt == \
            'video_view':
        Video.objects(id=video_id).update(inc__video_view=1)
    elif video_cnt == 'comment' or video_cnt == 'comments' or video_cnt == \
            'video_comment':
        Video.objects(id=video_id).update(inc__video_comment=1)
    elif video_cnt == 'like' or video_cnt == 'likes' or video_cnt == \
            'video_like':
        Video.objects(id=video_id).update(inc__video_like=1)
    elif video_cnt == 'dislike' or video_cnt == 'dislikes' or video_cnt == \
            'video_dislike':
        Video.objects(id=video_id).update(inc__video_dislike=1)
    elif video_cnt == 'star' or video_cnt == 'stars' or video_cnt == \
            'video_star':
        Video.objects(id=video_id).update(inc__video_star=1)
    elif video_cnt == 'share' or video_cnt == 'shares' or video_cnt == \
            'video_share':
        Video.objects(id=video_id).update(inc__video_share=1)
    else:
        raise MongoError(ErrorCode.MONGODB_INVALID_VIDEO_CNT_PARAM)

    return 1


def query_video_cnt_decr_by_one(video_id: str, video_cnt: str):
    """
    This is for decrementing total number of
    views/comments/likes/dislikes/stars/shares.

    :param video_id: video's unique id
    :param video_cnt: can choose from (view/comment/like/dislike/star/share)
    :return: 1 if succeeded, 0 if cnt < 0
    """

    videos = query_video_get_by_video_id(video_id)
    if len(videos) == 0:
        raise MongoError(ErrorCode.MONGODB_VIDEO_NOT_FOUND)

    if video_cnt not in VALID_VIDEO_CNT:
        raise MongoError(ErrorCode.MONGODB_INVALID_VIDEO_CNT_PARAM)

    video = videos[0].to_dict()

    if video_cnt == 'view' or video_cnt == 'views' or video_cnt == \
            'video_view':
        if video['video_view'] <= 0:
            return 0
            # raise MongoError(ErrorCode.MONGODB_VIDEO_CNT_ZERO)
        Video.objects(id=video_id).update(dec__video_view=1)
    if video_cnt == 'comment' or video_cnt == 'comments' or video_cnt == \
            'video_comment':
        if video['video_comment'] <= 0:
            return 0
            # raise MongoError(ErrorCode.MONGODB_VIDEO_CNT_ZERO)
        Video.objects(id=video_id).update(dec__video_comment=1)
    if video_cnt == 'like' or video_cnt == 'likes' or video_cnt == \
            'video_like':
        if video['video_like'] <= 0:
            return 0
            # raise MongoError(ErrorCode.MONGODB_VIDEO_CNT_ZERO)
        Video.objects(id=video_id).update(dec__video_like=1)
    if video_cnt == 'dislike' or video_cnt == 'dislikes' or video_cnt == \
            'video_dislike':
        if video['video_dislike'] <= 0:
            return 0
            # raise MongoError(ErrorCode.MONGODB_VIDEO_CNT_ZERO)
        Video.objects(id=video_id).update(dec__video_dislike=1)
    if video_cnt == 'star' or video_cnt == 'stars' or video_cnt == \
            'video_star':
        if video['video_star'] <= 0:
            return 0
            # raise MongoError(ErrorCode.MONGODB_VIDEO_CNT_ZERO)
        Video.objects(id=video_id).update(dec__video_star=1)
    if video_cnt == 'share' or video_cnt == 'shares' or video_cnt == \
            'video_share':
        if video['video_share'] <= 0:
            return 0
            # raise MongoError(ErrorCode.MONGODB_VIDEO_CNT_ZERO)
        Video.objects(id=video_id).update(dec__video_share=1)

    return 1


def query_video_update(video_id: str, **kw):
    """
    Update Video Info
    :param video_id: video's unique id
    :param kw:
        :key "video_title": (```str```, optional) new title
        :key "video_raw_content": (```str```, optional) new URI of raw video
        data (in temp space, to be transcode)
        :key "video_raw_status": (```str```, optional) new status of raw
        video data, default
        :key "video_raw_size": (```float```, optional) new size of raw video
        data
        :key "video_duration": (```int```, optional) duration of video in
        second
        :key "video_channel": (```str```, optional) channel of video (default
        self-made)
        :key "video_tag": (```list```, optional) array of new tags
        :key "video_category": (```list```, optional) array of new categories
        :key "video_description": (```str```, optional) new description
        :key "video_language": (```str```, optional) new language
        :key "video_status": (```str```, optional) new status, default: public
        :key "video_thumbnail": (```str```, optional) new thumbnail uri
        :key "video_uri_low": (```str```, optional) new final uri (480p low
        resolution)
        :key "video_uri_mid": (```str```, optional) new final uri (720p mid
        resolution)
        :key "video_uri_high": (```str```, optional) new final uri (1080p
        high resolution)
    \nAt least one key must be provided
    :return: 1 if succeeded
    """

    if len(query_video_get_by_video_id(video_id)) == 0:
        raise MongoError(ErrorCode.MONGODB_VIDEO_NOT_FOUND)

    if 'video_title' in kw and kw['video_title'] != "":
        videos = query_video_get_by_title(kw['video_title'])
        if len(videos) != 0:
            raise MongoError(ErrorCode.MONGODB_VIDEO_TITLE_TAKEN)
        Video.objects(id=video_id).update(video_title=kw['video_title'])
    if 'video_raw_content' in kw:
        Video.objects(id=video_id).update(
            video_raw_content=kw['video_raw_content'])
    if 'video_raw_status' in kw:
        Video.objects(id=video_id).update(
            video_raw_status=kw['video_raw_status'])
    if 'video_raw_size' in kw:
        Video.objects(id=video_id).update(video_raw_size=kw['video_raw_size'])
    if 'video_duration' in kw:
        Video.objects(id=video_id).update(video_duration=kw['video_duration'])
    if 'video_channel' in kw:
        Video.objects(id=video_id).update(video_channel=kw['video_channel'])
    if 'video_tag' in kw:
        if type(kw['video_tag']) is not list:
            raise MongoError(ErrorCode.MONGODB_LIST_EXPECTED)
        Video.objects(id=video_id).update(video_tag=kw['video_tag'])
    if 'video_category' in kw:
        if type(kw['video_category']) is not list:
            raise MongoError(ErrorCode.MONGODB_LIST_EXPECTED)
        Video.objects(id=video_id).update(video_category=kw['video_category'])
    if 'video_description' in kw:
        Video.objects(id=video_id).update(
            video_description=kw['video_description'])
    if 'video_language' in kw:
        Video.objects(id=video_id).update(video_language=kw['video_language'])
    if 'video_status' in kw:
        if kw['video_status'] not in VALID_VIDEO_STATUS:
            raise MongoError(ErrorCode.MONGODB_VIDEO_INVALID_STATUS)
        Video.objects(id=video_id).update(video_status=kw['video_status'])
    if 'video_thumbnail' in kw:
        Video.objects(id=video_id).update(
            video_thumbnail=kw['video_thumbnail'])
    if 'video_uri_low' in kw:
        Video.objects(id=video_id).update(
            video_uri__video_uri_low=kw['video_uri_low'])
    if 'video_uri_mid' in kw:
        Video.objects(id=video_id).update(
            video_uri__video_uri_mid=kw['video_uri_mid'])
    if 'video_uri_high' in kw:
        Video.objects(id=video_id).update(
            video_uri__video_uri_high=kw['video_uri_high'])

    return 1


##########
# DELETE #
##########
def query_video_delete(video_id: str, silent=False):
    """
    :param video_id: video's unique id
    :param silent: delete video regardless of existence
    :return: 1 if succeeded, -1 if no such video
    """
    videos = query_video_get_by_video_id(video_id)
    if len(videos) == 0 and silent is False:
        raise MongoError(ErrorCode.MONGODB_VIDEO_NOT_FOUND)

    return Video.objects(id=video_id).delete()


##########
# Search #
##########
# Search by i-contains
def query_video_search_by_contains(**kw):
    """
    Search video by i-contains (ignore case)
    :param kw: keyword arguments
        :key "video_id": (```str```, optional) video's unique id
        :key "user_id": (```str```, optional) user's unique id
        :key "video_title": (```str```, optional) string of video title to be
        searched
        :key "video_channel": (```str```, optional) channel of videos
        :key "video_category": (```str```, optional) category of videos
    \nAt least one key must be provided
    :return: array of searching results (Video Model)
    """
    # Check input param
    if len(kw) == 0:
        raise MongoError(ErrorCode.MONGODB_EMPTY_PARAM)

    for arg in kw:
        if type(kw[arg]) != str:
            raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    if 'video_id' in kw:
        return query_video_get_by_video_id(kw['video_id'])
    elif 'user_id' in kw:
        return query_video_get_by_user_id(kw['user_id'])
    elif 'video_title' in kw:
        return Video.objects.filter(video_title__icontains=kw['video_title'])
    elif 'video_channel' in kw:
        return Video.objects.filter(
            video_channel__icontains=kw['video_channel'])
    elif 'video_category' in kw:
        return Video.objects.filter(
            video_category__icontains=kw['video_category'])
    elif 'video_tag' in kw:
        return Video.objects.filter(video_tag__icontains=kw['video_tag'])
    elif 'video_description' in kw:
        return Video.objects.filter(
            video_description__icontains=kw['video_description'])

    raise MongoError(ErrorCode.MONGODB_INVALID_SEARCH_PARAM)


# Search by pattern
def query_video_search_by_pattern(**kw):
    """
    Search video by pattern
    :param kw: keyword arguments
        :key "pattern_title": (```str```, optional) search title pattern
        :key "pattern_description": (```str```, optional) search description
        pattern
    \nAt least one key must be provided
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
def query_video_search_by_aggregate(aggr: dict or list):
    """
    :param aggr: dict or list of searching param
    :return: array of searching results in dict
    """
    if type(aggr) != list and type(aggr) != dict:
        raise MongoError(ErrorCode.MONGODB_LIST_EXPECTED)
    return list(Video.objects.aggregate(aggr))
