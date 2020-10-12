from source.service.service_search import *
from source.config import TestConfig


def test_search_user():
    print("\n===================== Test Search User =========================")
    print(service_search_user(TestConfig, name="t", ignore_case=False, format="json"))
    print("\n===================== Test Search User (exact not found) =========================")
    print(service_search_user(TestConfig, name="test", ignore_case=True, format="dict", exact=True))
    print("\n===================== Test Search User =========================")
    print(service_search_user(TestConfig, name="test_user", ignore_case=True, format="dict", exact=True))


def test_search_video():
    print("\n===================== Test Search Video: Title =========================")
    print(service_search_video(TestConfig, title="Xi"))
    print("\n===================== Test Search Video: Title (case not found) =========================")
    print(service_search_video(TestConfig, title="xi", ignore_case=False))
    print("\n===================== Test Search Video: Title, json =========================")
    print(service_search_video(TestConfig, title="E", format="json"))
    print("\n===================== Test Search Video: Category =========================")
    print(service_search_video(TestConfig, video_category="A"))
    print("\n===================== Test Search Video: Tag =========================")
    print(service_search_video(TestConfig, video_tag="O"))
    print("\n===================== Test Search Video: Title slice =========================")
    print(service_search_video(TestConfig, title="a h", slice=True))
    print("\n===================== Test Search Video: Title slice =========================")
    print(service_search_video(TestConfig, title="i a", slice=True))


if __name__ == "__main__":
    test_search_user()
    test_search_video()
