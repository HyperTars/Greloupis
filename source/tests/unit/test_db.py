import unittest
from source.settings import *
from source.db.mongo import get_db
from source.tests.unit.test_load_data import *
from source.db.query_user import *
from source.models.model_errors import MongoError


class TestQueryUser(unittest.TestCase):
    # temp name
    temp_name = "temp_name"
    temp_email = "temp@gmail.com"
    temp_password = "temp"
    permanent_name = "hypertars"
    permanent_email = "hypertars@gmail.com"
    permanent_password = "hypertars_pass"

    def setUp(self):
        self.data = util_load_test_data()

    def test_user_create(self):
        # Create successfully
        self.assertEqual(query_user_create(user_name=self.temp_name, user_email=self.temp_email,
                                           user_password=self.temp_password).user_name, self.temp_name)

        # Raise Error: ErrorCode.MONGODB_USER_NAME_TAKEN
        with self.assertRaises(MongoError) as e1:
            query_user_create(user_name=self.temp_name, user_email=self.temp_email,
                              user_password=self.temp_password)
        self.assertEqual(e1.exception.error_code, ErrorCode.MONGODB_USER_NAME_TAKEN)

        # Raise Error: ErrorCode.MONGODB_USER_EMAIL_TAKEN
        with self.assertRaises(MongoError) as e2:
            query_user_create(user_name="NotImportantName", user_email=self.temp_email,
                              user_password=self.temp_password)
        self.assertEqual(e2.exception.error_code, ErrorCode.MONGODB_USER_EMAIL_TAKEN)

    def test_user_get_by_name(self):
        # Get successfully
        temp_model = query_user_get_by_name(self.permanent_name)[0]
        self.assertEqual(temp_model.user_email, self.permanent_email)

    def test_user_get_by_email(self):
        pass

    def test_user_get_by_id(self):
        pass

    def test_user_update_status(self):
        pass

    def test_user_add_follow(self):
        pass

    def test_user_delete_follow(self):
        pass

    def test_user_update_name(self):
        pass

    def test_user_update_password(self):
        pass

    def test_user_update_thumbnail(self):
        pass

    def test_user_update_details(self):
        pass

    def test_user_add_login(self):
        pass

    def test_user_delete_by_id(self):
        temp_model = query_user_get_by_name(self.temp_name)[0]
        self.assertEqual(query_user_delete_by_id(temp_model._id), 1)

    def test_user_delete_by_name(self):
        pass

    def test_user_search_by_contains(self):
        pass

    def test_user_search_by_pattern(self):
        pass

    def test_user_search_by_aggregate(self):
        pass


class TestQueryVideo(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()


class TestQueryVideoOp(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()


class TestQuerySearch(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()


if __name__ == "__main__":
    db = get_db(TestConfig)
    unittest.main()
