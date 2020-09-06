from app import app
# from app.db import db
# remove as soon as SQL is ready
from app.models.user_right import UserRightModel
from app.models.country import CountryModel
from app.models.user import UserModel
import sys
from app.db import db


# flask logger
sys.stdout = sys.stderr = open('log/flasklog.txt', 'w+')

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()

    if len([item for item in UserRightModel.find_all()]) == 0:
        # we need to create Rights only once!
        right = UserRightModel('blocked')
        right.save_to_db()
        right = UserRightModel('customer')
        right.save_to_db()
        right = UserRightModel('operator')
        right.save_to_db()
        right = UserRightModel('chief operator')
        right.save_to_db()
        right = UserRightModel('manager')
        right.save_to_db()
        right = UserRightModel('regional manager')
        right.save_to_db()
        right = UserRightModel('admin')
        right.save_to_db()

    if len([item for item in CountryModel.find_all()]) == 0:
        country = CountryModel("USA")
        country.save_to_db()
        country = CountryModel("Germany")
        country.save_to_db()
        country = CountryModel("Finland")
        country.save_to_db()
        country = CountryModel("UK")
        country.save_to_db()
    if len([item for item in UserModel.find_all()]) == 0:
        user = UserModel("admin@admin.com", "test")
        user.right_id = 7
        user.save_to_db()
        user = UserModel("oper@oper.com", "test")
        user.right_id = 3
        user.save_to_db()
        user = UserModel("customer@customer.com", "test")
        user.right_id = 2
        user.save_to_db()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
