import unittest
from looqbox.objects.looq_object import LooqObject
from looqbox.objects.visual.looq_avatar import ObjAvatar
from looqbox.integration.user import User


class TestAvatar(unittest.TestCase):
    """
    Test Avatar Component
    """

    def setUp(self):
        self.mocked_login: str = "johnDoe"
        self.mocked_id: int = 1
        self.mocked_user: User = User(login="johnDoe", id=1)
        self.mocked_avatar = ObjAvatar()

    def test_instance(self):
        self.assertIsInstance(self.mocked_avatar, LooqObject)

    def test_set_login(self):
        avatar = ObjAvatar()
        avatar.set_user_login(self.mocked_login)
        self.assertEqual(avatar.source, self.mocked_login)

    def test_set_id(self):
        avatar = ObjAvatar()
        avatar.set_user_id(self.mocked_id)
        self.assertEqual(avatar.source, self.mocked_id)

    def test_build_from_user(self):
        avatar = ObjAvatar()
        avatar.set_user_login(self.mocked_login)

        avatar_from_user = ObjAvatar()
        avatar_from_user.from_user(self.mocked_user)
        self.assertEqual(avatar.source, avatar_from_user.source)

    def test_set_user(self):
        avatar = ObjAvatar()
        avatar.set_user(login=self.mocked_login)
        self.assertEqual(avatar.source, self.mocked_login)

        avatar = ObjAvatar()
        avatar.set_user(id=self.mocked_id)
        self.assertEqual(avatar.source, self.mocked_id)

    def test_catch_missing_method(self):
        self.assertRaises(KeyError, ObjAvatar()._set_source_type, "NoMethod")

    def test_catch_missing_source(self):
        avatar = ObjAvatar(source_type="Login")
        self.assertRaises(Exception, avatar._set_image_source)

    def test_autoset_query_method(self):
        avatar = ObjAvatar()
        avatar.set_user_login(self.mocked_login)
        self.assertEqual(avatar.source_type.name.lower(), "login")


if __name__ == '__main__':
    unittest.main()
