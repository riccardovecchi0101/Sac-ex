import json
from .classes import Cantiere, Umarell
from google.cloud import firestore
from google.cloud.exceptions import NotFound

class Dao(object):
    def __init__(self):
        self.db = firestore.Client()

    def add_umarell(self, u: Umarell):
        u_dict = u.to_dict()
        id = u_dict['id']
        del(u_dict['id'])
        umarell_ref = self.db.collection('umarell')
        umarell_ref.document(id).create(u_dict)
        return u_dict

    def add_cantiere(self, c: Cantiere):
        c_dict = c.to_dict()
        id = c_dict['id']
        del(c_dict['id'])
        cantiere_ref = self.db.collection('cantieri')
        cantiere_ref.document(id).create(c_dict)
        return c_dict
    
    def get_umarell(self, id:int):
        umarell = self.db.collection('umarell').document(id).get()
        if not umarell.exists:
            raise NotFound('Umarell not found') 
        
        return umarell.to_dict()
    
    def get_cantiere(self, id:int):
        cantiere = self.db.collection('cantieri').document(id).get()
        if not cantiere.exists:
            raise NotFound('Cantiere not found')
        
        return cantiere.to_dict()


    def clean(self):
        cantieri = self.db.collection('cantieri').stream()
        umarell = self.db.collection('umarell').stream()

        for c in cantieri:
            c.reference.delete()

        for u in umarell:
            u.reference.delete()

if __name__=='__main__':
    c=Dao() 
#    c.populate_db()
    c.clean_db()