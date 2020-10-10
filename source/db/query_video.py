from source.models import Video
import bson

def video_get_by_id(video_id: str):
    """
    :return: an array of such Video (len == 0 or 1), len == 0 if no such video_id, len == 1 if found
    """
    return Video.objects(_id=bson.ObjectId(video_id))