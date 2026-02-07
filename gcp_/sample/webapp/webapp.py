from flask import Blueprint, render_template, request
from api.gcpdao import Dao, Partecipant
from api.api import time
from google.cloud.exceptions import Conflict, NotFound


webapp = Blueprint('webapp', __name__, template_folder='templates', static_folder='static')
dao = Dao()


@webapp.get('/')
def webapp_get_index():
    return render_template('form.html'), 200


@webapp.post("/register")
def webapp_register():
    nome = request.form['nome']
    cognome = request.form['cognome']
    email = request.form['email']

    if not nome or not cognome or not email:
         return render_template('form.html', message="manca un campo, babbo di minchia!"), 200
    
    user_dict = {
         'name':nome,
         'surname':cognome,
         'order': time.time_ns()
    }

    try:
        partecipant = Partecipant.from_dict(user_dict)
        dao.add_partecipant(partecipant, email)
    except ValueError:
         return render_template('form.html', message="campi sbagliati, pirla"), 400
    
    except Conflict:
         return render_template('form.html', message="la mail è gia registrata, il furto di identità è reato penale"), 409
    
    return render_template('form.html', message="Sei registrato, non fare minchiate")
         

@webapp.get('/destinatario/<email>')
def webapp_get_destinatario(email):

    email= request.args.get('email')
    try:
        rv = dao.get_destinatario(email)
        if rv is None:
            return render_template("form.html", message="Sei solo come un cane, trovati degli amici")
    except NotFound:
        return render_template("form.html", message="La mail non risulta registrata, se ti senti un comico, vai a fare zelig."), 400
        
    destinatario_dict={
        'nome':rv['toFirstName'],
        'cognome':rv['toLastName'],
        'email':rv['toEmail']
    }

    return render_template("form.html", destinatario=destinatario_dict), 200