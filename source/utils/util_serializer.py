from flask import Response
import json
import datetime


def util_serializer_mongo_results_to_array(results):
    res = []
    for r in results:
        res.append(r.to_dict())
    return res


def util_serializer_array_dict_to_json(array_dict):
    res = []
    for d in array_dict:
        res.append(json.dumps(d, cls=JSONDateEncoder))
    return res


def util_serializer_request(request, format="dict"):
    return request.to_dict()


def util_serializer_api_response(body, code):
    response = {'body': body}
    result = json.dumps(response, indent=4, sort_keys=True, separators=(',', ': ')) \
        .replace('\\"', "'").replace('"{', '{').replace('}"', '}').replace("'", '"')
    return Response(result, status=code, mimetype='application/json')


class JSONDateEncoder(json.JSONEncoder):
    def default(self, obj, date):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
