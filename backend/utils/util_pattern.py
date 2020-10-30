import re
from models.model_errors import ErrorCode, UtilError


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
    if 'first_name' in kw and 'user_first_name' not in kw:
        kw['user_first_name'] = kw['first_name']
        kw.pop('first_name')
    if 'last_name' in kw and 'user_last_name' not in kw:
        kw['user_last_name'] = kw['last_name']
        kw.pop('last_name')
    if 'phone' in kw and 'user_phone' not in kw:
        kw['user_phone'] = kw['phone']
        kw.pop('phone')
    if 'street1' in kw and 'user_street1' not in kw:
        kw['user_street1'] = kw['street1']
        kw.pop('street1')
    if 'street2' in kw and 'user_street2' not in kw:
        kw['user_street2'] = kw['street2']
        kw.pop('street2')
    if 'city' in kw and 'user_city' not in kw:
        kw['user_city'] = kw['city']
        kw.pop('city')
    if 'state' in kw and 'user_state' not in kw:
        kw['user_state'] = kw['state']
        kw.pop('state')
    if 'country' in kw and 'user_country' not in kw:
        kw['user_country'] = kw['country']
        kw.pop('country')
    if 'zip' in kw and 'user_zip' not in kw:
        kw['user_zip'] = kw['zip']
        kw.pop('zip')
    if 'status' in kw and 'user_status' not in kw:
        kw['user_status'] = kw['status']
        kw.pop('status')
    if 'reg_date' in kw and 'user_reg_date' not in kw:
        kw['user_reg_date'] = kw['reg_date']
        kw.pop('reg_date')

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
        kw['video_title'] = '.*'.join(
            kw['video_title'].replace("%20", " ").split(" "))
    elif 'video_description' in kw:
        kw['video_description'] = '.*'.join(
            kw['video_description'].replace("%20", " ").split(" "))
    return kw


def util_pattern_build(**kw):
    # Construct pattern string
    # User
    if 'user_name' in kw:
        kw['user_name'] = util_pattern_compile(kw['user_name'], **kw)
    elif 'user_email' in kw:
        kw['user_email'] = util_pattern_compile(kw['user_email'], **kw)
    elif 'user_first_name' in kw:
        kw['user_first_name'] = util_pattern_compile(kw['user_first_name'],
                                                     **kw)
    elif 'user_last_name' in kw:
        kw['user_last_name'] = util_pattern_compile(kw['user_last_name'], **kw)
    elif 'user_phone' in kw:
        kw['user_phone'] = util_pattern_compile(kw['user_phone'], **kw)
    elif 'user_street1' in kw:
        kw['user_street1'] = util_pattern_compile(kw['user_street1'], **kw)
    elif 'user_street2' in kw:
        kw['user_street2'] = util_pattern_compile(kw['user_street2'], **kw)
    elif 'user_city' in kw:
        kw['user_city'] = util_pattern_compile(kw['user_city'], **kw)
    elif 'user_state' in kw:
        kw['user_state'] = util_pattern_compile(kw['user_state'], **kw)
    elif 'user_country' in kw:
        kw['user_country'] = util_pattern_compile(kw['user_country'], **kw)
    elif 'user_zip' in kw:
        kw['user_zip'] = util_pattern_compile(kw['user_zip'], **kw)
    elif 'user_status' in kw:
        kw['user_status'] = util_pattern_compile(kw['user_status'], **kw)
    elif 'user_reg_date' in kw:
        kw['user_reg_date'] = util_pattern_compile(kw['user_reg_date'], **kw)

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
        kw['video_description'] = util_pattern_compile(kw['video_description'],
                                                       **kw)

    # VideoOp
    elif 'video_op_comment' in kw:
        kw['video_op_comment'] = util_pattern_compile(kw['video_op_comment'],
                                                      **kw)
    # TODO: add more attr search support
    else:
        raise UtilError(ErrorCode.UTIL_INVALID_PATTERN_PARAM)

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
