from source.service.service_search import *
from source.config import TestConfig


def test_search_user():
    print("\n=====================Test Search User=========================")
    print(service_search_user(TestConfig, name="t", ignore_case=False, type="json"))
    print("\n=====================Test Search User (exact not found)=========================")
    print(service_search_user(TestConfig, name="test", ignore_case=True, type="dict", exact=True))
    print("\n=====================Test Search User=========================")
    print(service_search_user(TestConfig, name="test_user", ignore_case=True, type="dict", exact=True))


def test_search_video():
    print("\n=====================Test Search Video=========================")
    print(service_search_video(TestConfig, title="xi"))
    print("\n=====================Test Search Video=========================")
    print(service_search_video(TestConfig, title="E", type="json"))


if __name__ == "__main__":
    test_search_user()
    test_search_video()
