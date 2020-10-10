from source.models.video import Video, Thumbnail, VideoURI
from source.db.query_user import user_get_by_id
from source.models.errors import ErrorCode
import bson
import datetime


def video_get_by_id(video_id: str):
    """
    :return: an array of such Video (len == 0 or 1), len == 0 if no such video_id, len == 1 if found
    """
    return Video.objects(_id=bson.ObjectId(video_id))


def video_get_by_title(video_title: str):
    """
    :return: an array of such Video (len == 0 or 1), len == 0 if no such video_id, len == 1 if found
    """
    return Video.objects(video_title=video_title)


def video_create(user_id: str, video_title: str, video_raw_content: str, **kw):
    # video_raw_content description:
    # user will get a raw video URI after uploading raw video to cache (temp storage space where videos waiting for being transcoded)
    # transcoder will start transcoding, but user can create a video now
    """
    :param user_id (required): user's unique id
    :param video_title (required): video's title
    :param video_raw_content (required): URI of raw video data (in temp space, to be transcode)
    :param video_raw_status (optional): status of raw video data, default: pending
    :param video_raw_size (optional): size of raw video data
    :param video_tag (optional): array of video's tags
    :param video_category (optional): array of video's categories
    :param video_description (optional): video's description
    :param video_language (optional): video's language
    :param video_status (optional): video's status, default: public
    :param video_thumbnail_uri (optional): video's thumbnail uri
    :param video_thumbnail_type (optional): video's thumbnail type
    :param video_upload_date (optional): video's upload date
    :return: video created (Video Model)
    """

    if len(user_get_by_id(user_id)) == 0:
        return ErrorCode.MONGODB_USER_NOT_FOUND

    if len(video_get_by_title(video_title)) > 0:
        return ErrorCode.MONGODB_VIDEO_TITLE_TAKEN

    # Default
    video_raw_status = "pending"
    video_raw_size = 0.00
    video_tag = []
    video_category = []
    video_description = ""
    video_language = ""
    video_status = "public"
    video_thumbnail = Thumbnail()
    video_upload_date = datetime.datetime.utcnow()

    # Fill if exist
    if 'video_raw_status' in kw:
        video_raw_status = kw['video_raw_status']
    if 'video_raw_size' in kw:
        video_raw_size = kw['video_raw_size']
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
    if 'video_thumbnail_uri' in kw and 'video_thumbnail_type' in kw:
        video_thumbnail = Thumbnail(thumbnail_uri=kw['video_thumbnail_uri'], thumbnail_type=kw['video_thumbnail_type'])
    if 'video_upload_date' in kw:
        video_upload_date = kw['upload_date']

    # Construct Video Model
    video = Video(user_id=user_id, video_title=video_title, video_raw_content=video_raw_content,
                  video_raw_status=video_raw_status, video_raw_size=video_raw_size, video_tag=video_tag,
                  video_category=video_category, video_description=video_description, video_language=video_language,
                  video_status=video_status, video_view=0, video_comment=0, video_like=0, video_dislike=0,
                  video_star=0, video_share=0, video_thumbnail=video_thumbnail, video_upload_date=video_upload_date,
                  video_uri=VideoURI())

    return video.save()


def video_update(video_id: str, **kw):
    """
    :param video_title (optional): video's new title
    :param video_raw_content (optional): new URI of raw video data (in temp space, to be transcode)
    :param video_raw_status (optional): new status of raw video data, default
    :param video_raw_size (optional): new size of raw video data
    :param video_tag (optional): array of video's new tags
    :param video_category (optional): array of video's new categories
    :param video_description (optional): video's new description
    :param video_language (optional): video's new language
    :param video_status (optional): video's new status, default: public
    
    :param video_view (optional): new total number of video's views, default = 0
    :param video_comment (optional): new total number of video's comments, default = 0
    :param video_like (optional): new total number of video's likes, default = 0
    :param video_dislike (optional): new total number of video's dislikes, default = 0
    :param video_star (optional): new total number of video's stars, default = 0
    :param video_share (optional): new total number of video's shares, default = 0
    
    :param video_thumbnail_uri (optional): video's new thumbnail uri
    :param video_thumbnail_type (optional): video's new thumbnail type
    :param video_uri_low (optional): video's new final uri (480p low resolution)
    :param video_uri_mid (optional): video's new final uri (720p mid resolution)
    :param video_uri_high (optional): video's new final uri (1080p high resolution)
    """

    if len(video_get_by_id(video_id)) == 0:
        return ErrorCode.MONGODB_VIDEO_NOT_FOUND

    id = bson.ObjectId(video_id)

    if 'video_title' in kw:
        videos = video_get_by_title(kw['video_title'])
        if len(videos) == 0:
            return ErrorCode.MONGODB_VIDEO_TITLE_TAKEN
        Video.objects(_id=id).update(video_title=kw['video_title'])
    if 'video_raw_content' in kw:
        Video.objects(_id=id).update(video_raw_content=kw['video_raw_content'])
    if 'video_raw_status' in kw:
        Video.objects(_id=id).update(video_status=kw['video_raw_status'])
    if 'video_raw_size' in kw:
        Video.objects(_id=id).update(video_raw_size=kw['video_raw_size'])
    if 'video_tag' in kw:
        if type(kw['video_tag']) is not list:
            return ErrorCode.MONGODB_EXPECT_LIST
        Video.objects(_id=id).update(video_tag=kw['video_tag'])
    if 'video_category' in kw:
        if type(kw['video_category']) is not list:
            return ErrorCode.MONGODB_EXPECT_LIST
        Video.objects(_id=id).update(video_categoty=kw['video_category'])
    if 'video_description' in kw:
        Video.objects(_id=id).update(video_description=kw['video_description'])
    if 'video_language' in kw:
        Video.objects(_id=id).update(video_language=kw['video_language'])
    if 'video_status' in kw:
        Video.objects(_id=id).update(video_language=kw['video_status'])
    if 'video_thumbnail_uri' in kw and 'video_thumbnail_type' in kw:
        video_thumbnail = Thumbnail(thumbnail_uri=kw['video_thumbnail_uri'], thumbnail_type=kw['video_thumbnail_type'])
        Video.objects(_id=id).update(video_thumbnail=video_thumbnail)
    if 'video_thumbnail_uri' in kw or 'video_thumbnail_type' in kw:
        return ErrorCode.MONGODB_THUMBNAIL_MISS_ONE
    if 'video_uri_low' in kw:
        Video.objects(_id=id).update(set__video_uri__video_low=kw['video_uri_low'])
    if 'video_uri_mid' in kw:
        Video.objects(_id=id).update(set__video_uri__video_mid=kw['video_uri_mid'])
    if 'video_uri_high' in kw:
        Video.objects(_id=id).update(set__video_uri__video_high=kw['video_uri_high'])

def video_delete(video_id: str):
    """
    :param video_id: video's unique id
    :return: 1 if succeeded, -1 if no such video
    """
    videos = video_get_by_id(video_id)
    if len(videos) == 0:
        # print("No such video")
        return -1  # TODO: error_code
    return Video.objects(_id=bson.ObjectId(video_id)).delete()
