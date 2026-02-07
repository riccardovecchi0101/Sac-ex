from flask import  request, Blueprint
from .gcpdao import Dao , Partecipant
from google.cloud.exceptions import Conflict, NotFound ##Not found per update
import re
import time

#time.time_ns()

api=Blueprint("api",__name__)
dao=Dao()

@api.get("/clean")
def clean():
    dao.clean()
    return "Ok", 200

@api.post("/santa/<email>")
def add_partecipant(email):
    data = request.json

    try:
        data['order'] = time.time_ns()
        print(data)
        p = Partecipant.from_dict(data)
        print("inserito")
        dao.add_partecipant(p, email)
        
    except ValueError:
        return "Input non valido", 400
    
    except Conflict:
        return "Utente già presente", 409
   
    return request.json,  201

@api.get("/santa/<email>")
def get_destinatario(email):

    try:
        rv = dao.get_destinatario(email)
        print(rv)
        if rv is None:
            return "Sei solo", 400
    except NotFound as e:
        return e.message, 404
        

    
    return rv, 200
    
    
