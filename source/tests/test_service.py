from source.service.service_search import *
from source.config import TestConfig
from source.db.mongo import get_db

def test_search_user():
    print(search_user(name="t", ignore_case=False, type="json"))
    print("\n==============================================")
    print(search_user(name="test", ignore_case=True, type="dict", exact=True))
    print("\n==============================================")
    print(search_user(name="test4", ignore_case=True, type="dict", exact=True))

def test_search_video():
    print("\n==============================================")
    print(search_video(title="Xi"))


if __name__ == "__main__":
    db = get_db(TestConfig)
    # test_search_user()
    test_search_video()