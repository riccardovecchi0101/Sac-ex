from flask import  request, Blueprint
from .gcpdao import Dao , Chirps
from google.cloud.exceptions import Conflict, NotFound ##Not found per update
import re

from google.cloud import pubsub_v1

from .utils import get_hashtags
import time
import uuid
import json
#time.time_ns()


api=Blueprint("api",__name__)
dao=Dao()

project_id = "secretsantaesame"



@api.post("/clean")
def clean():
    dao.clean()
    return "Ok", 200

@api.post("/chirps")
def add_message():

    data = request.data.decode("utf-8")

    try:
        parsed = json.loads(data)
        if isinstance(parsed, dict):
            return "Input non valido", 400
    except: pass

    if type(data) != str:
        return "Input non valido",400

    
    data = json.loads(data)
    hastags = get_hashtags(data)
    hastags = list(dict.fromkeys(hastags))
    timestamp = str(time.time_ns())
    id = str(uuid.uuid1())

    try:
        dict_ = {'id':id, 'message':data, 'timestamp':timestamp, 'hashtags':hastags}
        chirp = Chirps.from_dict(dict_)
        dao.add_message(chirp)

    except ValueError:
        return "Input non valido", 400
    
    return dict_,  201

@api.get("/chirps/<id>")
def get_destinatario(id):

    try:
        rv = dao.get_message(id)
    except NotFound as e:
        return e.message, 404
        
    return rv, 200


@api.get("/topics/<topic>")
def get_topic(topic):

    try:
        rv = dao.messages_from_topic(topic)
    except NotFound:
        return "Not Found", 404
    
    return rv , 200


    
    
