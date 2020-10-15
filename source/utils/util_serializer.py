from flask import Response
import json
import datetime


def util_serializer_mongo_results_to_array(results, format="dict"):
    res = []
    for r in results:
        if format == "json":
            res.append(util_serializer_dict_to_json(r.to_dict()))
        res.append(r.to_dict())
    return res


def util_serializer_dict_to_json(d):
    return json.dumps(d, cls=JSONDateEncoder)


def util_serializer_request(request, format="dict"):
    if format == "json":
        return util_serializer_dict_to_json(request.to_dict())
    else:
        return request.to_dict()


def util_serializer_api_response(body, code):
    response = {'body': body}
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
