from models import User, LoginDetail, UserDetail, Thumbnail
import bson
import datetime

# User CRUD
def user_get_by_name(user_name: str):
    """
    :return: an array of such User, len == 0 if no such user_name, len == 1 if found
    """
    return User.objects(user_name=user_name)


def user_get_by_email(user_email: str):
    """
    :return: an array of such User (len == 0 or 1), len == 0 if no such user_email, len == 1 if found
    """
    return User.objects(user_email=user_email)


def user_get_by_id(user_id: str):
    """
    :return: an array of such User (len == 0 or 1), len == 0 if no such user_id, len == 1 if found
    """
    return User.objects(_id = bson.ObjectId(user_id))


def user_create(user_name: str, user_email: str, user_password: str, user_ip="0.0.0.0"):
    """
    :param user_name: user's unique nickname
    :param user_email: user's unique email
    :param user_password: user's password
    :param user_ip: user's ip address (defaut 0.0.0.0)
    :return: 1 if succeeded, -1 if name already taken, -2 if email already taken
    """
    if len(user_get_by_name(user_name)) > 0:
        # print("user name is taken")
        return -1 # TODO: error_code
    elif len(user_get_by_email(user_email)) > 0:
        # print("user email is taken")
        return -2 # TODO: error_code
    login = []
    login.append(LoginDetail(login_ip=user_ip, login_time=datetime.datetime.utcnow()))
    user = User(user_name=user_name, user_email=user_email, user_password=user_password, user_status="private", user_detail = UserDetail(), user_thumbnail=Thumbnail(), user_recent_login=login, user_reg_date=datetime.datetime.utcnow())
    user.save()
    return 1


def user_update_status(user_id: str, user_status: str):
    """
    :param user_id: user's unique id
    :return: 1 if succeeded, -1 if no such user
    """
    if len(user_get_by_id(user_id)) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    valid_status = ["public", "private", "closed"]
    if user_status not in valid_status:
        # print("Not valid status")
        return -2 # TODO: error_code
    return User.objects(_id = bson.ObjectId(user_id)).update(user_status=user_status)


def user_add_follow(follower_id: str, following_id: str):
    """
    :param follower_id: follower's user id
    :param following_id: uploader's user_id
    :return: 1 if succeeded, -1 if no such follower, -2 if no such uploader, -3 already followed
    """
    follower = user_get_by_id(follower_id)
    following = user_get_by_id(following_id)
    if len(follower) == 0:
        return -1
    if len(following) == 0:
        return -2
    if following_id in follower[0].user_following and follower_id in following[0].user_follower:
        # print("already followed")
        return -3
    if following_id in follower[0].user_following or follower_id in following[0].user_follower:
        # print("following relationship broken, try to remove")
        user_delete_follow(follower_id, following_id)
    r1 = User.objects(_id = bson.ObjectId(follower_id)).update(add_to_set__user_following=following_id)
    r2 = User.objects(_id = bson.ObjectId(following_id)).update(add_to_set__user_follower=follower_id)
    if r1 != 1:
        return r1
    elif r2 != 1:
        return r2
    return 1


def user_delete_follow(follower_id: str, following_id: str):
    """
    :param follower_id: follower's user id
    :param following_id: uploader's user_id
    :return: 1 if succeeded, -1 if no such follower, -2 if no such uploader
    """
    follower = user_get_by_id(follower_id)
    following = user_get_by_id(following_id)
    if len(follower) == 0:
        return -1
    if len(following) == 0:
        return -2
    r1 = User.objects(_id = bson.ObjectId(follower_id)).update(pull__user_following=following_id)
    r2 = User.objects(_id = bson.ObjectId(following_id)).update(pull__user_follower=follower_id)
    if r1 != 1:
        return r1
    elif r2 != 1:
        return r2
    return 1


def user_update_name(user_id: str, user_name: str):
    """
    :param user_id: user's id
    :param user_name: user's name
    :return: 1 if succeeded, -1 if no such user, -2 if same name as current, -3 if name already taken
    """
    users = user_get_by_id(user_id)
    if len(users) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    old_name = users[0].user_name
    if user_name == old_name:
        # print("Same name as the current")
        return -2 # TODO: error_code
    if len(user_get_by_name(user_name)) > 0:
        # print("Name already taken")
        return -3 # TODO: error_code
    return User.objects(_id = bson.ObjectId(user_id)).update(user_name=user_name)


