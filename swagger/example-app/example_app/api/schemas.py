# -*- coding: utf-8 -*-

import six
from jsonschema import RefResolver
# TODO: datetime support

class RefNode(object):

    def __init__(self, data, ref):
        self.ref = ref
        self._data = data

    def __getitem__(self, key):
        return self._data.__getitem__(key)

    def __setitem__(self, key, value):
        return self._data.__setitem__(key, value)

    def __getattr__(self, key):
        return self._data.__getattribute__(key)

    def __iter__(self):
        return self._data.__iter__()

    def __repr__(self):
        return repr({'$ref': self.ref})

    def __eq__(self, other):
        if isinstance(other, RefNode):
            return self._data == other._data and self.ref == other.ref
        elif six.PY2:
            return object.__eq__(other)
        elif six.PY3:
            return object.__eq__(self, other)
        else:
            return False

    def __deepcopy__(self, memo):
        return RefNode(copy.deepcopy(self._data), self.ref)

    def copy(self):
        return RefNode(self._data, self.ref)

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###

base_path = '/api'

definitions = {'definitions': {'AddressDetail': {'type': 'object', 'properties': {'street1': {'type': 'string'}, 'street2': {'type': 'string'}, 'city': {'type': 'string'}, 'state': {'type': 'string'}, 'country': {'type': 'string'}, 'zip': {'type': 'string'}}, 'xml': {'name': 'AddresDetail'}}, 'UserDetail': {'type': 'object', 'required': ['first_name', 'last_name', 'phone'], 'properties': {'first_name': {'type': 'string'}, 'last_name': {'type': 'string'}, 'phone': {'type': 'string'}, 'address': {'$ref': '#/definitions/AddressDetail'}}, 'xml': {'name': 'UserDetail'}}, 'LoginDetail': {'type': 'object', 'properties': {'login_ip': {'type': 'string'}, 'login_time': {'type': 'string', 'format': 'date-time'}}, 'xml': {'name': 'LoginDetail'}}, 'VideoURI': {'type': 'object', 'properties': {'video_low': {'type': 'string'}, 'video_mid': {'type': 'string'}, 'video_high': {'type': 'string'}}, 'xml': {'name': 'VideoURI'}}, 'Thumbnail': {'type': 'object', 'required': ['thumbnail_type'], 'properties': {'thumbnail_uri': {'type': 'string'}, 'thumbnail_type': {'type': 'string', 'enum': ['system default', 'user upload', 'auto first frame']}}, 'xml': {'name': 'Thumbnail'}}, 'User': {'type': 'object', 'required': ['user_email', 'user_name'], 'properties': {'user_id': {'type': 'string'}, 'user_name': {'type': 'string'}, 'user_password': {'type': 'string'}, 'user_detail': {'$ref': '#/definitions/UserDetail'}, 'user_status': {'type': 'string', 'enum': ['public', 'private', 'closed']}, 'user_thumbnail': {'$ref': '#/definitions/Thumbnail'}, 'user_follower': {'type': 'integer', 'format': 'int64'}, 'user_reg_date': {'type': 'string', 'format': 'date-time'}, 'user_recent_login': {'type': 'array', 'xml': {'name': 'login_detail', 'wrapped': True}, 'items': {'$ref': '#/definitions/LoginDetail'}}}, 'xml': {'name': 'User'}}, 'UserInput': {'type': 'object', 'required': ['user_email', 'user_name', 'user_password'], 'properties': {'user_email': {'type': 'string'}, 'user_name': {'type': 'string'}, 'user_password': {'type': 'string'}, 'user_detail': {'$ref': '#/definitions/UserDetail'}}, 'xml': {'name': 'UserInput'}}, 'Follow': {'type': 'object', 'properties': {'follow_uploader': {'type': 'string'}, 'follow_by': {'type': 'string'}, 'follow_date': {'type': 'string', 'format': 'date-time'}}, 'xml': {'name': 'Follow'}}, 'History': {'type': 'object', 'properties': {'history_id': {'type': 'string'}, 'user_id': {'type': 'string'}, 'video_id': {'type': 'string'}, 'process': {'type': 'string', 'format': 'date-time'}}, 'xml': {'name': 'History'}}, 'Video': {'type': 'object', 'required': ['video_title'], 'properties': {'video_id': {'type': 'string'}, 'user_id': {'type': 'string'}, 'video_title': {'type': 'string'}, 'video_tag': {'type': 'array', 'xml': {'name': 'tg', 'wrapped': True}, 'items': {'type': 'string'}}, 'video_category': {'type': 'array', 'xml': {'name': 'cat', 'wrapped': True}, 'items': {'type': 'string'}}, 'video_description': {'type': 'string'}, 'video_language': {'type': 'string', 'example': 'English'}, 'video_status': {'type': 'string', 'enum': ['public', 'private', 'limited', 'deleted']}, 'video_content': {'type': 'string'}, 'video_content_status': {'type': 'string', 'enum': ['pending', 'processing', 'finished', 'failed', 'rejected']}, 'video_size': {'type': 'string'}, 'video_view': {'type': 'integer', 'format': 'int64'}, 'video_like': {'type': 'integer', 'format': 'int64'}, 'video_dislike': {'type': 'integer', 'format': 'int64'}, 'video_comment': {'type': 'integer', 'format': 'int64'}, 'video_star': {'type': 'integer', 'format': 'int64'}, 'video_share': {'type': 'integer', 'format': 'int64'}, 'video_thumbnail': {'$ref': '#/definitions/Thumbnail'}, 'video_upload_date': {'type': 'string', 'format': 'date-time'}, 'video_uri': {'$ref': '#/definitions/VideoURI'}}, 'xml': {'name': 'Video'}}, 'VideoInput': {'type': 'object', 'properties': {'video_title': {'type': 'string'}, 'video_category': {'type': 'array', 'items': {'type': 'string'}}, 'video_tags': {'type': 'array', 'items': {'type': 'string'}}, 'video_description': {'type': 'string'}, 'video_language': {'type': 'string', 'example': 'English'}}, 'xml': {'name': 'User'}}, 'Comment': {'type': 'object', 'required': ['comment'], 'properties': {'comment_id': {'type': 'string'}, 'user_id': {'type': 'string'}, 'video_id': {'type': 'string'}, 'comment': {'type': 'string'}, 'comment_date': {'type': 'string', 'format': 'date-time'}}, 'xml': {'name': 'Comment'}}, 'CommentInput': {'type': 'object', 'required': ['comment'], 'properties': {'comment': {'type': 'string'}}, 'xml': {'name': 'CommentInput'}}, 'Like': {'type': 'object', 'properties': {'like_id': {'type': 'string'}, 'user_id': {'type': 'string'}, 'video_id': {'type': 'string'}, 'like_date': {'type': 'string', 'format': 'date-time'}}, 'xml': {'name': 'Like'}}, 'Dislike': {'type': 'object', 'properties': {'dislike_id': {'type': 'string'}, 'user_id': {'type': 'string'}, 'video_id': {'type': 'string'}, 'dislike_date': {'type': 'string', 'format': 'date-time'}}, 'xml': {'name': 'Dislike'}}, 'Star': {'type': 'object', 'properties': {'star_id': {'type': 'string'}, 'user_id': {'type': 'string'}, 'video_id': {'type': 'string'}, 'star_date': {'type': 'string', 'format': 'date-time'}}, 'xml': {'name': 'Star'}}, 'ApiResponse': {'type': 'object', 'properties': {'code': {'type': 'integer', 'format': 'int32'}, 'message': {'type': 'string'}}}, 'ApiResponseWithUser': {'type': 'object', 'properties': {'code': {'type': 'integer', 'format': 'int32'}, 'message': {'$ref': '#/definitions/User'}}}, 'ApiResponseWithVideo': {'type': 'object', 'properties': {'code': {'type': 'integer', 'format': 'int32'}, 'message': {'$ref': '#/definitions/Video'}}}, 'ApiResponseWithList': {'type': 'object', 'properties': {'code': {'type': 'integer', 'format': 'int32'}, 'message': {'type': 'array', 'items': {'type': 'string'}}}}}, 'parameters': {}}

