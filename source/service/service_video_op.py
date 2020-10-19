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

        except Exception as e:
            result = extract_error_msg(str(e))

    else:
        result = [{}]

    if len(result) == 1:
        video_result_json = util_serializer_mongo_results_to_array(result, format="json")
        video_view = json.loads(video_result_json[0])["video_view"]
        return_body ={
            "video_id": kw["video_id"],
            "view_count": video_view
        }
        return util_serializer_api_response(200, body=return_body, msg="Successfully add video count by 1")
    else:
        return util_serializer_api_response(500, msg="Failed to add video view count by 1")


def service_video_op_get_view(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw:
        try:
            # Invalid video ID
            if not is_valid_id(kw["video_id"]):
                return util_serializer_api_response(400, msg=ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

            result = query_video_get_by_video_id(kw["video_id"])
        except Exception as e:
            result = extract_error_msg(str(e))

    else:
        result = [{}]

    if len(result) == 1:
        video_result_json = util_serializer_mongo_results_to_array(result, format="json")
        video_view = json.loads(video_result_json[0])["video_view"]
        return_body ={
            "video_id": kw["video_id"],
            "view_count": video_view
        }
        return util_serializer_api_response(200, body=return_body, msg="Successfully get video count")
    else:
        return util_serializer_api_response(500, msg="Failed to get video view count")


def service_video_op_add_comment():
    return


def service_video_op_update_comment():
    return


def service_video_op_cancel_comment():
    return


def service_video_op_add_process():
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
