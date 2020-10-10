from source.service.search import *
from source.config import TestConfig
from source.db.mongo import get_db

def test_search_user():
    print(search_user_by_keyword(name="te"))

if __name__ == "__main__":
    db = get_db(TestConfig)
    test_search_user()