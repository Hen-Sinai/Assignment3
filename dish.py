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

API_KEY = '9Llhkz9updYQTisodM+hQg==2Q21ObLNXqb5J2WU'
api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'
headers = {'Content-Type': 'application/json', 'X-Api-Key': API_KEY}

class dishes(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize parse
        parser.add_argument('name', required=True)  # add args

        if request.content_type != 'application/json':
            return 0, 415
        if 'name' not in request.json:
            return -1, 400
        data = request.get_json()
        doc = dishesColl.find_one({"name": data["name"]})
        if doc is not None:
            return -2, 400
        
        name = data["name"]
        response = requests.get(api_url.format(name),headers=headers)
        if response.status_code == requests.codes.ok:
            dish = json.loads(response.text)
            if len(dish) is not 0:
                cals = dish[0]["calories"] if len(dish) is 1 else dish[0]["calories"] + dish[1]["calories"]
                size = dish[0]["serving_size_g"] if len(dish) is 1 else dish[0]["serving_size_g"] + dish[1]["serving_size_g"]
                sodium = dish[0]["sodium_mg"] if len(dish) is 1 else dish[0]["sodium_mg"] + dish[1]["sodium_mg"]
                sugar = dish[0]["sugar_g"] if len(dish) is 1 else dish[0]["sugar_g"] + dish[1]["sugar_g"]
                new_dish = dishesColl.insert_one({
                    "name": name,
                    "cals": cals,
                    "size": size,
                    "sodium": sodium,
                    "sugar": sugar,
                    })
                return str(new_dish.inserted_id), 201
            else:
                return -3, 400
        else:
            return -4, 400

    def get(self):
        cursor = dishesColl.find()
        cursor.rewind()
        cursor_list = list(cursor)
        cursor_json = json.dumps(cursor_list)     # convert list to JSON array
        print(cursor_json)
        return cursor_json, 200
    
    def delete(self):
        return -1, 400

class dishID(Resource):
    def get(self, id):
        doc = dishesColl.find_one({"_id": id})
        if doc is None:
            return -5, 404
        return doc["_id"], 200

    def delete(self, id):
        doc = dishesColl.find_one({"_id": id})
        if doc is None:
            return -5, 404
        dishesColl.delete_one({"_id": id})
        return id, 200

class dishName(Resource):
    def get(self, name):
        doc = dishesColl.find_one({"name": name})
        if doc is None:
            return -5, 404
        return doc, 200

    def delete(self, name):
        doc = dishesColl.find_one({"name": name})
        if doc is None:
            return -5, 404
        id = doc["_id"]
        dishesColl.delete_one({"name": name})
        return id, 200