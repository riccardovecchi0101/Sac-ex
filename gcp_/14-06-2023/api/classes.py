from dataclasses import dataclass
from .utils import check_correctnes_of_parametes


class ValidationError(Exception):
    pass


@dataclass
class routing_rule:

    ip: str
    netmaskCIDR: int
    gw: str
    device: str

    def __post_init__(self):
        
        if type(self.ip) != str or type(self.netmaskCIDR) != int or type(self.gw) != str or type(self.device) != str :
            raise(ValueError)
        
        if not check_correctnes_of_parametes(self.ip, self.netmaskCIDR, self.gw):
            raise (ValueError)


    def to_dict(self):
        return {
            'ip':self.ip,
            'netmaskCIDR':self.netmaskCIDR,
            'gw':self.gw,
            'device': self.device
        }

    @staticmethod
    def from_dict(nwrule_dict):
        try:
            return routing_rule (
                ip= nwrule_dict['ip'],
                netmaskCIDR= nwrule_dict['netmaskCIDR'],
                gw= nwrule_dict['gw'],
                device= nwrule_dict['device']
                
            )
        except KeyError as e:
            print("manca campo\n")
            raise ValueError(f"Campo mancante: {e}")

