from source.service.service_search import *
from source.config import TestConfig


def test_search_user():
    print(service_search_user(TestConfig, name="t", ignore_case=False, type="json"))
    print("\n==============================================")
    print(service_search_user(TestConfig, name="test", ignore_case=True, type="dict", exact=True))
    print("\n==============================================")
    print(service_search_user(TestConfig, name="test_user", ignore_case=True, type="dict", exact=True))


def test_search_video():
    print("\n==============================================")
    print(service_search_video(TestConfig, title="Xi"))
    print("\n==============================================")
    print(service_search_video(TestConfig, title="test", type="json"))


if __name__ == "__main__":
    test_search_user()
    test_search_video()
