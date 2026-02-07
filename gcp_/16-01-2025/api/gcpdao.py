import json
from .classes import Partecipant
from google.cloud import firestore
from google.cloud.exceptions import NotFound

class Dao(object):
    def __init__(self):
        self.db = firestore.Client()

    def add_partecipant(self, p: Partecipant, email:str):
        consumo_ref=self.db.collection('SecretSanta')
        consumo_ref.document(email).create(p.to_dict()) #create se oggetto è gia presente causa conflitto

                                                            #update per fare update errore se non da oggetto
    def get_destinatario(self, email:str):
        
        mittente  = self.db.collection('SecretSanta').document(email).get()

        if not mittente.exists:
            raise NotFound("Notfound")
        
        mittente = mittente.to_dict()
        
        partecipants = []
        docs = self.db.collection('SecretSanta').order_by("order").stream()

        for d in docs:
            dict_= d.to_dict()
            dict_['email'] = d.reference.id
            partecipants.append(dict_)
        
        if len(partecipants) == 1: #sei solo
            return None
        
        con = 0

        for p in partecipants:
            con += 1

            if p['email'] == email:
                if con == len(partecipants):
                    destinatario = partecipants[0]
                else:
                    destinatario = partecipants[con]
                

        rv = {
        "fromEmail":email,
        "fromFirstName": mittente["firstName"],
        "fromLastName":mittente["lastName"],
        "toEmail": destinatario["email"],
        "toFirstName": destinatario["firstName"],
        "toLastName":destinatario["lastName"],
        "receiver":""
        }

        return rv
        





    def clean(self):
        docs = self.db.collection('SecretSanta').stream()
        for doc in docs:
             doc.reference.delete()

if __name__=='__main__':
    c=Dao() 
#    c.populate_db()
    c.clean_db()