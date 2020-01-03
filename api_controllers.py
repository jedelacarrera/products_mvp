from models import Product, Offer, Provider, db
import os
from flask import abort

# GET controllers

def get_products(search=''):
    if search:
        products = Product.query.filter(Product.name.ilike('%' + search + '%'))
    else:
        products = Product.query.all()
    return {"products": [product.dict for product in products]}

def get_offers_by_product(pid):
    product = Product.query.filter_by(id=pid).first()
    if product is None:
        return abort(404)
    return {
        "offers": [offer.dict for offer in product.offers],
        "product": product.dict,
    }

def get_providers():
    return {"providers": [provider.dict for provider in Provider.query.all()]}
