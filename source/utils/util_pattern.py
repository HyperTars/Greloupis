import re
from source.models.model_errors import *


def util_pattern_compile(**kw):
    # Search by pattern (can ignore case)
    pattern_string = ""

    # Construct pattern string
    if 'title' in kw:
        pattern_string = kw['title']
    elif 'name' in kw:
        pattern_string = kw['name']
    elif 'email' in kw:
        pattern_string = kw['email']
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
