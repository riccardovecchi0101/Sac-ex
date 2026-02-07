from flask import Blueprint, render_template, request
from api.gcpdao import Dao, Chirps
from api.api import add_message
from google.cloud.exceptions import Conflict, NotFound
import json
from api.utils import get_hashtags
import time, uuid


webapp = Blueprint('webapp', __name__, template_folder='templates', static_folder='static')
dao = Dao()


@webapp.get('/')
def webapp_get_index():
    return render_template('form.html'), 200


@webapp.post("/addmessage")
def webapp_register():
    messaggio = request.form['message']

    try:
        parsed = json.loads(add_message)
        if isinstance(parsed, dict):
            return render_template("form.html", message="input non valido")
    except: pass 

    
    data = messaggio
    hastags = get_hashtags(data)
    hastags = list(dict.fromkeys(hastags))
    timestamp = str(time.time_ns())
    id = str(uuid.uuid1())

    try:
        dict_ = {'id':id, 'message':data, 'timestamp':timestamp, 'hashtags':hastags}
        chirp = Chirps.from_dict(dict_)
        dao.add_message(chirp)
    except ValueError:
        return render_template("form.html", message="input non valido")
    
    return render_template('form.html', message="Messaggio aggiunto")
         

@webapp.post("/searchht")
def get_ht():
    topic = request.form['ht']

    try:
        messages = dao.messages_from_topic(topic)
        content = []
        for m in messages:
            content.append(dao.get_message(m))
    except NotFound:
        return render_template("404.html")
    
    return render_template("messages.html", messages=content, topic = topic)