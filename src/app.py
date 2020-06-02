import os
import time
from threading import Thread
from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    redirect,
    url_for,
    send_from_directory,
    abort,
)


from src.dbconfig import init_db
from src.routes import init_routes

app = Flask(__name__)
db = init_db(app)
routes = init_routes(routes)


@app.route("/", methods=["GET"])
def index():
    return redirect("/products")


@app.template_filter()
def format_price(price):
    """1000 -> $1.000"""
    return "$" + format(price, ",d").replace(",", ".")
