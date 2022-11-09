from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHMEY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class CiteModel(db.Model):

    id = db.Column(db.BIGINT, primary_key=True)
    context = db.Column(db.String(100), nullable=False)
    nameOfBook = db.Column(db.String(100))
    votes = db.Column(db.Integer)

    def __repr__(self):
        return f"Cite(context={context}, nameOfBook = {nameOfBook}, votes={votes})"


db.create_all()
cite_put_args = reqparse.RequestParser()
cite_put_args.add_argument(
    "context", type=str, help="Name of the cite", required=True)
cite_put_args.add_argument("nameOfBook", type=str,
                           help="Name of book of the cite", required=True)
cite_put_args.add_argument(
    "votes", type=int, help="Votes of the cite", required=True)
cite_update_args = reqparse.RequestParser()
cite_update_args.add_argument("context", type=str, help="Name of the cite")
cite_update_args.add_argument("nameOfBook", type=str, help="Name of the book")
cite_update_args.add_argument("votes", type=int, help="Votes on the cite")
resurce_fileds = {
    'id': fields.Integer,
    'context': fields.String,
    'nameOfBook': fields.String,
    'votes': fields.Integer
}


class Cite(Resource):
    @marshal_with(resurce_fileds)
    def get(self, cite_id):
        result = CiteModel.query.filter_by(id=cite_id).first()
        return result

    @marshal_with(resurce_fileds)
    def put(self, cite_id):
        args = cite_put_args.parse_args()
        result = CiteModel.query.filter_by(id=cite_id).first()
        if result:
            abort(409, message="Video id taken...")

        cite = CiteModel(
            id=cite_id, context=args['context'], nameOfBook=args['nameOfBook'], votes=args['votes'])
        db.session.add(cite)
        db.session.commit()
        return cite, 201

    @marshal_with(resurce_fileds)
    def patch(self, cite_id):
        args = cite_update_args.parse_args()
        result = CiteModel.query.filter_by(id=cite_id).first()
        if not result:
            abort(409, message="Video id taken...")

        if args['context']:
            result.context = args['context']
        if args['nameOfBook']:
            result.nameOfBook = args['nameOfBook']
        if args['votes']:
            result.votes = args['votes']
            

        db.session.commit()
        return result


api.add_resource(Cite, "/cite/<int:cite_id>")

if __name__ == '__main__':
    app.run(debug=True)  # Debug mod on
