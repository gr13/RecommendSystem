from app.models.user import UserModel
from app.tests.base_test import BaseTest
from app.models.user_right import UserRightModel
import json


class UserTest(BaseTest):
    def setUp(self):
        super(UserTest, self).setUp()
        with self.app() as c:
            with self.app_context():
                right = UserRightModel('blocked')
                right.save_to_db()

                right = UserRightModel('user test')
                right.save_to_db()

    def test_register_user(self):
        with self.app() as c:
            with self.app_context():
                r = c.post(
                    '/register', data={
                    "email": "test@user.com",
                    "password": "password"
                    }
                )

                self.assertEqual(
                    r.status_code,
                    201,
                    f"Error in request, expected response 201, obtained {r.status_code}."
                )

                self.assertIsNotNone(UserModel.find_by_email("test@user.com"))
                self.assertDictEqual(
                    d1={"message": "User created successfully."},
                    d2=json.loads(r.data)
                )

    def test_register_and_login(self):
        with self.app() as c:
            with self.app_context():
                r = c.post(
                    '/register', data={
                        "email": "test@user.com",
                        "password": "password"
                    }
                )

                user = UserModel.find_by_email("test@user.com")
                user.right_id = 2
                user.save_to_db()

                login = c.post(
                    '/login',
                    data=json.dumps({
                        "email": "test@user.com",
                        "password": "password"
                    }),
                    headers={'Content-Type': 'application/json'}
                )

                self.assertIn(
                    'access_token',
                    json.loads(login.data).keys(),
                    "Access token is not found after user login"
                )

    def test_blocked_user_login(self):
        with self.app() as c:
            with self.app_context():
                r = c.post(
                    '/register',
                    data={
                        "email": "test@user.com",
                        "password": "password"
                    }
                )

                user = UserModel.find_by_email("test@user.com")
                self.assertEqual(user.right_id, 1)

                login = c.post(
                    '/login',
                    data=json.dumps({
                        "email": "test@user.com",
                        "password": "password"
                    }),
                    headers={'Content-Type': 'application/json'}
                )

                self.assertNotIn(
                    'access_token',
                    json.loads(login.data).keys(),
                    "A blocked User logged in successfully."
                )
                self.assertDictEqual(
                    {"message": "Invalid credentials"},
                    json.loads(login.data)
                )

    def test_register_dublicate_user(self):
        with self.app() as c:
            with self.app_context():
                c.post(
                    '/register',
                    data={
                        "email": "test@user.com",
                        "password": "password"
                    }
                )
                r = c.post(
                    '/register',
                    data={
                        "email": "test@user.com",
                        "password": "password"
                    }
                )

                self.assertEqual(r.status_code, 400)
                self.assertDictEqual(d1={'message': 'A user with that username already exists.'},
                                     d2=json.loads(r.data))

    def test_user_list(self):
        with self.app() as c:
            with self.app_context():
                user = UserModel("test@user.com", "password")
                user.save_to_db()

                r = c.get('users')

                expected = {
                    "users": [
                        {"id": 1, "email": "test@user.com", "right_id": 1, "right": {"id": 1, "right": "blocked"}, "username": "", "position": "", "hide": False}
                    ]
                }

                self.assertEqual(r.status_code, 200)
                self.assertDictEqual(d1=expected,
                                     d2=json.loads(r.data))
