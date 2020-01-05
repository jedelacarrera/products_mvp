from models import Product, Offer, Provider, db
import os
from flask import abort
import time

INPUT_FOLDER = 'tmp/'
# GET controllers

def get_products(search=''):
    products = Product.query.filter(Product.description.ilike('%' + search + '%')).order_by(Product.category, Product.description).all()
    products = list(filter(lambda product: len(product.offers) > 0 and product.best_price != None, products))
    categories = {}
    for product in products:
        if categories.get(product.category):
            categories.get(product.category).append(product)
        else:
            categories[product.category] = [product.dict]
    print(categories['Salsas'])
    return {"categories": categories}

def get_offers_by_product(pid):
    product = Product.query.filter_by(id=pid).first()
    if product is None:
        return abort(404)
    return {
        "offers": [offer.dict for offer in product.offers],
        "product": product.dict,
        "similar_products": [prod.dict for prod in product.similar_products]
    }

def get_providers():
    return {"providers": [provider.dict for provider in Provider.query.all()]}

def get_product_id(line):
    # Código, Marca, Descripción, Proveedor, Fuente, Peso, Descripción Completa, Categoría, Subcategoría, Observación, Precio Normal, Precio Oferta, URL Foto Producto.
    splitted_line = line.split(';')
    product = Product.query.filter_by(code=splitted_line[0]).first()
    if product:
        return product.id

    product = Product(
        code=splitted_line[0],
        brand=splitted_line[1],
        description=splitted_line[2],
        # Skip 3, 4
        quantity=splitted_line[5],
        complete_description=splitted_line[6],
        category=splitted_line[7],
        subcategory=splitted_line[8],
        # Skip 9, 10, 11
        url=splitted_line[12],
    )
    db.session.add(product)
    db.session.commit()
    return product.id

def create_offer(line):
    product_id = get_product_id(line)

    splitted_line = line.split(';')
    provider_id = Provider.query.filter_by(name=splitted_line[3]).first().id,

    offer = Offer(
        product_id=product_id,
        provider_id=provider_id,
        source=splitted_line[4] or None,
        comment=splitted_line[9] or None,
        price=splitted_line[10].replace('$', '') or None,
        sale_price=splitted_line[11].replace('$', '') or None,
    )

    db.session.add(offer)
    db.session.commit()

def handle_file(filename):
    with open(filename, 'r') as file:
        file.readline()
        try:
            for line in file.readlines():
                product_id = create_offer(line)
        except Exception as error:
            return str(error)


def update_data(request):
    file = request.files.get('file')

    if not file:
        return abort(400)

    filename = INPUT_FOLDER + str(time.time()) + '_' + file.filename
    file.save(filename)

    offers = Offer.query.all()
    for offer in offers:
        db.session.delete(offer)
    db.session.commit()

    return handle_file(filename)
