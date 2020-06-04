from flask import Flask, redirect


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return redirect("/products")


@app.template_filter()
def format_price(price):
    """1000 -> $1.000"""
    return "$" + format(price, ",d").replace(",", ".")
