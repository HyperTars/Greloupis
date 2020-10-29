# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from source.utils.util_serializer import util_serializer_api_response, \
    extract_error_msg
from source.models.model_errors import MongoError, RouteError, ServiceError


def util_error_handler(e):
    if type(e) == RouteError:
        return util_serializer_api_response(404, error_code=e.get_code(),
                                            msg=e.get_msg())
    elif type(e) == ServiceError:
        if e.get_code() == 3004 or e.get_code() == 3011:
            return util_serializer_api_response(404, error_code=e.get_code(),
                                                msg=e.get_msg())
        else:
            return util_serializer_api_response(400, error_code=e.get_code(),
                                                msg=e.get_msg())
    elif type(e) == MongoError:
        if 4101 <= e.get_code() <= 4103:
            return util_serializer_api_response(404, error_code=e.get_code(),
                                                msg=e.get_msg())
        else:
            return util_serializer_api_response(500, error_code=e.get_code(),
                                                msg=e.get_msg())
    elif type(e) == Exception:
        return util_serializer_api_response(500, msg=extract_error_msg(str(e)))
    else:
        return util_serializer_api_response(503, msg=extract_error_msg(str(e)))
