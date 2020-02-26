import os
import uuid
from flask import Flask, jsonify, request, redirect, render_template, redirect, url_for, send_from_directory
from threading import Thread

app = Flask(__name__)

import api_controllers


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
        error = api_controllers.update_data(request)
        if error:
            return redirect(url_for('update_data', error=error))
        return redirect(url_for('update_data', ok='Actualizado correctamente'))

    success = request.args.get('ok')
    error = request.args.get('error')
    files = sorted([file for file in os.listdir('tmp') if '.csv' in file])
    last_scrape = api_controllers.get_central_mayorista_last_scrape()
    return render_template('data.html', success=success, error=error, file=files[-1], scrape=last_scrape)

@app.route('/data/<file>', methods=['GET'])
def api_search_result(file):
    return send_from_directory('tmp', file)

@app.route('/scrapes/central_mayorista/', methods=['POST'])
def scrape():
    element = api_controllers.new_scrape()
    thread = Thread(target=api_controllers.scrape_central_mayorista, args=(element,))
    thread.start()
    return redirect(url_for('update_data', ok='Proceso iniciado correctamente'))

@app.route('/scrapes/central_mayorista/<file>', methods=['GET'])
def scrape_file(file):
    if not os.path.isfile('./tmp/scrapes/central_mayorista/' + file):
        return redirect(url_for('update_data', error='Se eliminó el archivo, deberías haberlo guardado. Puedes obtener la información nuevamente'))
    return send_from_directory('tmp/scrapes/central_mayorista/', file)


@app.template_filter()
def format_price(price):
    """1000 -> $1.000"""
    return '$' + format(price, ',d').replace(',', '.')