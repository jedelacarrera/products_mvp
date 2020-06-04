from flask import abort
from src.models import Product
from sqlalchemy import or_


def get_products(search=""):
    if search:
        products = (
            Product.query.filter(
                or_(
                    Product.description.ilike("%" + search + "%"),
                    Product.brand.ilike("%" + search + "%"),
                )
            )
            .order_by(Product.subcategory, Product.description)
            .limit(1000)
            .all()
        )
    else:
        products = (
            Product.query.order_by(Product.subcategory, Product.description)
            .limit(1000)
            .all()
        )
    products = list(
        filter(
            lambda product: len(product.offers) > 0 and product.best_price != None,
            products,
        )
    )
    categories = {}
    for product in products:
        if categories.get(product.subcategory.lower()):
            categories.get(product.subcategory.lower()).append(product.dict)
        else:
            categories[product.subcategory.lower()] = [product.dict]
    return {"categories": categories}


def get_offers_by_product(pid):
    product = Product.query.filter_by(id=pid).first()
    if product is None:
        return abort(404)
    return {
        "offers": [offer.dict for offer in product.offers],
        "product": product.dict,
        "similar_products": [prod.dict for prod in product.similar_products],
    }
