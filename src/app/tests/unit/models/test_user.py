from app.models.user import UserModel
from app.tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_create_user(self):
        user = UserModel('test@test.com', 'abcd')

        self.assertEqual(user.email, 'test@test.com',
                         "The name of the user after creation does not equal the constructor argument")

        self.assertEqual(user.password, 'abcd',
                         "The password of the user after creation does not equal the constructor argument")

    def test_error_email_user(self):
        # test if user e-mail after creation has '@' symbol
        with self.assertRaises(AssertionError) as cm:
            user = UserModel('test', 'abcd')
