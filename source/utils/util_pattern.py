import re
from source.models.model_errors import *


def util_pattern_compile(**kw):
    # Search by pattern (can ignore case)
    pattern_string = ""

    # Construct pattern string
    # Video
    if 'title' in kw:
        pattern_string = kw['title']
    elif 'video_title' in kw:
        pattern_string = kw['video_title']
    elif 'description' in kw:
        pattern_string = kw['description']
    elif 'video_description' in kw:
        pattern_string = kw['video_description']
    # User
    elif 'name' in kw:
        pattern_string = kw['name']
    elif 'user_name' in kw:
        pattern_string = kw['user_name']
    elif 'email' in kw:
        pattern_string = kw['email']
    elif 'user_email' in kw:
        pattern_string = kw['user_email']
    # VideoOp
    elif 'comment' in kw:
        pattern_string = kw['comment']
    elif 'video_op_comment' in kw:
        pattern_string = kw['video_op_comment']
    # TODO: add more attr search support
    else:
        return ErrorCode.MONGODB_INVALID_PATTERN_PARAM

    # Pattern flags
    if ('like' in kw and kw['like'] is False) or ('exact' in kw and kw['exact'] is True):
        pattern_string = '\\b' + pattern_string + '\\b'
    else:
        pattern_string = '.*' + pattern_string + '.*'
    # TODO: allow typo, allow slice

    # Compile pattern string
    pattern = re.compile(pattern_string)
    if 'ignore_case' in kw and kw['ignore_case'] is True:
        pattern = re.compile(pattern_string, re.IGNORECASE)

    return pattern
