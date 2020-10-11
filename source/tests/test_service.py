from source.service.service_search import *

def test_search_user():
    print(search_user(name="t", ignore_case=False, type="json"))
    print("\n==============================================")
    print(search_user(name="test", ignore_case=True, type="dict", exact=True))
    print("\n==============================================")
    print(search_user(name="test4", ignore_case=True, type="dict", exact=True))

def test_search_video():
    print("\n==============================================")
    print(search_video(title="Xi"))
    print("\n==============================================")
    print(search_video(title="test", type="json"))


if __name__ == "__main__":
    test_search_user()
    test_search_video()