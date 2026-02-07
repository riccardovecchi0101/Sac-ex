
from dataclasses import dataclass
import re 

@dataclass
class Partecipant():

    firstName:str
    lastName:str
    order: int

    def __post_init__(self):
        if len(self.firstName) <= 0 or len(self.lastName) <=0 or self.order is None:
            raise ValueError
        
    def to_dict(self):
        return {'firstName': self.firstName, 'lastName':self.lastName, 'order':self.order}

    def from_dict(partecipant_dict):
        try:
            return Partecipant(partecipant_dict['name'], partecipant_dict['surname'], partecipant_dict['order'])
        except KeyError:
            raise ValueError('invalid dictionary')

