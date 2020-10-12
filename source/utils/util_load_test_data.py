import os
import sys
import json
import platform as pf
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def util_load_test_data():    
    os_ver = pf.system()
    cwd = os.getcwd()

    if os_ver == 'Darwin' or os_ver == 'Linux':
        path = cwd + '/source/tests/test_data/'
    elif os_ver == 'Windows':
        path = cwd + '\\source\\tests\\test_data\\'
    else:
        print("System not supported.")

    data = {}
    data['user'] = get_json_data(path + "data_user.json")
    data['video'] = get_json_data(path + "data_video.json")
    data['video_op'] = get_json_data(path + "data_video_op.json")
    return data


def get_json_data(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


if __name__ == '__main__':    
    print(util_load_test_data())
