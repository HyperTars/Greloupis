import unittest
from source.service.service_search import *
from source.settings import *

"""
def test_search_user(conf):
    print("\n===================== Test Search User =========================")
    print(service_search_user(conf, name="t", ignore_case=False, format="json"))
    print("\n===================== Test Search User (exact not found) =========================")
    print(service_search_user(conf, name="test", ignore_case=True, format="dict", exact=True))
    print("\n===================== Test Search User =========================")
    print(service_search_user(conf, name="test_user", ignore_case=True, format="dict", exact=True))


def test_search_video(conf):
    print("\n===================== Test Search Video: Title =========================")
    print(service_search_video(conf, title="Xi"))
    print("\n===================== Test Search Video: Title (case not found) =========================")
    print(service_search_video(conf, title="xi", ignore_case=False))
    print("\n===================== Test Search Video: Title, json =========================")
    print(service_search_video(conf, title="E", format="json"))
    print("\n===================== Test Search Video: Category =========================")
    print(service_search_video(conf, video_category="A"))
    print("\n===================== Test Search Video: Tag =========================")
    print(service_search_video(conf, video_tag="O"))
    print("\n===================== Test Search Video: Title slice =========================")
    print(service_search_video(conf, title="a h", slice=True))
    print("\n===================== Test Search Video: Title slice =========================")
    print(service_search_video(conf, title="i a", slice=True))
    print("\n===================== Test Search Video: Title slice =========================")
    print(service_search_video(conf, title="i%20a", slice=True))
"""

if __name__ == "__main__":
    unittest.main()
