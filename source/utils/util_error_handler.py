# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace

from source.utils.util_serializer import *
from source.models.model_errors import *


def util_error_handler(e):
    if type(e) == RouteError:
        return util_serializer_api_response(404, error_code=e.get_code(), msg=e.get_msg())
    elif type(e) == ServiceError:
        return util_serializer_api_response(400, error_code=e.get_code(), msg=e.get_msg())
    elif type(e) == MongoError:
        if 4101 <= e.get_code() <= 4103:
            return util_serializer_api_response(404, error_code=e.get_code(), msg=e.get_msg())
        else:
            return util_serializer_api_response(500, error_code=e.get_code(), msg=e.get_msg())
    elif type(e) == Exception:
        return util_serializer_api_response(500, msg=extract_error_msg(str(e)))
    else:
        return util_serializer_api_response(503, msg=extract_error_msg(str(e)))
