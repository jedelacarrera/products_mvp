from flask import abort
from sqlalchemy import or_
from src.models import Product, Provider


def get_products(search="", provider_id=0):
    query = Product.query
    if search:
        query = query.filter(
            or_(
                Product.description.ilike("%" + search + "%"),
                Product.brand.ilike("%" + search + "%"),
            )
        )
    products = (
        query.order_by(Product.subcategory, Product.description).limit(1000).all()
    )
    products = list(filter(lambda prod: prod.best_price() is not None, products))
    if provider_id:
        products_dicts = [prod.dict_by_provider_id(provider_id) for prod in products]
        products_dicts = list(filter(lambda prod: prod is not None, products_dicts))
    else:
        products_dicts = [prod.dict for prod in products]

    categories = {}
    for product in products_dicts:
        if categories.get(product["subcategory"].lower()):
            categories.get(product["subcategory"].lower()).append(product)
        else:
            categories[product["subcategory"].lower()] = [product]
    return {"categories": categories}


def get_providers():
    return Provider.query.all()


def get_offers_by_product(pid):
    product = Product.query.filter_by(id=pid).first()
    if product is None:
        return abort(404)
    return {
        "offers": [offer.dict for offer in product.offers],
        "product": product.dict,
        "similar_products": [prod.dict for prod in product.similar_products],
    }
