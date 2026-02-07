
from dataclasses import dataclass
import re 

@dataclass
class Umarell:

    id:int
    nome:str
    cognome:str
    cap:int

    def __post_init__(self):
        if len(self.nome) <= 0 or len(self.cognome) <= 0 or type(self.cap) != int:
            raise(ValueError)
        
    def to_dict(self):
        return {'id': self.id, 'nome':self.nome, 'cognome':self.cognome, 'cap':self.cap}

    def from_dict(umarell_dict):
        try:
            return Umarell(umarell_dict['id'], umarell_dict['nome'], umarell_dict['cognome'], umarell_dict['cap'])
        except KeyError:
            raise ValueError('invalid dictionary')

@dataclass
class Cantiere:
    
    id:int
    indirizzo: str
    cap: int

    def __post_init__(self):
        if len(self.indirizzo) <= 0 or type(self.cap) != int:
            raise(ValueError)
        
    def to_dict(self):
        return {'id': self.id, 'indirizzo':self.indirizzo,  'cap':self.cap}

    def from_dict(cantiere_dict):
        try:
            return Cantiere(cantiere_dict['id'], cantiere_dict['indirizzo'],  cantiere_dict['cap'])
        except KeyError:
            raise ValueError('invalid dictionary')