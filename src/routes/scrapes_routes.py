import os
from threading import Thread
from flask import Blueprint
from src.constants import INPUT_FOLDER

scrapes_app = Blueprint("scrapes", __name__, url_prefix="/scrapes")


@scrapes_app.route("/<provider>/", methods=["POST"])
def scrape(provider):
    element = api_controllers.new_scrape(TRANSLATIONS[provider])
    thread = Thread(target=api_controllers.scrape, args=(provider, element.id))
    thread.start()
    return redirect(
        url_for("update_data", ok=f"Proceso iniciado correctamente ({provider})")
    )


@scrapes_app.route("/<provider>/<file>", methods=["GET"])
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
