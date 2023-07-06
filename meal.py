from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import pymongo
import json
import sys
import requests
import os

# MongoDB connection details
# mongo_host = os.getenv('MONGO_HOST', '')
# mongo_port = int(os.getenv('MONGO_PORT', '27017'))
# mongo_username = os.getenv('MONGO_USERNAME', '')
# mongo_password = os.getenv('MONGO_PASSWORD', '')

client = pymongo.MongoClient("mongodb://mongo:27017/")
# client = pymongo.MongoClient(host=mongo_host, port=mongo_port, username=mongo_username, password=mongo_password)
db = client["db"]
dishesColl = db["dishes"]
mealsColl = db["meals"]

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
        doc = mealsColl.find_one({"name": data["name"]})
        if doc is not None:
            return -2, 400

        doc_appetizer = dishesColl.find_one({"_id": int(data["appetizer"])})
        doc_main = dishesColl.find_one({"_id": int(data["main"])})
        doc_dessert = dishesColl.find_one({"_id": int(data["dessert"])})
        if not doc_appetizer or not doc_main or not doc_dessert:
            return -5, 404
        
        meal_name = data["name"]
        new_meal = mealsColl.insert_one({
            "name": meal_name,
            "appetizer": doc_appetizer["_id"],
            "main": doc_main["_id"],
            "dessert": doc_dessert["_id"],
            "cal": doc_appetizer["cal"] + doc_main["cal"] + doc_dessert["cal"],
            "sodium": doc_appetizer["sodium"] + doc_main["sodium"] + doc_dessert["sodium"],
            "sugar": doc_appetizer["sugar"] + doc_main["sugar"] + doc_dessert["sugar"],
        })

        return new_meal["_id"], 201

    def get(self):
        diet = request.args.get('diet')  # Replace 'param_name' with the actual query parameter name
        if diet is not None:
            base_url = request.host_url + request.script_root
            doc_diet = requests.get(base_url, params=diet)
            response = mealsColl.find({
                "cal": {"$lte": doc_diet["cals"]},
                "sodium": {"$lte": doc_diet["sodium"]},
                "sugar": {"$lte": doc_diet["sugar"]}
            })
            return response, 200
        else:
            # Query parameter doesn't exist, perform default action
            return mealsColl.find(), 200
        
    
    def delete(self):
        return -1, 400

class mealID(Resource):
    def get(self, id):
        doc = mealsColl.find_one({"_id": id})
        if doc is None:
            return -5, 404
        return doc["_id"], 200

    def delete(self, id):
        doc = mealsColl.find_one({"_id": id})
        if doc is None:
            return -5, 404
        mealsColl.delete_one({"_id": id})
        return id, 200
    
    def put(self, id):
        if request.content_type != 'application/json':
            return 0, 415
        
        doc = mealsColl.find_one({"_id": id})
        if doc is None:
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
        doc_by_name = mealsColl.find_one({"_id": id})
        if doc_by_name is not None:
            return -2, 400


        doc_appetizer = dishesColl.find_one({"_id": int(data["appetizer"])})
        doc_main = dishesColl.find_one({"_id": int(data["main"])})
        doc_dessert = dishesColl.find_one({"_id": int(data["dessert"])})
        if not doc_appetizer or not doc_main or not doc_dessert:
            return -5, 404

        updated_meal = mealsColl.update_one({
            "name": data["name"],
            "appetizer": doc_appetizer["_id"],
            "main": doc_main["_id"],
            "dessert": doc_dessert["_id"],
            "cal": doc_appetizer["cal"] + doc_main["cal"] + doc_dessert["cal"],
            "sodium": doc_appetizer["sodium"] + doc_main["sodium"] + doc_dessert["sodium"],
            "sugar": doc_appetizer["sugar"] + doc_main["sugar"] + doc_dessert["sugar"],
        })

        return updated_meal["_id"], 200

class mealName(Resource):
    def get(self, name):
        doc = mealsColl.find_one({"name": name})
        if doc is None:
            return -5, 404
        return doc, 200

    def delete(self, name):
        doc = mealsColl.find_one({"name": name})
        if doc is None:
            return -5, 404
        id = doc["_id"]
        mealsColl.delete_one({"name": name})
        return id, 200
