from flask import request, Blueprint
from .gcpdao import Dao
from .classes import routing_rule
from google.cloud.exceptions import Conflict, NotFound
import os
import json


import json 

api = Blueprint("api", __name__)
dao  = Dao()


@api.post("/clean")
def delete_data():

    dao.clean()
    return "Database pulito", 200

@api.get("/routing/<id>")
def get_network_rule(id):

   # data_requested = request.json
    str_id = str(id)
   
    if not str_id.isnumeric():
        return "bad id", 400

    rule = dao.get_rule(id)
    if rule is None:
        return "Not found", 404
    

    return rule, 200


@api.post("/routing/<id>")
def add_network_rule(id):

    response = request.json

    print("\n")
    print(response)
    print("\n")

    try:
        rule = routing_rule.from_dict(response)
        dao.add_rule(id, rule)
    except ValueError:
        return "invalid item", 400
    except Conflict:
        return "Conflict", 409

    return response, 201


@api.put("/routing/<id>")
def update_network_rule(id):

    response = request.json

    try:
        r = dao.update_rule(id, response)
        if r is None:
            return "error",  400
        
    except NotFound:
        return "rule not found", 404
    
    return r, 200


@api.delete("/routing/<id>")
def delete_network_rule(id):
    deleted = dao.delete_rule(id)

    if not deleted: 
        return "Not Found", 404
    
    return "Deleted", 204


@api.get("/routing")
def get_rules():

    rules = dao.get_all_rules()

    return rules, 200

@api.post("/routing")
def get_rule():

    id = dao.get_matching_rule(request.json)

    if id is None:
        return "q1", 200
    
    return str(id), 200