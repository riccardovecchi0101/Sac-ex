from flask import Flask
from api.api import api
from webapp.webapp import webapp

app = Flask(__name__)
app.register_blueprint(api, url_prefix= "/api/v1/")
app.register_blueprint(webapp, url_prefix="/")




if __name__== '__main__':
    app.run("localhost",8080)