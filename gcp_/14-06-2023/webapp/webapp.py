from flask import Blueprint, render_template, request
from api.gcpdao import Dao
webapp = Blueprint('webapp', __name__, template_folder='templates', static_folder='static')
import ipaddress

dao = Dao()
@webapp.get('/')
def webapp_get():
    
    rules_ref = dao.db.collection("routing").stream()
    rules = []
    for rule in rules_ref:
        rules.append(rule.to_dict())
    

    return render_template("form.html", rules=rules), 200
    

@webapp.post('/getdata')
def webapp_get_data():

    ip = request.form['ip']

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        render_template("error.html"), 404

    rules_ref = dao.db.collection("routing").stream()
    rules = []
    for rule in rules_ref:   
        rules.append(rule.to_dict())

    correct_rule = dao.get_matching_rule(ip)


    


    return render_template("form.html", rules=rules, correct_rule=correct_rule ), 200
