from app.models.user import UserModel
from app.models.user_right import UserRightModel

from app.tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            # to test user we need to create user right
            right = UserRightModel('test right')
            right.save_to_db()

            user = UserModel('test@test.com', 'abcd')

            self.assertIsNone(
                UserModel.find_by_email('test@test.com'),
                "Found a user with e-mail 'test@test.com' before save_to_db."
            )

            self.assertIsNone(
                UserModel.find_by_id(1),
                "Found a user with id '1' before save_to_db."
            )

            user.save_to_db()

            self.assertIsNotNone(
                UserModel.find_by_email('test@test.com'),
                "Did not find a user with e-mail 'test@test.com' after save_to_db"
            )
            self.assertIsNot(
                UserModel.find_by_id(1),
                "Did not find a user with id '1' after save_to_db"
            )

    def test_user_json(self):
        with self.app_context():
            # to test user we need to create user right
            userright = UserRightModel('test right')
            userright.save_to_db()

            user = UserModel('test@test.com', 'abcd')
            user.save_to_db()

            expected = {
                'id': 1,
                'email': 'test@test.com',
                'right_id': 1,
                'right': {'id': 1, 'right': 'test right'},
                'username': '',
                'position': '',
                'hide': False
            }

            self.assertEqual(
                user.json(),
                expected,
                f"The JSON export of the user is incorrect. Received {user.json()}, expected {expected}"
            )