def user_update_password(user_id: str, user_password: str):
    """
    :param user_id: user's id
    :param user_password: user's password
    :return: 1 if succeeded, -1 if no such user, -2 if same password as current
    """
    users = user_get_by_id(user_id)
    if len(users) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    old_password = users[0].user_password
    if user_password == old_password:
        # print("Same password as the current")
        return -2 # TODO: error_code
    return User.objects(_id = bson.ObjectId(user_id)).update(user_password=user_password)


def user_update_details(user_id: str, **kw):
    """
    :param user_first_name (optional): new user's first name
    :param user_last_name (optional): new user's last_name
    :param user_phone (optional): new user's phone
    :param user_street1 (optional): new user's street1
    :param user_street2 (optional): new user's street2
    :param user_city (optional): new user's city
    :param user_state (optional): new user's state
    :param user_country (optional): new user's country
    :param user_zip (optional): new user's zip
    :return 1 if succeeded, -1 if no such user
    """
    users = user_get_by_id(user_id)
    id = bson.ObjectId(user_id)
    if len(users) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    if 'user_first_name' in kw:
        User.objects(_id=id).update(set__user_detail__first_name=kw['user_first_name'])
    if 'user_last_name' in kw:
        User.objects(_id=id).update(set__user_detail__last_name=kw['user_last_name'])
    if 'user_phone' in kw:
        User.objects(_id=id).update(set__user_detail__phone=kw['user_phone'])
    if 'user_street1' in kw:
        User.objects(_id=id).update(set__user_detail__street1=kw['user_street1'])
    if 'user_street2' in kw:
        User.objects(_id=id).update(set__user_detail__street2=kw['user_street2'])
    if 'user_city' in kw:
        User.objects(_id=id).update(set__user_detail__city=kw['user_city'])
    if 'user_state' in kw:
        User.objects(_id=id).update(set__user_detail__state=kw['user_state'])
    if 'user_country' in kw:
        User.objects(_id=id).update(set__user_detail__country=kw['user_country'])
    if 'user_zip' in kw:
        User.objects(_id=id).update(set__user_detail__zip=kw['user_zip'])
    return 1


def user_update_thumbnail(user_id: str, **kw):
    """
    :param user_id: user's unique id
    :param user_thumbnail_uri: thumbnail uri
    :param user_thumbnail_type: must be in ['default', 'user', 'system']
    :return 1 if succeeded, -1 if no such user, -2 if invalid thumbnail type
    """
    users = user_get_by_id(user_id)
    id = bson.ObjectId(user_id)
    if len(users) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    valid_type=['default', 'user', 'system']
    if 'user_thumbnail_uri' in kw:
        User.objects(_id=id).update(set__user_thumbnail__thumbnail_uri=kw['user_thumbnail_uri'])
    if 'user_thumbnail_type' in kw:
        if kw['user_thumbnail_type'] not in valid_type:
            # print("Invalid thumbnail type")
            return -2 # TODO: error_code
        User.objects(_id=id).update(set__user_thumbnail__thumbnail_type=kw['user_thumbnail_type'])
    return 1


def user_add_login(user_id: str, ip="0.0.0.0", time=datetime.datetime.utcnow()):
    """
    :param user_id: user's unique id
    :param ip: user's login ip address
    :param time: user's login time (utc, optional), default: current system time (utc)
    :return: 0 if succeeded, -1 if no such user, -2 if time already exist
    """
    users = user_get_by_id(user_id)
    if len(users) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    # only keep 10 login info
    login_history = users[0].user_recent_login
    oldest_login_time = login_history[0].login_time
    latest_login_time = login_history[-1].login_time
    if len(login_history) >= 10:
        # print("Delete oldest history")
        User.objects(_id = bson.ObjectId(user_id)).update(pull__user_recent_login__login_time=oldest_login_time)
    # add new login info
    # print(time)
    # print(latest_login_time)
    if time == latest_login_time:
        # print("Login info already added")
        return -2
    new_login = {'login_ip': ip, 'login_time': time}
    User.objects(_id = bson.ObjectId(user_id)).update(add_to_set__user_recent_login=[new_login])
    return 0


def user_delete(user_id: str):
    """
    :param user_id: user's unique id
    :return: 1 if succeeded, -1 if no such user
    """
    users = user_get_by_id(user_id)
    if len(users) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    return User.objects(_id = bson.ObjectId(user_id)).delete()