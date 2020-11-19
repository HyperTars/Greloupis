import os
import sys
import json
import platform as pf
from db.mongo import get_db
from settings import config
from models.model_user import User
from models.model_video_op import VideoOp
from models.model_video import Video
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def util_tests_clean_database():
    get_db(config['test'])
    data = util_tests_load_data()

    for user in data['temp_user']:
        User.objects(user_name=user['user_name']).delete()

    for video in data['temp_video']:
        Video.objects(video_title=video['video_title']).delete()

    for video in data['const_video']:
        VideoOp.objects(video_id=video['_id']['$oid']).delete()


def util_tests_load_data():
    os_ver = pf.system()
    cwd = os.getcwd()

    if os_ver == 'Darwin' or os_ver == 'Linux':
        path = cwd + '/tests/test_data/'
    elif os_ver == 'Windows':
        path = cwd + '\\tests\\test_data\\'
    else:
        print("System not supported.")

    data = {}
    data['temp_user'] = util_tests_get_json(path + "temp_user.json")
    data['temp_video'] = util_tests_get_json(path + "temp_video.json")
    data['temp_video_op'] = util_tests_get_json(path + "temp_video_op.json")
    data['const_user'] = util_tests_get_json(path + "const_user.json")
    data['const_video'] = util_tests_get_json(path + "const_video.json")
    data['const_video_op'] = util_tests_get_json(path + "const_video_op.json")
    return data


def util_tests_get_json(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


def util_tests_python_version():
    if pf.python_version()[:3] != '3.7' and pf.python_version()[:3] != '3.8':
        print("Your python ver." + pf.python_version() + "is not supported.")
        print("Currently supported python version: 3.7 | 3.8")
        return False
    return True


if __name__ == '__main__':
    print(util_tests_load_data())
