from source.db.mongo import get_db
from source.db.query_video_op import *
from source.utils.util_validator import *
from source.utils.util_serializer import *


def service_video_op_add_view(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw:
        try:
            # Invalid video ID
            if not is_valid_id(kw["video_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            query_video_cnt_incr_by_one(kw["video_id"], "video_view")
            result = query_video_get_by_video_id(kw["video_id"])

            if len(result) == 1:
                video_result = util_serializer_mongo_results_to_array(result)
                video_view = video_result[0]["video_view"]
                return_body = {
                    "video_id": kw["video_id"],
                    "view_count": video_view
                }
                return util_serializer_api_response(200, body=return_body, msg="Successfully add video count by 1")
            else:
                return util_serializer_api_response(500, msg="Failed to add video view count by 1")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))
    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_get_view(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw:
        try:
            # Invalid video ID
            if not is_valid_id(kw["video_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            result = query_video_get_by_video_id(kw["video_id"])

            if len(result) == 1:
                video_result = util_serializer_mongo_results_to_array(result)
                video_view = video_result[0]["video_view"]
                return_body = {
                    "video_id": kw["video_id"],
                    "view_count": video_view
                }
                return util_serializer_api_response(200, body=return_body, msg="Successfully get video count")
            else:
                return util_serializer_api_response(500, msg="Failed to get video view count")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_add_comment(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw and "body" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 0:
                # create a new video_op object for current user and video
                query_video_op_create(kw["user_id"], kw["video_id"])
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            video_op_result = util_serializer_mongo_results_to_array(query_video_op)
            video_op_id = video_op_result[0]["video_op_id"]

            update_result = query_video_op_update_comment(video_op_id, kw["body"]["comment"], get_time_now_utc())

            if update_result == 1:
                query_video_cnt_incr_by_one(kw["video_id"], "video_comment")

                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])
                video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

                return_body = {
                    "user_id": video_op_obj["user_id"],
                    "video_id": video_op_obj["video_id"],
                    "comment": video_op_obj["comment"],
                    "comment_date": str(video_op_obj["comment_date"])
                }

                return util_serializer_api_response(200, body=return_body, msg="Successfully posted comment")
            else:
                return util_serializer_api_response(500, msg="Failed to post comment")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_get_comment(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 0:
                return util_serializer_api_response(400, msg=ErrorCode.MONGODB_VIDEOOP_NOT_FOUND.get_msg())

            video_op_result = util_serializer_mongo_results_to_array(query_video_op)

            if len(video_op_result) == 1:
                video_op_obj = video_op_result[0]

                return_body = {
                    "user_id": video_op_obj["user_id"],
                    "video_id": video_op_obj["video_id"],
                    "comment": video_op_obj["comment"],
                    "comment_date": str(video_op_obj["comment_date"])
                }

                return util_serializer_api_response(200, body=return_body, msg="Successfully got comment")
            else:
                return util_serializer_api_response(500, msg="Failed to get comment")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_update_comment(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw and "body" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 0:
                return util_serializer_api_response(400, msg=ErrorCode.MONGODB_VIDEOOP_NOT_FOUND.get_msg())

            video_op_result = util_serializer_mongo_results_to_array(query_video_op)
            video_op_id = video_op_result[0]["video_op_id"]

            update_result = query_video_op_update_comment(video_op_id, kw["body"]["comment"], get_time_now_utc())

            if update_result == 1:
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])
                video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

                return_body = {
                    "user_id": video_op_obj["user_id"],
                    "video_id": video_op_obj["video_id"],
                    "comment": video_op_obj["comment"],
                    "comment_date": str(video_op_obj["comment_date"])
                }

                return util_serializer_api_response(200, body=return_body, msg="Successfully updated comment")
            else:
                return util_serializer_api_response(500, msg="Failed to update comment")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_cancel_comment(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 0:
                return util_serializer_api_response(400, msg=ErrorCode.MONGODB_VIDEOOP_NOT_FOUND.get_msg())

            video_op_result = util_serializer_mongo_results_to_array(query_video_op)
            video_op_id = video_op_result[0]["video_op_id"]

            update_result = query_video_op_update_comment(video_op_id, "", get_time_now_utc())

            if update_result == 1:
                query_video_cnt_decr_by_one(kw["video_id"], "video_comment")

                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])
                video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

                return_body = {
                    "user_id": video_op_obj["user_id"],
                    "video_id": video_op_obj["video_id"],
                    "comment": video_op_obj["comment"],
                    "comment_date": str(video_op_obj["comment_date"])
                }

                return util_serializer_api_response(200, body=return_body, msg="Successfully delete comment")
            else:
                return util_serializer_api_response(500, msg="Failed to delete comment")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_add_process(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw and "body" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 0:
                # create a new video_op object for current user and video
                query_video_op_create(kw["user_id"], kw["video_id"])
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            video_op_result = util_serializer_mongo_results_to_array(query_video_op)
            video_op_id = video_op_result[0]["video_op_id"]

            if video_op_result[0]["process"] != 0:
                return util_serializer_api_response(400, msg="Process already existed")

            update_result = query_video_op_update_process(video_op_id, kw["body"]["process"], get_time_now_utc())

            if update_result == 1:
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])
                video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

                return_body = {
                    "user_id": video_op_obj["user_id"],
                    "video_id": video_op_obj["video_id"],
                    "process": video_op_obj["process"],
                    "process_date": str(video_op_obj["process_date"])
                }

                return util_serializer_api_response(200, body=return_body, msg="Successfully add video process")
            else:
                return util_serializer_api_response(500, msg="Failed to add video process")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_get_process(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 1:
                video_op_result = util_serializer_mongo_results_to_array(query_video_op)
                video_op_obj = video_op_result[0]

                return_body = {
                    "user_id": video_op_obj["user_id"],
                    "video_id": video_op_obj["video_id"],
                    "process": video_op_obj["process"],
                    "process_date": str(video_op_obj["process_date"])
                }

                return util_serializer_api_response(200, body=return_body, msg="Successfully get video process")
            else:
                return util_serializer_api_response(500, msg="Failed to get video process")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_update_process(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw and "body" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 0:
                # create a new video_op object for current user and video
                query_video_op_create(kw["user_id"], kw["video_id"])
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            video_op_result = util_serializer_mongo_results_to_array(query_video_op)
            video_op_id = video_op_result[0]["video_op_id"]

            update_result = query_video_op_update_process(video_op_id, kw["body"]["process"], get_time_now_utc())

            if update_result == 1:
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])
                video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

                return_body = {
                    "user_id": video_op_obj["user_id"],
                    "video_id": video_op_obj["video_id"],
                    "process": video_op_obj["process"],
                    "process_date": str(video_op_obj["process_date"])
                }

                return util_serializer_api_response(200, body=return_body, msg="Successfully update video process")
            else:
                return util_serializer_api_response(500, msg="Failed to update video process")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_cancel_process(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 0:
                # create a new video_op object for current user and video
                query_video_op_create(kw["user_id"], kw["video_id"])
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            video_op_result = util_serializer_mongo_results_to_array(query_video_op)
            video_op_id = video_op_result[0]["video_op_id"]

            if video_op_result[0]["process"] == 0:
                return util_serializer_api_response(400, msg="Process already set to zero")

            update_result = query_video_op_update_process(video_op_id, 0, get_time_now_utc())

            if update_result == 1:
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])
                video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

                return_body = {
                    "user_id": video_op_obj["user_id"],
                    "video_id": video_op_obj["video_id"],
                    "process": video_op_obj["process"],
                    "process_date": str(video_op_obj["process_date"])
                }

                return util_serializer_api_response(200, body=return_body, msg="Successfully delete video process")
            else:
                return util_serializer_api_response(500, msg="Failed to delete video process")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_add_like(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 0:
                # create a new video_op object for current user and video
                query_video_op_create(kw["user_id"], kw["video_id"])
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            video_op_result = util_serializer_mongo_results_to_array(query_video_op)
            video_op_id = video_op_result[0]["video_op_id"]

            # If already liked, like operation cannot be duplicated
            if video_op_result[0]["like"]:
                return util_serializer_api_response(400, msg="Already liked the video")

            # If already disliked, dislike operation should be set to False
            if video_op_result[0]["dislike"]:
                query_video_op_update_dislike(video_op_id, False)
                query_video_cnt_decr_by_one(kw["video_id"], "video_dislike")

            update_result = query_video_op_update_like(video_op_id, True, get_time_now_utc())

            if update_result == 1:
                query_video_cnt_incr_by_one(kw["video_id"], "video_like")

                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])
                video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

                return_body = {
                    "user_id": video_op_obj["user_id"],
                    "video_id": video_op_obj["video_id"],
                    "like": video_op_obj["like"],
                    "like_date": str(video_op_obj["like_date"]),
                    "dislike": video_op_obj["dislike"],
                    "dislike_date": str(video_op_obj["dislike_date"])
                }

                return util_serializer_api_response(200, body=return_body, msg="Successfully liked the video")
            else:
                return util_serializer_api_response(500, msg="Failed to like the video")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_cancel_like(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 0:
                # create a new video_op object for current user and video
                query_video_op_create(kw["user_id"], kw["video_id"])
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            video_op_result = util_serializer_mongo_results_to_array(query_video_op)
            video_op_id = video_op_result[0]["video_op_id"]

            # Only perform the operation when like is True and dislike is False
            if video_op_result[0]["like"] and not video_op_result[0]["dislike"]:
                update_result = query_video_op_update_like(video_op_id, False, get_time_now_utc())
                if update_result == 1:
                    query_video_cnt_decr_by_one(kw["video_id"], "video_like")

                    query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])
                    video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

                    return_body = {
                        "user_id": video_op_obj["user_id"],
                        "video_id": video_op_obj["video_id"],
                        "like": video_op_obj["like"],
                        "like_date": str(video_op_obj["like_date"]),
                        "dislike": video_op_obj["dislike"],
                        "dislike_date": str(video_op_obj["dislike_date"])
                    }

                    return util_serializer_api_response(200, body=return_body, msg="Successfully undo video like")
                else:
                    return util_serializer_api_response(500, msg="Failed to undo video like")
            else:
                return util_serializer_api_response(400, msg="Video not liked yet")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_add_dislike(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 0:
                # create a new video_op object for current user and video
                query_video_op_create(kw["user_id"], kw["video_id"])
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            video_op_result = util_serializer_mongo_results_to_array(query_video_op)
            video_op_id = video_op_result[0]["video_op_id"]

            # If already disliked, dislike operation cannot be duplicated
            if video_op_result[0]["dislike"]:
                return util_serializer_api_response(400, msg="Already disliked the video")

            # If already liked, like operation should be set to False
            if video_op_result[0]["like"]:
                query_video_op_update_like(video_op_id, False, get_time_now_utc())
                query_video_cnt_decr_by_one(kw["video_id"], "video_like")

            update_result = query_video_op_update_dislike(video_op_id, True, get_time_now_utc())

            if update_result == 1:
                query_video_cnt_incr_by_one(kw["video_id"], "video_dislike")

                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])
                video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

                return_body = {
                    "user_id": video_op_obj["user_id"],
                    "video_id": video_op_obj["video_id"],
                    "like": video_op_obj["like"],
                    "like_date": str(video_op_obj["like_date"]),
                    "dislike": video_op_obj["dislike"],
                    "dislike_date": str(video_op_obj["dislike_date"])
                }

                return util_serializer_api_response(200, body=return_body, msg="Successfully disliked the video")
            else:
                return util_serializer_api_response(500, msg="Failed to dislike the video")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_cancel_dislike(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 0:
                # create a new video_op object for current user and video
                query_video_op_create(kw["user_id"], kw["video_id"])
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            video_op_result = util_serializer_mongo_results_to_array(query_video_op)
            video_op_id = video_op_result[0]["video_op_id"]

            # Only perform the operation when like is False and dislike is True
            if not video_op_result[0]["like"] and video_op_result[0]["dislike"]:
                update_result = query_video_op_update_dislike(video_op_id, False, get_time_now_utc())
                if update_result == 1:
                    query_video_cnt_decr_by_one(kw["video_id"], "video_dislike")

                    query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])
                    video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

                    return_body = {
                        "user_id": video_op_obj["user_id"],
                        "video_id": video_op_obj["video_id"],
                        "like": video_op_obj["like"],
                        "like_date": str(video_op_obj["like_date"]),
                        "dislike": video_op_obj["dislike"],
                        "dislike_date": str(video_op_obj["dislike_date"])
                    }

                    return util_serializer_api_response(200, body=return_body, msg="Successfully undo video dislike")
                else:
                    return util_serializer_api_response(500, msg="Failed to undo video dislike")
            else:
                return util_serializer_api_response(400, msg="Video not disliked yet")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_add_star(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 0:
                # create a new video_op object for current user and video
                query_video_op_create(kw["user_id"], kw["video_id"])
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            video_op_result = util_serializer_mongo_results_to_array(query_video_op)
            video_op_id = video_op_result[0]["video_op_id"]

            # If already starred, star operation cannot be duplicated
            if video_op_result[0]["star"]:
                return util_serializer_api_response(400, msg="Already starred the video")

            update_result = query_video_op_update_star(video_op_id, True, get_time_now_utc())

            if update_result == 1:
                query_video_cnt_incr_by_one(kw["video_id"], "video_star")

                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])
                video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

                return_body = {
                    "user_id": video_op_obj["user_id"],
                    "video_id": video_op_obj["video_id"],
                    "star": video_op_obj["star"],
                    "star_date": str(video_op_obj["star_date"])
                }

                return util_serializer_api_response(200, body=return_body, msg="Successfully starred the video")
            else:
                return util_serializer_api_response(500, msg="Failed to star the video")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_cancel_star(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "user_id" in kw:
        try:
            # Invalid video ID or user ID
            if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            # check if the video_op object exists
            query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            if len(query_video_op) == 0:
                # create a new video_op object for current user and video
                query_video_op_create(kw["user_id"], kw["video_id"])
                query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])

            video_op_result = util_serializer_mongo_results_to_array(query_video_op)
            video_op_id = video_op_result[0]["video_op_id"]

            # Only perform the operation when star is True
            if video_op_result[0]["star"]:
                update_result = query_video_op_update_star(video_op_id, False, get_time_now_utc())
                if update_result == 1:
                    query_video_cnt_decr_by_one(kw["video_id"], "video_star")

                    query_video_op = query_video_op_get_by_user_video(kw["user_id"], kw["video_id"])
                    video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

                    return_body = {
                        "user_id": video_op_obj["user_id"],
                        "video_id": video_op_obj["video_id"],
                        "star": video_op_obj["star"],
                        "star_date": str(video_op_obj["star_date"])
                    }

                    return util_serializer_api_response(200, body=return_body, msg="Successfully undo video star")
                else:
                    return util_serializer_api_response(500, msg="Failed to undo video star")
            else:
                return util_serializer_api_response(400, msg="Video not starred yet")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())
