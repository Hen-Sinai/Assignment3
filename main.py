import os
from flask import Flask
from flask_restful import Api
from dish import dishes, dishID, dishName
from meal import meals, mealID, mealName

app = Flask(__name__)  # initialize Flask
api = Api(app)  # create API

api.add_resource(dishes, '/dishes')
api.add_resource(dishID, '/dishes/<int:id>')
api.add_resource(dishName, '/dishes/<string:name>')
api.add_resource(meals, '/meals')
api.add_resource(mealID, '/meals/<int:id>')
api.add_resource(mealName, '/meals/<string:name>')

@app.route('/<path:path>', methods=['GET', 'DELETE'])
def catch_all(path):
    return '-1', 400