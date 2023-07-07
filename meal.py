from flask import request
from flask_restful import Resource, reqparse
from dish import DC

class mealCollection:
    def __init__(self):
        self.counter = 0
        self.meals_by_name = {}
        self.meals_by_id = {}
        self.dishes = DC.dishes_by_id

    def set_up_meal(self, appetizer_id, main_id, dessert_id):
        appetizer = self.dishes[appetizer_id]
        main = self.dishes[main_id]
        dessert = self.dishes[dessert_id]
        return appetizer, main, dessert

    def insert_meal(self, meal):
        appetizer = meal["appetizer"]
        main = meal["main"]
        dessert = meal["dessert"]
        self.counter += 1
        new_meal = {
            "name": meal["name"],
            "ID": self.counter,
            "appetizer": appetizer["ID"],
            "main": main["ID"],
            "dessert": dessert["ID"],
            "cal": appetizer["cal"] + main["cal"] + dessert["cal"],
            "sodium": appetizer["sodium"] + main["sodium"] + dessert["sodium"],
            "sugar": appetizer["sugar"] + main["sugar"] + dessert["sugar"],
        }
        self.meals_by_name[meal["name"]] = new_meal
        self.meals_by_id[self.counter] = new_meal

    def update_meal(self, meal, id):
        appetizer = meal["appetizer"]
        main = meal["main"]
        dessert = meal["dessert"]
        self.meals_by_id[id] = {
            "name": meal["name"],
            "ID": id,
            "appetizer": appetizer["ID"],
            "main": main["ID"],
            "dessert": dessert["ID"],
            "cal": appetizer["cal"] + main["cal"] + dessert["cal"],
            "sodium": appetizer["sodium"] + main["sodium"] + dessert["sodium"],
            "sugar": appetizer["sugar"] + main["sugar"] + dessert["sugar"],
        }
        self.meals_by_name[meal["name"]] = self.meals_by_id[id]

MC = mealCollection()


class meals(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize parse
        parser.add_argument('name', required=True)  # add args
        parser.add_argument('appetizer', required=True)  # add args
        parser.add_argument('main', required=True)  # add args
        parser.add_argument('dessert', required=True)  # add args

        if request.content_type != 'application/json':
            return 0, 415
        for param in ['name', 'appetizer', 'main', 'dessert']:
            if param not in request.json:
                return -1, 400
        
        data = parser.parse_args()
        if data["name"] in MC.meals_by_name:
            return -2, 400

        if int(data["appetizer"]) not in MC.dishes or int(data["main"]) not in MC.dishes or int(data["dessert"]) not in MC.dishes:
            return -5, 404
        appetizer, main, dessert = MC.set_up_meal(int(data["appetizer"]), int(data["main"]), int(data["dessert"]))

        meal_name = data["name"]
        meal = {
            "name": meal_name,
            "appetizer": appetizer,
            "main": main,
            "dessert": dessert
        }
        MC.insert_meal(meal)
        return MC.counter, 201

    def get(self):
        return MC.meals_by_id, 200
    
    def delete(self):
        return -1, 400

class mealID(Resource):
    global MC

    def get(self, id):
        if id not in MC.meals_by_id:
            return -5, 404
        return MC.meals_by_id[id], 200

    def delete(self, id):
        if id not in MC.meals_by_id:
            return -5, 404
        meal_to_delete = MC.meals_by_id[id]
        name_of_meal = meal_to_delete["name"]
        del MC.meals_by_id[id]
        del MC.meals_by_name[name_of_meal]
        return id, 200
    
    def put(self, id):
        if request.content_type != 'application/json':
            return 0, 415
        if id not in MC.meals_by_id:
            return -5, 404
        
        parser = reqparse.RequestParser()  # initialize parse
        parser.add_argument('name', required=True)  # add args
        parser.add_argument('appetizer', required=True)  # add args
        parser.add_argument('main', required=True)  # add args
        parser.add_argument('dessert', required=True)  # add args

        for param in ['name', 'appetizer', 'main', 'dessert']:
            if param not in request.json:
                return -1, 400
        
        data = parser.parse_args()
        if data["name"] in MC.meals_by_name:
            return -2, 400

        if int(data["appetizer"]) not in MC.dishes or int(data["main"]) not in MC.dishes or int(data["dessert"]) not in MC.dishes:
            return -5, 404
        appetizer, main, dessert = MC.set_up_meal(int(data["appetizer"]), int(data["main"]), int(data["dessert"]))

        meal_name = data["name"]
        meal = {
            "name": meal_name,
            "appetizer": appetizer,
            "main": main,
            "dessert": dessert
        }
        MC.update_meal(meal, id)
        return MC.counter, 201

class mealName(Resource):
    global MC

    def get(self, name):
        if name not in MC.meals_by_name:
            return -5, 404
        return MC.meals_by_name[name], 200

    def delete(self, name):
        if name not in MC.meals_by_name:
            return -5, 404
        meal_to_delete = MC.meals_by_name[name]
        id_of_meal = meal_to_delete["ID"]
        del MC.meals_by_id[id_of_meal]
        del MC.meals_by_name[name]
        return id_of_meal, 200
