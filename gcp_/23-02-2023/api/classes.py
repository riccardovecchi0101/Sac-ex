
from dataclasses import dataclass
import re 

@dataclass
class Chirps():

    id: str
    message: str
    hashtag: list
    timestamp: int

    def __post_init__(self):
        if len(self.message) > 100 or len(self.message) < 1:
            raise ValueError
        
    def to_dict(self):
        return {'id': self.id, 'message':self.message, 'hashtags':self.hashtag, 'timestamp':self.timestamp}

    def from_dict(chirps_dict):
        try:
            return Chirps(chirps_dict['id'], chirps_dict['message'], chirps_dict['hashtags'], chirps_dict['timestamp'])
        except KeyError:
            raise KeyError('invalid dictionary')

