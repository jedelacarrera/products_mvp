import os
import uuid
from flask import Flask, jsonify, request, redirect, render_template, redirect, url_for, send_from_directory

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
        return redirect(url_for('update_data', ok=True))

    success = request.args.get('ok') is not None
    error = request.args.get('error')
    return render_template('data.html', success=success, error=error, file=sorted(os.listdir('tmp'))[-1])

@app.route('/data/<file>', methods=['GET'])
def api_search_result(file):
    return send_from_directory('tmp', file)


@app.template_filter()
def format_price(price):
    """1000 -> $1.000"""
    return '$' + format(price, ',d').replace(',', '.')