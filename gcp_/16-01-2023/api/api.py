from flask import  request, Blueprint
from .gcpdao import Dao , Consumo
from .utils import date_from_str
from google.cloud.exceptions import Conflict, NotFound ##Not found per update
import re
import time

#time.time_ns()

api=Blueprint("api",__name__)
dao=Dao()

@api.post("/clean")
def clean():
    dao.clean()
    return "Ok", 200

@api.post("/consumi/<data>")
def add_consumo(data):
    requested = request.json

    try:
        if type(requested['value']) != int:
            raise ValueError
        
        if date_from_str(data) is None:
            return "bad data", 400
        
        if(requested['value'] == 0):
            isInterpolated = True
        else:
            isInterpolated = False

        requested['isInterpolated'] = isInterpolated
        consumo = Consumo.from_dict(requested)
        dao.add_consumo(consumo, data)
        
    except ValueError:
        return "Input non valido", 400
    
    except Conflict:
        return "Consumo già presente", 409
    except KeyError:
        return "bad dict", 400
   
    return requested,  201

@api.get("/consumi/<data>")
def get_destinatario(data):

    if date_from_str(data) is None:
        return "bad data", 400

    rv = dao.get_consumo(data)
        
    return rv, 200
    
    
