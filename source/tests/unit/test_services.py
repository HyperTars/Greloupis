import unittest
from source.service.service_search import *
from source.settings import *
from source.tests.unit.test_load_data import util_load_test_data


class TestServiceSearchUser(unittest.TestCase):
    data = util_load_test_data()
    const_user_0 = data['const_user'][0]

    @classmethod
    def setUpClass(cls) -> None:
        cls.conf = config['test']

    def test_search_user(self):
        self.assertEqual(service_search_user(self.conf, name="t", ignore_case=False)[0]['user_name'],
                         self.const_user_0['user_name'])
        self.assertEqual(len(service_search_user(self.conf, name="test", ignore_case=True, exact=True)),
                         0)
        self.assertEqual(len(service_search_user(self.conf, name="test_user", ignore_case=True,
                                                 format="dict", exact=True)),
                         0)


class TestServiceSearchVideo(unittest.TestCase):
    data = util_load_test_data()
    const_video_0 = data['const_video'][0]

    @classmethod
    def setUpClass(cls) -> None:
        cls.conf = config['test']

    def test_search_video(self):
        self.assertEqual(service_search_video(self.conf, title="Xi")[0]['video_title'],
                         self.const_video_0['video_title'], msg="Test Search Video: Title")

        self.assertEqual(len(service_search_video(self.conf, title="xi", ignore_case=False)), 0,
                         msg="Test Search Video: Title (not found)")

        self.assertEqual(len(service_search_video(self.conf, title="E", format="json")), 0,
                         msg="Test Search Video: Title, json")

        self.assertEqual(service_search_video(self.conf, video_category="A")[0]['video_title'],
                         self.const_video_0['video_title'], msg="Test Search Video: Category")

        self.assertEqual(service_search_video(self.conf, video_tag="O")[0]['video_title'],
                         self.const_video_0['video_title'], msg="Test Search Video: Tag")

        self.assertEqual(service_search_video(self.conf, title="a h", slice=True)[0]['video_title'],
                         self.const_video_0['video_title'], msg="Test Search Video: Tag")

        self.assertEqual(service_search_video(self.conf, title="i a", slice=True)[0]['video_title'],
                         self.const_video_0['video_title'], msg="Test Search Video: Tag")

        self.assertEqual(service_search_video(self.conf, title="i%20a", slice=True)[0]['video_title'],
                         self.const_video_0['video_title'], msg="Test Search Video: Tag")


if __name__ == "__main__":
    unittest.main()
