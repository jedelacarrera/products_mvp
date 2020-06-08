import os
import time
from threading import Thread
from flask import (
    Blueprint,
    abort,
    request,
    render_template,
    send_from_directory,
    redirect,
    url_for,
)
from src.constants import INPUT_FOLDER, CentralMayorista, LaCaserita, Alvi, Lider, Jumbo
from src.routes.data import controllers

data_app = Blueprint("data", __name__, url_prefix="/data")


@data_app.route("/", methods=["GET", "POST"])
def update_data():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return abort(400)
        filename = f"{INPUT_FOLDER}/{time.time()}_{file.filename}"
        file.save(filename)
        thread = Thread(target=controllers.update_data, args=(filename,))
        thread.start()
        return redirect(
            url_for("data.update_data", ok="Actualización iniciada correctamente")
        )

    return render_template(
        "data.html",
        success=request.args.get("ok"),
        error=request.args.get("error"),
        file=sorted([file for file in os.listdir(INPUT_FOLDER) if ".csv" in file])[-1],
        mayorista_scrape=controllers.get_last_scrape(CentralMayorista.name),
        caserita_scrape=controllers.get_last_scrape(LaCaserita.name),
        alvi_scrape=controllers.get_last_scrape(Alvi.name),
        lider_scrape=controllers.get_last_scrape(Lider.name),
        jumbo_scrape=controllers.get_last_scrape(Jumbo.name),
    )


@data_app.route("/<file>", methods=["GET"])
def api_search_result(file):
    return send_from_directory(f"../{INPUT_FOLDER}", file)
