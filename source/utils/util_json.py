from flask import Response
import json

def api_response(body, code):
    response = {}
    response['body'] = body
    result = json.dumps(response, indent=4, sort_keys=True).replace('\\"', "'")
    return Response(result, status=code, mimetype='application/json')