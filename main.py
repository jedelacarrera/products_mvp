import os
import uuid
import time
from flask import Flask, jsonify, request, redirect, render_template, redirect, url_for, send_from_directory
from threading import Thread

from constants import CentralMayorista, LaCaserita, Alvi, Walmart

app = Flask(__name__)

import api_controllers

INPUT_FOLDER = 'tmp/'


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('products'))

# GET and POST models

@app.route('/products/', methods=['GET'])
def products():
    search = request.args.get('search', '')
    products = api_controllers.get_products(search=search)
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify(products)

    return render_template('products.html', search=search, categories=products['categories'])

@app.route('/products/<pid>/', methods=['GET'])
def product(pid):
    result = api_controllers.get_offers_by_product(pid)
    return render_template('product.html', product=result['product'], offers=result['offers'], similar_products=result['similar_products'])

@app.route('/data/', methods=['GET', 'POST'])
def update_data():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            return abort(400)
        filename = INPUT_FOLDER + str(time.time()) + '_' + file.filename
        file.save(filename)
        thread = Thread(target=api_controllers.update_data, args=(filename,))
        thread.start()
        # if error:
            # return redirect(url_for('update_data', error=error))
        return redirect(url_for('update_data', ok='Actualición iniciada correctamente'))

    success = request.args.get('ok')
    error = request.args.get('error')
    files = sorted([file for file in os.listdir('tmp') if '.csv' in file])
    last_scrape_mayorista = api_controllers.get_last_scrape(CentralMayorista.name)
    last_scrape_caserita = api_controllers.get_last_scrape(LaCaserita.name)
    last_scrape_alvi = api_controllers.get_last_scrape(Alvi.name)

    return render_template(
        'data.html',
        success=success,
        error=error,
        file=files[-1],
        mayorista_scrape=last_scrape_mayorista,
        caserita_scrape=last_scrape_caserita,
        alvi_scrape=last_scrape_alvi
    )

@app.route('/data/<file>', methods=['GET'])
def api_search_result(file):
    return send_from_directory('tmp', file)

@app.route('/scrapes/<provider>/', methods=['POST'])
def scrape_central_mayorista(provider):
    if provider == CentralMayorista.url_name:
        element = api_controllers.new_scrape(CentralMayorista.name)
        thread = Thread(target=api_controllers.scrape, args=(provider, element))
    elif provider == LaCaserita.url_name:
        element = api_controllers.new_scrape(LaCaserita.name)
        thread = Thread(target=api_controllers.scrape, args=(provider, element))
    elif provider == Alvi.url_name:
        element = api_controllers.new_scrape(Alvi.name)
        thread = Thread(target=api_controllers.scrape, args=(provider, element))
    else:
        return redirect(url_for('update_data', ok=f'Error, proveedor no existe'))
    thread.start()
    return redirect(url_for('update_data', ok=f'Proceso iniciado correctamente ({provider})'))

@app.route('/scrapes/<provider>/<file>', methods=['GET'])
def scrape_central_mayorista_file(provider, file):
    if not os.path.isfile(f'./tmp/scrapes/{provider}/' + file):
        return redirect(url_for('update_data', error='Se eliminó el archivo, deberías haberlo guardado. Puedes obtener la información nuevamente'))
    return send_from_directory(f'tmp/scrapes/{provider}/', file)

@app.template_filter()
def format_price(price):
    """1000 -> $1.000"""
    return '$' + format(price, ',d').replace(',', '.')