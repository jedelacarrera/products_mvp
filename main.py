import os
import uuid
from flask import Flask, jsonify, request, redirect, render_template, redirect, url_for

app = Flask(__name__)

import api_controllers


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('products'))

# GET and POST models

@app.route('/products/', methods=['GET'])
def products():
    products = api_controllers.get_products(search=request.args.get('search'))
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify(products)

    return render_template('products.html', products=products['products'])

@app.route('/products/<pid>/', methods=['GET'])
def product(pid):
    result = api_controllers.get_offers_by_product(pid)
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify(result)
    return render_template('product.html', product=result['product'], offers=result['offers'])
