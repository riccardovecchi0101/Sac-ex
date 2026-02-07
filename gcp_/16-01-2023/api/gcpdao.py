import json
from .classes import Consumo
from google.cloud import firestore
from google.cloud.exceptions import NotFound
from .utils import date_from_str, str_from_date
from datetime import datetime,timezone

class Dao(object):
    def __init__(self):
        self.db = firestore.Client()

    def add_consumo(self, c: Consumo, date: str):

        consumo_ref = self.db.collection('consumi')
        consumo_dict = c.to_dict()
        consumo_dict['date_ts'] = date_from_str(date)
        consumo_ref.document(date).create(consumo_dict)

    def get_interpolated_consumo(self,date:str):

        consumi_precedenti = []
        date_ts = date_from_str(date)
        print(f"data richiesta{date}")
        consumi = self.db.collection('consumi').where('date_ts', '<', date_ts ).order_by('date_ts', direction=firestore.Query.DESCENDING).limit(2).stream()

        print("itero")
        for c in consumi:
            print(c)
            consumi_precedenti.append(c.to_dict())

        if len(consumi_precedenti) == 0:
            return {'value':0, 'isInterpolated':True}
        
        if len(consumi_precedenti) == 1:
            first_value = consumi_precedenti[0]
            return {'value': (first_value['value']), 'isInterpolated':True}
        
        first_consumo = consumi_precedenti[1]
        second_consumo = consumi_precedenti[0]

        first_value = first_consumo['value']
        second_value = second_consumo['value']

        first_date = first_consumo['date_ts']
        second_date = second_consumo['date_ts']


        date_ts = date_from_str(date).replace(tzinfo=timezone.utc)

        deltatime1 = (second_date-first_date).total_seconds()
        deltatime2 = (date_ts - second_date).total_seconds()

        interpolated_value = second_value + (((second_value-first_value)/deltatime1)*deltatime2)

        return {'value':interpolated_value, 'isInterpolated':True}



    def get_consumo(self, date:str):
        '''Si vuole calcolare il valore dei consumi cx al tempo tx.
        Se sono presenti almeno due letture nel database precedenti a tx si considerano
        le ultime due letture. Sia c1 al tempo t1 e c2 al tempo t2, con t1 < t2 < tx.
        cx= c2 + c2 −c1
        t2 −t1
        (tx−t2)
        Se è presente una sola lettura c1 precedente a txsi considera che i consumi non
        siano variati dall’ultima lettura. Quindi Il valore al tempo t2 diventa:
        cx= c1
        Se non è presente nessun valore, il risultato è semplicemente cx= 0
        '''

        ###CASO 1 --> consumo presente ###
        consumo_ref = self.db.collection('consumi').document(date).get()
        if consumo_ref.exists:
            dict_ = consumo_ref.to_dict()
            return {'value': dict_['value'], 'isInterpolated': dict_['isInterpolated']}
        
        ##caso 2 --> consumo interpolato
        else:
            rv = self.get_interpolated_consumo(date)
            return rv




    def clean(self):
        docs = self.db.collection('consumi').stream()
        for doc in docs:
             doc.reference.delete()
