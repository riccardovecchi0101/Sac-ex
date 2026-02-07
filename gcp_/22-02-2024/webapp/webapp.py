from flask import Blueprint, render_template, request
from api.gcpdao import Dao
from google.cloud.exceptions import  NotFound


webapp = Blueprint('webapp', __name__, template_folder='templates', static_folder='static')
dao = Dao()


@webapp.get('/')
def webapp_get_index():
    return render_template('form.html'), 200

@webapp.post('/')
def cerca_cap():
    cap = request.form['cap']
    vogliocantieri = False
    voglioumarell = False

    if request.form.get('umarell'):
        voglioumarell=True

    if request.form.get('cantieri'):
        vogliocantieri = True

    try:
        cap = int(cap)
    except: return render_template("404.html", cap="cap non valido")
    
    umarell = dao.db.collection('umarell').where('cap', '==', cap).stream()
    cantieri = dao.db.collection('cantieri').where('cap', '==', cap).stream()


    umarell_list = []
    cantieri_list = []

    if voglioumarell:
        for u in umarell:
            umarell_list.append(u.to_dict())

    if vogliocantieri:
        for c in cantieri:
            cantieri_list.append(c.to_dict())

    if (len(umarell_list) == 0 and voglioumarell) or (len(cantieri_list) == 0 and vogliocantieri):
        return render_template("404.html", cap=cap)

    return render_template("form.html", umarell=umarell_list, cantieri=cantieri_list)
    