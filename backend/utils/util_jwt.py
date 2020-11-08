from flask import jsonify

blacklist = set()


def util_get_formated_response(code=200, data={}, msg=""):
    return jsonify({
        "code": code,
        "data": data,
        "message": msg
    })