validators = {
    ('user', 'POST'): {'json': {'$ref': '#/definitions/UserInput'}},
    ('user_login', 'POST'): {'form': {'required': ['user_name', 'user_email', 'user_password'], 'properties': {'user_name': {'description': "user's name", 'type': 'string'}, 'user_email': {'description': "user's name", 'type': 'string'}, 'user_password': {'description': "user's name", 'type': 'string'}}}},
    ('user_user_id', 'PUT'): {'json': {'$ref': '#/definitions/UserInput'}},
    ('video', 'POST'): {'json': {'$ref': '#/definitions/VideoInput'}},
    ('video_video_id', 'PUT'): {'json': {'$ref': '#/definitions/VideoInput'}},
    ('search_video', 'GET'): {'args': {'required': ['keyword'], 'properties': {'keyword': {'description': "video's keyword", 'type': 'string'}}}},
    ('search_user', 'GET'): {'args': {'required': ['keyword'], 'properties': {'keyword': {'description': "user's keyword", 'type': 'string'}}}},
    ('video_video_id_comment_user_id', 'POST'): {'json': {'$ref': '#/definitions/CommentInput'}},
    ('video_video_id_comment_user_id', 'PUT'): {'json': {'$ref': '#/definitions/CommentInput'}},
}

filters = {
    ('user', 'POST'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithUser'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('user_login', 'POST'): {200: {'headers': {'X-Expires-After': {'type': 'string', 'format': 'date-time', 'description': 'date in UTC when token expires'}, 'X-Rate-Limit': {'type': 'integer', 'format': 'int32', 'description': 'calls per hour allowed by the user'}}, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('user_logout', 'POST'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('user_user_id', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithUser'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('user_user_id', 'PUT'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithUser'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('user_user_id', 'DELETE'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video', 'POST'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithVideo'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithVideo'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id', 'PUT'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithUser'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id', 'DELETE'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('search_video', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithList'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('search_user', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithList'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('user_user_id_like', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithList'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_like', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithList'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_like_user_id', 'POST'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithList'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_like_user_id', 'DELETE'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('user_user_id_dislike', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithList'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_dislike', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithList'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_dislike_user_id', 'POST'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithList'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_dislike_user_id', 'DELETE'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('user_user_id_star', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithList'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_star', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithList'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_star_user_id', 'POST'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithList'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_star_user_id', 'DELETE'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_view', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_view', 'PUT'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('user_user_id_comment', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithList'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_comment', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponseWithList'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_comment_user_id', 'GET'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_comment_user_id', 'POST'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_comment_user_id', 'PUT'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
    ('video_video_id_comment_user_id', 'DELETE'): {200: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 400: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 404: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 405: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}, 500: {'headers': None, 'schema': {'$ref': '#/definitions/ApiResponse'}}},
}

scopes = {
    ('user', 'POST'): [],
    ('user_login', 'POST'): [],
    ('user_logout', 'POST'): [],
    ('user_user_id', 'GET'): [],
    ('user_user_id', 'PUT'): [],
    ('user_user_id', 'DELETE'): [],
    ('video', 'POST'): [],
    ('video_video_id', 'GET'): [],
    ('video_video_id', 'PUT'): [],
    ('video_video_id', 'DELETE'): [],
    ('search_video', 'GET'): [],
    ('search_user', 'GET'): [],
    ('user_user_id_like', 'GET'): [],
    ('video_video_id_like', 'GET'): [],
    ('video_video_id_like_user_id', 'POST'): [],
    ('video_video_id_like_user_id', 'DELETE'): [],
    ('user_user_id_dislike', 'GET'): [],
    ('video_video_id_dislike', 'GET'): [],
    ('video_video_id_dislike_user_id', 'POST'): [],
    ('video_video_id_dislike_user_id', 'DELETE'): [],
    ('user_user_id_star', 'GET'): [],
    ('video_video_id_star', 'GET'): [],
    ('video_video_id_star_user_id', 'POST'): [],
    ('video_video_id_star_user_id', 'DELETE'): [],
    ('video_video_id_view', 'GET'): [],
    ('video_video_id_view', 'PUT'): [],
    ('user_user_id_comment', 'GET'): [],
    ('video_video_id_comment', 'GET'): [],
    ('video_video_id_comment_user_id', 'GET'): [],
    ('video_video_id_comment_user_id', 'POST'): [],
    ('video_video_id_comment_user_id', 'PUT'): [],
    ('video_video_id_comment_user_id', 'DELETE'): [],
}

resolver = RefResolver.from_schema(definitions)

class Security(object):

    def __init__(self):
        super(Security, self).__init__()
        self._loader = lambda: []

    @property
    def scopes(self):
        return self._loader()

    def scopes_loader(self, func):
        self._loader = func
        return func

security = Security()


def merge_default(schema, value, get_first=True, resolver=None):
    # TODO: more types support
    type_defaults = {
        'integer': 9573,
        'string': 'something',
        'object': {},
        'array': [],
        'boolean': False
    }

    results = normalize(schema, value, type_defaults, resolver=resolver)
    if get_first:
        return results[0]
    return results


def normalize(schema, data, required_defaults=None, resolver=None):
    if required_defaults is None:
        required_defaults = {}
    errors = []

    class DataWrapper(object):

        def __init__(self, data):
            super(DataWrapper, self).__init__()
            self.data = data

        def get(self, key, default=None):
            if isinstance(self.data, dict):
                return self.data.get(key, default)
            return getattr(self.data, key, default)

        def has(self, key):
            if isinstance(self.data, dict):
                return key in self.data
            return hasattr(self.data, key)

        def keys(self):
            if isinstance(self.data, dict):
                return list(self.data.keys())
            return list(getattr(self.data, '__dict__', {}).keys())

        def get_check(self, key, default=None):
            if isinstance(self.data, dict):
                value = self.data.get(key, default)
                has_key = key in self.data
            else:
                try:
                    value = getattr(self.data, key)
                except AttributeError:
                    value = default
                    has_key = False
                else:
                    has_key = True
            return value, has_key

    def _merge_dict(src, dst):
        for k, v in six.iteritems(dst):
            if isinstance(src, dict):
                if isinstance(v, dict):
                    r = _merge_dict(src.get(k, {}), v)
                    src[k] = r
                else:
                    src[k] = v
            else:
                src = {k: v}
        return src

    def _normalize_dict(schema, data):
        result = {}
        if not isinstance(data, DataWrapper):
            data = DataWrapper(data)

        for _schema in schema.get('allOf', []):
            rs_component = _normalize(_schema, data)
            _merge_dict(result, rs_component)

        for key, _schema in six.iteritems(schema.get('properties', {})):
            # set default
            type_ = _schema.get('type', 'object')

            # get value
            value, has_key = data.get_check(key)
            if has_key or '$ref' in _schema:
                result[key] = _normalize(_schema, value)
            elif 'default' in _schema:
                result[key] = _schema['default']
            elif key in schema.get('required', []):
                if type_ in required_defaults:
                    result[key] = required_defaults[type_]
                else:
                    errors.append(dict(name='property_missing',
                                       message='`%s` is required' % key))

        additional_properties_schema = schema.get('additionalProperties', False)
        if additional_properties_schema is not False:
            aproperties_set = set(data.keys()) - set(result.keys())
            for pro in aproperties_set:
                result[pro] = _normalize(additional_properties_schema, data.get(pro))

        return result

    def _normalize_list(schema, data):
        result = []
        if hasattr(data, '__iter__') and not isinstance(data, (dict, RefNode)):
            for item in data:
                result.append(_normalize(schema.get('items'), item))
        elif 'default' in schema:
            result = schema['default']
        return result

    def _normalize_default(schema, data):
        if data is None:
            return schema.get('default')
        else:
            return data

    def _normalize_ref(schema, data):
        if resolver == None:
            raise TypeError("resolver must be provided")
        ref = schema.get(u"$ref")
        scope, resolved = resolver.resolve(ref)
        if resolved.get('nullable', False) and not data:
            return {}
        return _normalize(resolved, data)

    def _normalize(schema, data):
        if schema is True or schema == {}:
            return data
        if not schema:
            return None
        funcs = {
            'object': _normalize_dict,
            'array': _normalize_list,
            'default': _normalize_default,
            'ref': _normalize_ref
        }
        type_ = schema.get('type', 'object')
        if type_ not in funcs:
            type_ = 'default'
        if schema.get(u'$ref', None):
            type_ = 'ref'

        return funcs[type_](schema, data)

    return _normalize(schema, data), errors
