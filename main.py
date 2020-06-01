# pylint: disable=missing-function-docstring,missing-module-docstring,wrong-import-position
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

from constants import (
    CentralMayorista,
    LaCaserita,
    Alvi,
    Lider,
    Jumbo,
    TRANSLATIONS,
)

app = Flask(__name__)

import api_controllers

INPUT_FOLDER = "tmp/"


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("get_products"))


# GET and POST models


@app.route("/products/", methods=["GET"])
def get_products():
    search = request.args.get("search", "")
    products = api_controllers.get_products(search=search)
    if request.headers.get("Content-Type") == "application/json":
        return jsonify(products)

    return render_template(
        "products.html", search=search, categories=products["categories"]
    )


@app.route("/products/<pid>/", methods=["GET"])
def product(pid):
    result = api_controllers.get_offers_by_product(pid)
    return render_template(
        "product.html",
        product=result["product"],
        offers=result["offers"],
        similar_products=result["similar_products"],
    )


@app.route("/data/", methods=["GET", "POST"])
def update_data():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return abort(400)
        filename = INPUT_FOLDER + str(time.time()) + "_" + file.filename
        file.save(filename)
        thread = Thread(target=api_controllers.update_data, args=(filename,))
        thread.start()
        return redirect(url_for("update_data", ok="Actualición iniciada correctamente"))

    return render_template(
        "data.html",
        success=request.args.get("ok"),
        error=request.args.get("error"),
        file=sorted([file for file in os.listdir("tmp") if ".csv" in file])[-1],
        mayorista_scrape=api_controllers.get_last_scrape(CentralMayorista.name),
        caserita_scrape=api_controllers.get_last_scrape(LaCaserita.name),
        alvi_scrape=api_controllers.get_last_scrape(Alvi.name),
        lider_scrape=api_controllers.get_last_scrape(Lider.name),
        jumbo_scrape=api_controllers.get_last_scrape(Jumbo.name),
    )


@app.route("/data/<file>", methods=["GET"])
def api_search_result(file):
    return send_from_directory("tmp", file)


@app.route("/scrapes/<provider>/", methods=["POST"])
def scrape(provider):
    element = api_controllers.new_scrape(TRANSLATIONS[provider])
    thread = Thread(target=api_controllers.scrape, args=(provider, element.id))
    thread.start()
    return redirect(
        url_for("update_data", ok=f"Proceso iniciado correctamente ({provider})")
    )


@app.route("/scrapes/<provider>/<file>", methods=["GET"])
def get_scrape_file(provider, file):
    if not os.path.isfile(f"./tmp/scrapes/{provider}/" + file):
        return redirect(
            url_for(
                "update_data",
                error="Se eliminó el archivo, deberías haberlo guardado. "
                + "Puedes obtener la información nuevamente",
            )
        )
    return send_from_directory(f"tmp/scrapes/{provider}/", file)


@app.template_filter()
def format_price(price):
    """1000 -> $1.000"""
    return "$" + format(price, ",d").replace(",", ".")
