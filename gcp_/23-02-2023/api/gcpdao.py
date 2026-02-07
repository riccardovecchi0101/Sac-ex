import json
from .classes import Chirps
from google.cloud import firestore
from google.cloud.exceptions import NotFound

class Dao(object):
    def __init__(self):
        self.db = firestore.Client()

    def add_message(self, m: Chirps):
        self.db.collection("messages").document(m.id).create(m.to_dict())
        
        for t in m.hashtag:
            topic_ref = self.db.collection("hashtags").document(t).get()

            data = {'messages':[{'id':m.id}]}

            if not topic_ref.exists:
                self.db.collection("hashtags").document(t).create(data)
            else:
                data = topic_ref.to_dict().get("messages",[])
                data.append({"id":m.id})
                self.db.collection("hashtags").document(t).update({"messages":data})

        return m.to_dict()

                                                            #update per fare update errore se non da oggetto
    def get_message(self, id:str):
        message = self.db.collection("messages").document(id).get()
        if not message.exists:
            raise NotFound("Notfound")
        
        return message.to_dict()
        

    def messages_from_topic(self, topic:str):

        topic = "#"+topic
        topics_ref = self.db.collection("hashtags").document(topic).get()
        if not topics_ref.exists:
            raise NotFound("Notfound")

        dict_  = topics_ref.to_dict()
        ids = []
        for id in dict_['messages']:
            ids.append(id['id'])
        return ids




    def clean(self):
        docs_messages = self.db.collection("messages").stream()
        docs_hashtags = self.db.collection("hashtags").stream()

        for doc in docs_messages:
            doc.reference.delete()

        for doc in docs_hashtags:
            doc.reference.delete()

if __name__=='__main__':
    c=Dao() 
#    c.populate_db()
    c.clean_db()