from models import Product, Offer, Provider, CentralMayoristaScrape, db
from datetime import datetime
import os
from flask import abort
import time
from scrapers.central_mayorista_scraper import CentralMayoristaScraper

INPUT_FOLDER = 'tmp/'
# GET controllers

def get_products(search=''):
    products = Product.query.filter(Product.description.ilike('%' + search + '%')).order_by(Product.category, Product.description).all()
    products = list(filter(lambda product: len(product.offers) > 0 and product.best_price != None, products))
    categories = {}
    for product in products:
        if categories.get(product.category.lower()):
            categories.get(product.category.lower()).append(product.dict)
        else:
            categories[product.category.lower()] = [product.dict]
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
    provider = Provider.query.filter_by(name=splitted_line[3].strip()).first()
    if not provider:
        raise Exception(f'Provider "{splitted_line[3]}" does not exist')

    offer = Offer(
        product_id=product_id,
        provider_id=provider.id,
        source=splitted_line[4] or None,
        comment=splitted_line[9] or None,
        price=splitted_line[10].replace('$', '').replace('.', '') or None,
        sale_price=splitted_line[11].replace('$', '').replace('.', '') or None,
    )

    db.session.add(offer)
    db.session.commit()

def handle_file(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        file.readline()
        for index, line in enumerate(file.readlines()):
            try:
                product_id = create_offer(line)
            except Exception as error:
                return f'Line {index + 2}: {str(error)}'

def update_data(request):
    file = request.files.get('file')

    if not file:
        return abort(400)

    filename = INPUT_FOLDER + str(time.time()) + '_' + file.filename
    file.save(filename)

    offers = Offer.query.all()
    products = Product.query.all()
    for obj in offers + products:
        db.session.delete(obj)
    db.session.commit()

    return handle_file(filename)

def get_central_mayorista_last_scrape():
    return CentralMayoristaScrape.query.order_by(CentralMayoristaScrape.id.desc()).first()

def new_scrape():
    element = CentralMayoristaScrape(status='STARTED')
    db.session.add(element)
    db.session.commit()
    return element

def scrape_central_mayorista(element):
    scraper = CentralMayoristaScraper()
    try:
        filename = scraper.scrape()
        scraper.finish_session()

        element.filename = filename
        element.status = 'SUCCESS'
    except Exception as e:
        element.status = 'ERROR: ' + str(e)

    element.updated_at = str(datetime.now())
    db.session.add(element)
    db.session.commit()