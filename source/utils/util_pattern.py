import re
from source.models.model_errors import *


def util_pattern_format_search_param(**kw):
    # ID
    if kw['search'] == 'user':
        if '_id' in kw:
            kw['user_id'] = kw['_id']
            kw.pop('_id')
        if 'id' in kw:
            kw['user_id'] = kw['id']
            kw.pop('id')
    if kw['search'] == 'video':
        if '_id' in kw:
            kw['video_id'] = kw['_id']
            kw.pop('_id')
        if 'id' in kw:
            kw['video_id'] = kw['id']
            kw.pop('id')
    if kw['search'] == 'video_op':
        if '_id' in kw:
            kw['video_op_id'] = kw['_id']
            kw.pop('_id')
        if 'id' in kw:
            kw['video_op_id'] = kw['id']
            kw.pop('id')

    # User
    if 'name' in kw and 'user_name' not in kw:
        kw['user_name'] = kw['name']
        kw.pop('name')
    if 'email' in kw and 'user_email' not in kw:
        kw['user_email'] = kw['email']
        kw.pop('email')

    # Video
    if 'title' in kw and 'video_title' not in kw:
        kw['video_title'] = kw['title']
        kw.pop('title')
    if 'channel' in kw and 'video_channel' not in kw:
        kw['video_channel'] = kw['channel']
        kw.pop('channel')
    if 'tag' in kw and 'video_tag' not in kw:
        kw['video_tag'] = kw['tag']
        kw.pop('tag')
    if 'category' in kw and 'video_category' not in kw:
        kw['video_category'] = kw['category']
        kw.pop('category')
    if 'description' in kw and 'video_description' not in kw:
        kw['video_description'] = kw['description']
        kw.pop('description')

    # VideoOp
    if 'comment' in kw and 'video_op_comment' not in kw:
        kw['video_op_comment'] = kw['comment']
        kw.pop('comment')

    return kw


def util_pattern_slice(**kw):
    if 'video_title' in kw:
        kw['video_title'] = '.*'.join(kw['video_title'].replace("%20", " ").split(" "))
    elif 'video_description' in kw:
        kw['video_description'] = '.*'.join(kw['video_description'].replace("%20", " ").split(" "))
    return kw


def util_pattern_build(**kw):
    # Construct pattern string
    # User
    if 'user_name' in kw:
        kw['user_name'] = util_pattern_compile(kw['user_name'], kw['exact'], kw['ignore_case'])
    elif 'user_email' in kw:
        kw['user_email'] = util_pattern_compile(kw['user_email'], kw['exact'], kw['ignore_case'])

    # Video
    elif 'video_title' in kw:
        kw['video_title'] = util_pattern_compile(kw['video_title'], kw['exact'], kw['ignore_case'])
    elif 'video_channel' in kw:
        kw['video_channel'] = util_pattern_compile(kw['video_channel'], kw['exact'], kw['ignore_case'])
    elif 'video_tag' in kw:
        kw['video_tag'] = util_pattern_compile(kw['video_tag'], kw['exact'], kw['ignore_case'])
    elif 'video_category' in kw:
        kw['video_category'] = util_pattern_compile(kw['video_category'], kw['exact'], kw['ignore_case'])
    elif 'video_description' in kw:
        kw['video_description'] = util_pattern_compile(kw['video_description'], kw['exact'], kw['ignore_case'])

    # VideoOp
    elif 'video_op_comment' in kw:
        kw['video_op_comment'] = util_pattern_compile(kw['video_op_comment'], kw['exact'], kw['ignore_case'])
    # TODO: add more attr search support
    else:
        return ErrorCode.UTIL_INVALID_PATTERN_PARAM

    return kw


def util_pattern_compile(pattern_string, exact, ignore_case):
    # Pattern flags
    if exact is True:
        pattern_string = '\\b' + pattern_string + '\\b'
    else:
        pattern_string = '.*' + pattern_string + '.*'

    # TODO: allow typo, allow slice

    # Compile pattern string
    pattern = re.compile(pattern_string)
    if ignore_case is True:
        pattern = re.compile(pattern_string, re.IGNORECASE)

    return pattern
