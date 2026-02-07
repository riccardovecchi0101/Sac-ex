from flask import Flask, request, g
from api.api import api
from webapp.webapp import webapp

from werkzeug.exceptions import HTTPException

import logging
from logging.handlers import RotatingFileHandler
import os
import time

# --------------------------------------------------
# APP
# --------------------------------------------------
app = Flask(__name__)

# --------------------------------------------------
# LOGGING SU FILE
# --------------------------------------------------
if not os.path.exists("logs"):
    os.mkdir("logs")

open("logs/api.log", "w").close()

handler = RotatingFileHandler(
    "logs/api.log",
    maxBytes=2_000_000,
    backupCount=3
)

formatter = logging.Formatter(
    "%(levelname)s %(message)s"
)

handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# --------------------------------------------------
# BLUEPRINT
# --------------------------------------------------
app.register_blueprint(api, url_prefix="/api/v1/")
app.register_blueprint(webapp, url_prefix="/")

# --------------------------------------------------
# TIMER REQUEST
# --------------------------------------------------
@app.before_request
def start_timer():
    g.start_time = time.time()

# --------------------------------------------------
# LOG RESPONSE (GET / POST / ERRORI)
# --------------------------------------------------
@app.after_request
def log_response(response):
    duration = round((time.time() - g.start_time) * 1000)

    method = request.method
    path = request.path
    status = response.status_code

    # ---- GET ----
    if method == "GET":
        app.logger.info(
            f"[GET ] {path} → {status} ({duration}ms)"
        )

    # ---- POST OK ----
    elif method == "POST" and status < 400:
        app.logger.info(
            f"[POST OK ] {path} → {status} ({duration}ms)"
        )

    # ---- POST ERR ----
    elif method == "POST" and status >= 400:
        body = request.get_json(silent=True) or request.data.decode("utf-8", errors="ignore")
        app.logger.error(
            f"[POST ERR] {path} → {status} ({duration}ms) body={body}"
        )

    # ---- SERVER ERROR ----
    if status >= 500:
        app.logger.error(
            f"[SERVER ERROR] {method} {path} → {status}"
        )

    return response

# --------------------------------------------------
# ERROR HANDLER CORRETTO
# --------------------------------------------------
@app.errorhandler(Exception)
def handle_exception(e):

    # ---- ERRORI HTTP (404, 400, 405, ecc) ----
    if isinstance(e, HTTPException):
        app.logger.warning(
            f"[HTTP {e.code}] {request.method} {request.path}"
        )
        return {
            "error": e.name,
            "message": e.description
        }, e.code

    # ---- VERI SERVER ERROR (5xx) ----
    app.logger.exception(
        f"[SERVER EXCEPTION] {request.method} {request.path}"
    )
    return {"error": "Internal Server Error"}, 500

# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    app.run(host="localhost", port=8080)

