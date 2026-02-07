
from dataclasses import dataclass
import re 

@dataclass
class Consumo():

    value:int
    isInterpolated:bool

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError
        
    def to_dict(self):
        return {'value':self.value, 'isInterpolated':self.isInterpolated}

    def from_dict(consumo_dict):
        try:
            return Consumo(value = consumo_dict['value'], isInterpolated=consumo_dict['isInterpolated'])
        except KeyError:
            raise ValueError('invalid dictionary')

