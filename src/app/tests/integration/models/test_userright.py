from app.models.user_right import UserRightModel
from app.tests.base_test import BaseTest

class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            userright = UserRightModel('test user right')
            self.assertIsNone(
                UserRightModel.find_by_right('test user right'),
                "Found UserRight with title 'test user right' before save_to_db"
            )
            self.assertIsNone(
                UserRightModel.find_by_id(1),
                "Found UserRight with id '1' before save_to_db"
            )

            userright.save_to_db()

            self.assertIsNotNone(
                UserRightModel.find_by_right('test user right'),
                "Did not find an UserRight with title 'test user right' after save_to_db"
            )

            self.assertIsNotNone(
                UserRightModel.find_by_id(1),
                "Did not find an UserRight with id 1 after save to db"
            )
