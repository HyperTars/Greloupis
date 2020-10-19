import bson


def is_valid_id(id_str):
    return bson.objectid.ObjectId.is_valid(id_str)