from google.cloud import firestore
from .classes import  routing_rule
from .utils import check_if_rule_matches

class Dao:
    def __init__(self):
        self.db = firestore.Client()
    


    def add_rule(self, id:int, r: routing_rule):    

        rule_collection = self.db.collection("routing")
        rule_collection.document(id).create(r.to_dict())
        return r.to_dict()

    def get_rule(self, id:int):

        rule_ref = self.db.collection("routing").document(id).get()
        if not rule_ref: return None

        return rule_ref.to_dict()


    def update_rule(self, id:int, r:dict):
        rule_ref = self.db.collection("routing").document(id)
        if not rule_ref: return None

        rule_ref.update(r)

        return self.get_rule(id)

    def delete_rule(self, id:int):
        rule_ref = self.db.collection("routing").document(id).get()

        if not rule_ref:
            return False
        
        rule_ref.reference.delete()
        return True
        
    def get_all_rules(self):
        rule_references = self.db.collection("routing").order_by("netmaskCIDR",  direction=firestore.Query.DESCENDING).stream()
        rules = []
        for r in rule_references:
            rules.append(str(r.id))
        
        return rules

    def get_matching_rule(self, ip:str):
        rule_references = self.db.collection("routing").order_by("netmaskCIDR",  direction=firestore.Query.DESCENDING).stream()
        for r in rule_references:
            reference = r.to_dict()
            network = reference['ip'] + "/" + str(reference['netmaskCIDR'])
            if check_if_rule_matches(network, ip):
                return r.id

        return None
        
    
        
    
    def clean(self):
        rules = self.db.collection("routing").stream()

        for r in rules:
            r.reference.delete()


