from source.db.mongo import get_db
from source.db.query_user import *
from source.db.query_video import *
from source.db.query_video_op import *
from source.utils.util_pattern import *
from source.utils.util_serializer import *
from source.utils.util_validator import *
from source.models.model_errors import *


def service_video_upload(conf, **kw):
    db = get_db(conf)

    # new
    kw['service'] = 'video'
    if 'user_id' not in kw and 'id' not in kw and '_id' not in kw or \
            'video_title' not in kw and 'title' not in kw or \
            'video_raw_content' and 'raw_content' not in kw and 'content' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw = util_pattern_format_param(**kw)
    try:
        query_video_create(kw['user_id'], kw['video_title'], kw['video_raw_content'])
        result_mongo = query_video_get_by_title(kw['video_title'])
        result_array = util_serializer_mongo_results_to_array(result_mongo)
    except MongoError as e:
        print(e.get_code())
        print(e.get_msg())
        raise e
    except Exception as e:
        raise e
    return result_array  # Convert to api response in route

    # original version
    if "body" in kw:
        user_id = kw["body"]["user_id"]
        video_title = kw["body"]["video_title"]
        video_raw_content = kw["body"]["video_raw_content"]

        try:
            query_video_create(user_id=user_id, video_title=video_title, video_raw_content=video_raw_content)

            # get the video by title
            result = query_video_get_by_title(kw["body"]["video_title"])

            if len(result) == 1:
                post_result_json = util_serializer_mongo_results_to_array(result, format="json")
                return util_serializer_api_response(200, body=post_result_json, msg="Successfully uploaded video")
            else:
                return util_serializer_api_response(500, msg="Failed to upload video")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_info(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw:
        try:
            if not is_valid_id(kw["video_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            result = query_video_get_by_video_id(kw["video_id"])

            # Check if find result in database
            if len(result) == 1:
                search_result_json = util_serializer_mongo_results_to_array(result, format="json")
                return util_serializer_api_response(200, body=search_result_json, msg="Successfully got video by ID")
            else:
                return util_serializer_api_response(404, msg="Video not found")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_update(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "body" in kw:
        try:
            # Invalid video id
            if not is_valid_id(kw["video_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            result = query_video_get_by_video_id(kw["video_id"])
            if len(result) == 0:
                return util_serializer_api_response(400, msg=ErrorCode.MONGODB_VIDEO_NOT_FOUND.get_msg())

            original = util_serializer_mongo_results_to_array(result)[0]

            video_title = kw["body"]["video_title"] if 'video_title' in kw["body"] \
                else original["video_title"]
            video_raw_content = kw["body"]["video_raw_content"] if 'video_raw_content' in kw["body"] \
                else original["video_raw_content"]
            video_raw_status = kw["body"]["video_raw_status"] if 'video_raw_status' in kw["body"] \
                else original["video_raw_status"]
            video_raw_size = kw["body"]["video_raw_size"] if 'video_raw_size' in kw["body"] \
                else original["video_raw_size"]
            video_duration = int(kw["body"]["video_duration"]) if 'video_duration' in kw["body"] \
                else int(original["video_duration"])
            video_channel = kw["body"]["video_channel"] if 'video_channel' in kw["body"] \
                else original["video_channel"]
            video_tag = kw["body"]["video_tag"] if 'video_tag' in kw["body"] \
                else original["video_tag"]
            video_category = kw["body"]["video_category"] if 'video_category' in kw["body"] \
                else original["video_category"]
            video_description = kw["body"]["video_description"] if 'video_description' in kw["body"] \
                else original["video_description"]
            video_language = kw["body"]["video_language"] if 'video_language' in kw["body"] \
                else original["video_language"]
            video_status = kw["body"]["video_status"] if 'video_status' in kw["body"] \
                else original["video_status"]
            video_thumbnail = kw["body"]["video_thumbnail"] if 'video_thumbnail' in kw["body"] \
                else original["video_thumbnail"]
            video_uri_low = kw["body"]["video_uri_low"] if 'video_uri_low' in kw["body"] \
                else original["video_uri"]["video_uri_low"]
            video_uri_mid = kw["body"]["video_uri_mid"] if 'video_uri_mid' in kw["body"] \
                else original["video_uri"]["video_uri_mid"]
            video_uri_high = kw["body"]["video_uri_high"] if 'video_uri_high' in kw["body"] \
                else original["video_uri"]["video_uri_high"]

            query_video_update(video_id=kw["video_id"], video_title=video_title,
                               video_raw_content=video_raw_content, video_raw_status=video_raw_status,
                               video_raw_size=video_raw_size, video_channel=video_channel,
                               video_duration=video_duration, video_tag=video_tag,
                               video_category=video_category, video_description=video_description,
                               video_language=video_language, video_status=video_status,
                               video_thumbnail=video_thumbnail, video_uri_low=video_uri_low,
                               video_uri_mid=video_uri_mid, video_uri_high=video_uri_high)

            # get the video by ID
            result = query_video_get_by_video_id(kw["video_id"])

            # Check if find result in database
            if len(result) == 1:
                update_result_json = util_serializer_mongo_results_to_array(result, format="json")
                return util_serializer_api_response(200, body=update_result_json, msg="Successfully updated video")
            else:
                return util_serializer_api_response(500, msg=ErrorCode.MONGODB_VIDEO_UPDATE_FAILURE.get_msg())

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_delete(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw:
        try:
            # Invalid video ID
            if not is_valid_id(kw["video_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            result = query_video_delete(kw["video_id"])

            if result == 1:
                # delete all video_op related to this video
                video_op_objects = query_video_op_get_by_video_id(kw["video_id"])
                video_op_results = util_serializer_mongo_results_to_array(video_op_objects)
                for each in video_op_results:
                    query_video_op_delete(each["video_op_id"])

                return util_serializer_api_response(200, msg="Successfully deleted video by ID")
            else:
                return util_serializer_api_response(500, msg=result)

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_comments(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw:
        try:
            # Invalid video ID
            if not is_valid_id(kw["video_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            result = query_video_op_get_by_video_id(kw["video_id"])

            if len(result) > 0:
                search_result = util_serializer_mongo_results_to_array(result)

                return_result = []
                for each in search_result:
                    if each["comment"] != "":
                        return_result.append({
                            "video_id": each["video_id"],
                            "user_id": each["user_id"],
                            "comment": each["comment"],
                            "comment_date": str(each["comment_date"])
                        })

                return util_serializer_api_response(200, body=return_result, msg="Successfully got all comments")
            else:
                return util_serializer_api_response(500, msg="Failed to get all comments")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_likes(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw:
        try:
            # Invalid video ID
            if not is_valid_id(kw["video_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            result = query_video_op_get_by_video_id(kw["video_id"])

            if len(result) > 0:
                search_result = util_serializer_mongo_results_to_array(result)

                return_result = []
                for each in search_result:
                    if each["like"]:
                        return_result.append({
                            "video_id": each["video_id"],
                            "user_id": each["user_id"],
                            "like_date": str(each["like_date"])
                        })

                return util_serializer_api_response(200, body=return_result, msg="Successfully got all like users")
            else:
                return util_serializer_api_response(500, msg="Failed to get all like users")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_dislikes(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw:
        try:
            # Invalid video ID
            if not is_valid_id(kw["video_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            result = query_video_op_get_by_video_id(kw["video_id"])

            if len(result) > 0:
                search_result = util_serializer_mongo_results_to_array(result)

                return_result = []
                for each in search_result:
                    if each["dislike"]:
                        return_result.append({
                            "video_id": each["video_id"],
                            "user_id": each["user_id"],
                            "dislike_date": str(each["dislike_date"])
                        })

                return util_serializer_api_response(200, body=return_result, msg="Successfully got all dislike users")
            else:
                return util_serializer_api_response(500, msg="Failed to get all dislike users")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_stars(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw:
        try:
            # Invalid video ID
            if not is_valid_id(kw["video_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            result = query_video_op_get_by_video_id(kw["video_id"])

            if len(result) > 0:
                search_result = util_serializer_mongo_results_to_array(result)

                return_result = []
                for each in search_result:
                    if each["star"]:
                        return_result.append({
                            "video_id": each["video_id"],
                            "user_id": each["user_id"],
                            "star_date": str(each["star_date"])
                        })

                return util_serializer_api_response(200, body=return_result, msg="Successfully got all star users")
            else:
                return util_serializer_api_response(500, msg="Failed to get all star users")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())
