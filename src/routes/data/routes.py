import os
import time
from threading import Thread
from flask import Blueprint, request, render_template

data_app = Blueprint("data", __name__, url_prefix="/data")

INPUT_FOLDER = "tmp"


@data_app.route("/", methods=["GET", "POST"])
def update_data():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return abort(400)
        filename = f"{INPUT_FOLDER}/{time.time()}_{file.filename}
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


@data_app.route("/<file>", methods=["GET"])
def api_search_result(file):
    return send_from_directory(INPUT_FOLDER, file)
