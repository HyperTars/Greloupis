from flask import Response
import json
import datetime


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


def util_serializer_request(request, format="dict"):
    if format == "json":
        return util_serializer_dict_to_json(request.to_dict())
    else:
        return request.to_dict()


def util_serializer_api_response(code, body=[{}], msg=""):
    if code == 200:
        response = {"code": code, "body": body, "detailed_msg": msg}

    else:
        code = str(code)
        general_message = {
            "400": "Bad Request",
            "404": "Resource Not Found",
            "405": "Method Not Allowed",
            "500": "Internal Server Error"
        }
        response = {"code": code, "general_msg": general_message[code], "detailed_msg": msg}

    result = json.dumps(response, indent=4, sort_keys=True, separators=(',', ': ')) \
        .replace('\\"', "'").replace('"{', '{').replace('}"', '}').replace("'", '"')
    return Response(result, status=code, mimetype='application/json')


class JSONDateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
