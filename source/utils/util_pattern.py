import re
from source.models.model_errors import *


def util_pattern_format_param(**kw):
    # ID
    if kw['service'] == 'user':
        if '_id' in kw:
            kw['user_id'] = kw['_id']
            kw.pop('_id')
        if 'id' in kw:
            kw['user_id'] = kw['id']
            kw.pop('id')
    if kw['service'] == 'video':
        if '_id' in kw:
            kw['video_id'] = kw['_id']
            kw.pop('_id')
        if 'id' in kw:
            kw['video_id'] = kw['id']
            kw.pop('id')
    if kw['service'] == 'video_op':
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
    if 'password' in kw and 'user_password' not in kw:
        kw['user_password'] = kw['password']
        kw.pop('password')

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
    if 'raw_content' in kw and 'video_raw_content' not in kw:
        kw['video_raw_content'] = kw['raw_content']
        kw.pop('raw_content')
    if 'content' in kw and 'video_raw_content' not in kw:
        kw['video_raw_content'] = kw['content']
        kw.pop('content')

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
        kw['user_name'] = util_pattern_compile(kw['user_name'], **kw)
    elif 'user_email' in kw:
        kw['user_email'] = util_pattern_compile(kw['user_email'], **kw)

    # Video
    elif 'video_title' in kw:
        kw['video_title'] = util_pattern_compile(kw['video_title'], **kw)
    elif 'video_channel' in kw:
        kw['video_channel'] = util_pattern_compile(kw['video_channel'], **kw)
    elif 'video_tag' in kw:
        kw['video_tag'] = util_pattern_compile(kw['video_tag'], **kw)
    elif 'video_category' in kw:
        kw['video_category'] = util_pattern_compile(kw['video_category'], **kw)
    elif 'video_description' in kw:
        kw['video_description'] = util_pattern_compile(kw['video_description'], **kw)

    # VideoOp
    elif 'video_op_comment' in kw:
        kw['video_op_comment'] = util_pattern_compile(kw['video_op_comment'], **kw)
    # TODO: add more attr search support
    else:
        return ErrorCode.UTIL_INVALID_PATTERN_PARAM

    return kw


def util_pattern_compile(pattern_string, **kw):
    # Remove '+' in the beginning of phone number
    if '+' in pattern_string:
        pattern_string = pattern_string.replace('+', '')

    # Pattern flags
    if 'exact' in kw and kw['exact'] is True:
        pattern_string = '\\b' + pattern_string + '\\b'
    elif 'exact' in kw and kw['exact'] is False:
        pattern_string = '.*' + pattern_string + '.*'

    # TODO: allow typo, allow slice

    # Compile pattern string
    pattern = re.compile(pattern_string)
    if 'ignore_case' in kw and kw['ignore_case'] is True:
        pattern = re.compile(pattern_string, re.IGNORECASE)

    return pattern
