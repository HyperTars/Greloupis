def util_serializer_mongo_results_to_array(results, format="dict"):
    res = []

    for r in results:
        if format == "json":
            res.append(r.to_json())
        else:
            res.append(r.to_dict())

    return res


def util_serializer_request(request, format="dict"):
    return request.to_dict()
