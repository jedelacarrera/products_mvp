import os
import uuid
import time
from flask import Flask, jsonify, request, redirect, render_template, redirect, url_for, send_from_directory
from threading import Thread

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
    last_scrape_mayorista = api_controllers.get_last_scrape('Central Mayorista')
    last_scrape_caserita = api_controllers.get_last_scrape('La Caserita')
    return render_template('data.html', success=success, error=error, file=files[-1], mayorista_scrape=last_scrape_mayorista, caserita_scrape=last_scrape_caserita)

@app.route('/data/<file>', methods=['GET'])
def api_search_result(file):
    return send_from_directory('tmp', file)

@app.route('/scrapes/central_mayorista/', methods=['POST'])
def scrape_central_mayorista():
    element = api_controllers.new_scrape('Central Mayorista')
    thread = Thread(target=api_controllers.scrape_central_mayorista, args=(element,))
    thread.start()
    return redirect(url_for('update_data', ok='Proceso iniciado correctamente (Central Mayorista)'))

@app.route('/scrapes/la_caserita/', methods=['POST'])
def scrape_la_caserita():
    element = api_controllers.new_scrape('La Caserita')
    thread = Thread(target=api_controllers.scrape_la_caserita, args=(element,))
    thread.start()
    return redirect(url_for('update_data', ok='Proceso iniciado correctamente (La Caserita)'))

@app.route('/scrapes/central_mayorista/<file>', methods=['GET'])
def scrape_central_mayorista_file(file):
    if not os.path.isfile('./tmp/scrapes/central_mayorista/' + file):
        return redirect(url_for('update_data', error='Se eliminó el archivo, deberías haberlo guardado. Puedes obtener la información nuevamente'))
    return send_from_directory('tmp/scrapes/central_mayorista/', file)

@app.route('/scrapes/la_caserita/<file>', methods=['GET'])
def scrape_la_caserita_file(file):
    if not os.path.isfile('./tmp/scrapes/la_caserita/' + file):
        return redirect(url_for('update_data', error='Se eliminó el archivo, deberías haberlo guardado. Puedes obtener la información nuevamente'))
    return send_from_directory('tmp/scrapes/la_caserita/', file)

@app.template_filter()
def format_price(price):
    """1000 -> $1.000"""
    return '$' + format(price, ',d').replace(',', '.')