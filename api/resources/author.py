from api import Resource, reqparse, db
from api.models.author import AuthorModel
from api.schemas.author import author_schema, authors_schema


class AuthorResource(Resource):
    def get(self, author_id=None):
        if author_id is None:
            authors = AuthorModel.query.all()
            # authors_list = [author.to_dict() for author in authors]
            return authors_schema.dump(authors), 200

        author = AuthorModel.query.get(author_id)
        if author:
            return f"Author id={author_id} not found", 404

        return author_schema.dump(author), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        parser.add_argument("surname", required=True)
        author_data = parser.parse_args()
        author = AuthorModel(**author_data)
        db.session.add(author)
        db.session.commit()
        return author_schema.dump(author), 201

    def put(self, author_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("surname")
        author_data = parser.parse_args()
        author = AuthorModel.query.get(author_id)
        if author is None:
            author = AuthorModel(**author_data)
            db.session.add(author)
            db.session.commit()
            return author_schema.dump(author), 201
        for key, value in author_data.items():
            setattr(author, key, value)
        db.session.commit()
        return author_schema.dump(author), 200
