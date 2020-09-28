from flask import Flask, request
from flask_restx import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


@app.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


# Resourceful Routing Sample: users
users = {}


@api.route('/<string:user_id>')
class TodoSimple(Resource):
    def get(self, user_id):
        return {user_id: users[user_id]}

    def put(self, todo_id):
        users[user_id] = request.form['data']
        return {user_id: users[user_id]}


if __name__ == '__main__':
    app.run(debug=True)
