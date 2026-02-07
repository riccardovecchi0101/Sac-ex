from flask import Blueprint, render_template, request
from api.gcpdao import Dao, firestore
from api.api import time
from google.cloud.exceptions import Conflict, NotFound


webapp = Blueprint('webapp', __name__, template_folder='templates', static_folder='static')
dao = Dao()


@webapp.get('/')
def webapp_get_index():
    consumi=[]
    collection_ref = dao.db.collection('consumi').order_by('date_ts',direction=firestore.Query.DESCENDING).limit(12).stream()
    for c in collection_ref:
        if str(c.id).startswith("1"):
            dict_ = c.to_dict()
            dict_['id'] = str(c.id)
            consumi.append(dict_)

    return render_template('form.html', consumi=consumi), 200


@webapp.get('/consumo/<id>')
def webapp_consumo(id):
    collection_ref = dao.db.collection('consumi').document(id).get()
    bolletta = collection_ref.to_dict()
    return render_template("bolletta.html", bolletta=bolletta)

