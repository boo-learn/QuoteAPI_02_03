from api import Resource, reqparse, db
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


# /users GET
# /users/<id> GET
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = UserModel.query.get(user_id)
            return user_schema.dump(user)

        users = UserModel.query.all()
        return users_schema.dump(users)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        user_data = parser.parse_args()
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201

    def put(self, user_id):
        pass

    def delete(self, user_id):
        pass
