from flask import request
from flask_restful import Resource, reqparse
import json
import requests

API_KEY = '9Llhkz9updYQTisodM+hQg==2Q21ObLNXqb5J2WU'
api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'
headers = {'Content-Type': 'application/json', 'X-Api-Key': API_KEY}

class dishCollection:
    def __init__(self):
        self.counter = 0
        self.dishes_by_name = {}
        self.dishes_by_id = {}

    def insertDish(self, dish, name):
        self.counter += 1
        new_dish = {
            "name": name,
            "ID": self.counter,
            "cal": dish[0]["calories"] if len(dish) is 1 else dish[0]["calories"] + dish[1]["calories"],
            "size": dish[0]["serving_size_g"] if len(dish) is 1 else dish[0]["serving_size_g"] + dish[1]["serving_size_g"],
            "sodium": dish[0]["sodium_mg"] if len(dish) is 1 else dish[0]["sodium_mg"] + dish[1]["sodium_mg"],
            "sugar": dish[0]["sugar_g"] if len(dish) is 1 else dish[0]["sugar_g"] + dish[1]["sugar_g"],
        }
        self.dishes_by_name[name] = new_dish
        self.dishes_by_id[self.counter] = new_dish


global DC
DC = dishCollection()

class dishes(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize parse
        parser.add_argument('name', required=True)  # add args

        if request.content_type != 'application/json':
            return 0, 415
        if 'name' not in request.json:
            return -1, 400
        data = parser.parse_args()
        if data["name"] in DC.dishes_by_name:
            return -2, 400
        
        query = data["name"]
        response = requests.get(api_url.format(query),headers=headers)
        if response.status_code == requests.codes.ok:
            res_data = json.loads(response.text)
            if len(res_data) is not 0:
                DC.insertDish(res_data, query)
                return DC.counter, 201
            else:
                return -3, 400
        else:
            return -4, 400

    def get(self):
        return DC.dishes_by_id, 200
    
    def delete(self):
        return -1, 400

class dishID(Resource):
    global DC

    def get(self, id):
        if id not in DC.dishes_by_id:
            return -5, 404
        return DC.dishes_by_id[id], 200

    def delete(self, id):
        if id not in DC.dishes_by_id:
            return -5, 404
        dish_to_delete = DC.dishes_by_id[id]
        name_of_dish = dish_to_delete["name"]
        del DC.dishes_by_id[id]
        del DC.dishes_by_name[name_of_dish]
        return id, 200

class dishName(Resource):
    global DC

    def get(self, name):
        if name not in DC.dishes_by_name:
            return -5, 404
        dish_to_get = DC.dishes_by_name[name]
        id_of_dish = dish_to_get["ID"]
        return id_of_dish, 200

    def delete(self, name):
        if name not in DC.dishes_by_name:
            return -5, 404
        dish_to_delete = DC.dishes_by_name[name]
        id_of_dish = dish_to_delete["ID"]
        del DC.dishes_by_id[id_of_dish]
        del DC.dishes_by_name[name]
        return id_of_dish, 200