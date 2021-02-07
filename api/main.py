from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# making Flask instance
app = Flask(__name__)
# making Api wrapper
api = Api(app)
# configuring app for the db & then making SQLAlchemy wrapper
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# UserModel class
class UserModel(db.Model):
    # making id field within model; must be unique
    id = db.Column(db.Integer, primary_key=True)
    # making username field within model; max length of 254; requires that this field has some info
    username = db.Column(db.String(254), nullable=False)
    # making password field within model; max length of 254; requries that this field has some info
    password = db.Column(db.String(254), nullable=False)

    # repr method makes it possible to print this out
    def __repr__(self):
        return f"User(username = {username}, password = {password})"

# only want to do this once or it will write over pre-existing data
#db.create_all()

# parsing arguments of user
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("username", type=str, help="Username is required", required=True)
user_put_args.add_argument("password", type=str, help="Password is required", required=True)

# note: not required to provide all arguments here
user_update_args = reqparse.RequestParser()
user_update_args.add_argument("username", type=str, help="Username is required")
user_update_args.add_argument("password", type=str, help="Password is required")

# defines how an object should be serialized
resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String
}

# User class
class User(Resource):
    # get method - serialize 'result' with 'resource_fields'
    @marshal_with(resource_fields)
    def get(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        # abort if couldn't query a user of that user_id
        if not result:
            abort(404, message="Could not find user with that ID")
        return result

    # put method - makes a user dictionary and adds it to the database
    @marshal_with(resource_fields)
    def put(self, user_id):
        args = user_put_args.parse_args()
        # querying to see if there's any user_id's that are equal to the one we're putting in
        result = UserModel.query.filter_by(id=user_id).first()
        if result:
            abort(409, message="User ID already taken")
        user = UserModel(id=user_id, username=args['username'], password=args['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201
    
    # patch method - will update a user based on what arguments are passed in (not all are required)
    @marshal_with(resource_fields)
    def patch(self, user_id):
        args = user_update_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="Cannot update a user that does not exist")
        if args["username"]:
            result.username = args["username"]
        if args["password"]:
            result.password = args["password"]
        db.session.commit()
        return result

    # delete method - querying a user and then deleting if that user_id exists; otherwise, abort
    @marshal_with(resource_fields)
    def delete(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="Cannot delete a user that does not exist")
        db.session.delete(result)
        db.session.commit()
        return '', 204

api.add_resource(User,"/user/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True)