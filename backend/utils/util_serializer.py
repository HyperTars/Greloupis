from flask import Response
import json
import datetime
import ast


def util_serializer_mongo_results_to_array(results, format="dict"):
    res = []
    for r in results:
        if format == "json":
            res.append(util_serializer_dict_to_json(r.to_dict()))
        else:
            res.append(r.to_dict())
    return res


def util_serializer_dict_to_json(d):
    return json.dumps(d, cls=JSONDateEncoder)
    # return json.dumps(d)


def util_serializer_request(request):
    kw = {}
    if request.form != {}:
        kw = dict(request.form)
    else:
        kw = ast.literal_eval(request.data.decode("utf-8"))
    return kw


def extract_error_msg(message):
    return message.replace("'", "").replace('"', "")


def util_serializer_api_response(code, body=[{}], error_code=None, msg=""):
    if code == 200:
        response = {"code": code, "body": body, "message": str(msg)}
    else:
        if error_code is None:
            response = {"code": code, "message": str(msg)}
        else:
            error_code = str(error_code)
            response = {"code": code, "error_code": error_code,
                        "message": str(msg)}

    result = json.dumps(response, cls=JSONDateEncoder, indent=4,
                        sort_keys=True, separators=(',', ': ')) \
        .replace("'", "/^").replace('\\"', "'").replace('"{', '{') \
        .replace('}"', '}').replace("'", '"').replace("'", '"').replace("/^",
                                                                        "'")

    return Response(result, status=code, mimetype='application/json')


class JSONDateEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.strftime('%Y-%m-%d %H:%M:%S') \
            if isinstance(obj, datetime.datetime) \
            else json.JSONEncoder.default(self, obj)
