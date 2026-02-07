from flask import  request, Blueprint
from .gcpdao import Dao , Cantiere, Umarell
from google.cloud.exceptions import Conflict, NotFound ##Not found per update
from google.cloud import pubsub_v1
import json

api=Blueprint("api",__name__)
dao=Dao()

project_id="umarellcantieriesame"
request_topic_id ="cantieri"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, request_topic_id)



@api.get("/clean")
def clean():
    dao.clean()
    return "Ok", 200

@api.post("/umarell/<id>")
def add_umarell(id):

    data = request.json

    try:
        data['id'] = id
        umarell = Umarell.from_dict(data)
        rv = dao.add_umarell(umarell)

    except ValueError:
        return "Invalid umarell", 400
    
    except KeyError:
        return "Invalid umarell", 400
    
    except Conflict:
        return "Umarell già presente", 409
   
    return  rv, 201

@api.post("/cantiere/<id>")
def add_cantiere(id):

    data = request.json

    try:
        data['id'] = id
        cantiere = Cantiere.from_dict(data)
        rv = dao.add_cantiere(cantiere)

        ##PARTE PUBSUB###########################
        message = {
            "indirizzo":rv['indirizzo'],
            "cap":rv['cap']
        }
        publisher.publish(
            topic_path,
            json.dumps(message).encode("utf-8")
        )

        print(f"PUBBLICATO: {message}, nel topic: {topic_path}\n")
        #################################
    
    except ValueError:
        return "Invalid Cantiere", 400
    
    except KeyError:
        return "Invalid Cantiere", 400
    
    except Conflict:
        return "Cantiere già presente", 409
    return  rv, 201
    
    
@api.get("/umarell/<id>")
def get_umarell(id):

    try:
        umarell = dao.get_umarell(id)
    except NotFound as e:
        return e.message, 404
    
    return umarell, 200


    
@api.get("/cantiere/<id>")
def get_cantiere(id):

    try:
        cantiere = dao.get_cantiere(id)
    except NotFound as e:
        return e.message, 404
    
    return cantiere, 200
