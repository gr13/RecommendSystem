"""
BaseTest

This class should be parent to each test.
It allows for instantiation of the database dynamically,
and make sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from app.db import db


class BaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///data_test.db"

    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = BaseTest.SQLALCHEMY_DATABASE_URI
        app.config['DEBUG'] = False
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        with app.app_context():
            db.create_all()
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
