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

            update_result = query_video_op_update_comment(video_op_id, kw["body"]["comment"])

            if update_result == 1:
                query_video_cnt_incr_by_one(kw["video_id"], "video_comment")
                return util_serializer_api_response(200, msg="Successfully posted comment")
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
                video_op_comment = video_op_result[0]["comment"]

                return_body = {
                    "comment": video_op_comment
                }

                return util_serializer_api_response(200, body=return_body, msg="Successfully get comment")
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

            update_result = query_video_op_update_comment(video_op_id, kw["body"]["comment"])

            if update_result == 1:
                return util_serializer_api_response(200, msg="Successfully updated comment")
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

            update_result = query_video_op_update_comment(video_op_id, "")

            if update_result == 1:
                query_video_cnt_decr_by_one(kw["video_id"], "video_comment")
                return util_serializer_api_response(200, msg="Successfully delete comment")
            else:
                return util_serializer_api_response(500, msg="Failed to delete comment")

        except Exception as e:
            return util_serializer_api_response(500, msg=extract_error_msg(str(e)))

    else:
        return util_serializer_api_response(400, msg=ErrorCode.SERVICE_MISSING_PARAM.get_msg())


def service_video_op_add_process():
    return


def service_video_op_get_process():
    return


def service_video_op_update_process():
    return


def service_video_op_cancel_process():
    return


def service_video_op_add_like():
    return


def service_video_op_cancel_like():
    return


def service_video_op_add_dislike():
    return


def service_video_op_cancel_dislike():
    return


def service_video_op_add_star():
    return


def service_video_op_cancel_star():
    return
