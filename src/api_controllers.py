# pylint: disable=no-member
import os
from datetime import datetime
from flask import abort
from scrapers import (
    CentralMayoristaScraper,
    LaCaseritaScraper,
    AlviScraper,
    LiderScraper,
    JumboScraper,
)
from src.models import Product, Offer, Provider, Scrape, db
from src.constants import CentralMayorista, LaCaserita, Alvi, Lider, Jumbo
from sqlalchemy import or_

# GET controllers


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
            .limit(2000)
            .all()
        )
    else:
        products = (
            Product.query.order_by(Product.subcategory, Product.description)
            .limit(2000)
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


def get_providers():
    return {"providers": [provider.dict for provider in Provider.query.all()]}


def get_product_from_line(line):
    # Código, Marca, Descripción, Proveedor, Fuente, Peso, Descripción Completa, Categoría, Subcategoría, Observación, Precio Normal, Precio Oferta, URL Foto Producto.
    splitted_line = line.split(";")
    product = Product.query.filter_by(code=splitted_line[0]).first()
    if product:
        return product

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
    # db.session.commit()
    return product


def create_offer(line):
    product = get_product_from_line(line)

    splitted_line = line.split(";")
    provider = Provider.query.filter_by(name=splitted_line[3].strip()).first()
    if not provider:
        raise Exception(f'Provider "{splitted_line[3]}" does not exist')

    product.offers.append(
        Offer(
            # product_id=product_id,
            provider_id=provider.id,
            source=splitted_line[4] or None,
            comment=splitted_line[9] or None,
            price=splitted_line[10].replace("$", "").replace(".", "") or None,
            sale_price=splitted_line[11].replace("$", "").replace(".", "") or None,
        )
    )


def handle_file(filename):
    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        file.readline()
        for index, line in enumerate(file.readlines()):
            try:
                create_offer(line)
            except Exception as error:
                # raise error
                return f"Line {index + 2}: {str(error)}"

    db.session.commit()


def update_data(filename):
    offers = Offer.query.all()
    products = Product.query.all()
    for obj in offers + products:
        db.session.delete(obj)
    db.session.commit()

    result = handle_file(filename)
    print("File handled")
    print(result)
    return result


def get_last_scrape(provider_name):
    provider = Provider.query.filter_by(name=provider_name).first()
    return (
        Scrape.query.order_by(Scrape.id.desc())
        .filter_by(provider_id=provider.id)
        .first()
    )


def new_scrape(provider_name):
    provider = Provider.query.filter_by(name=provider_name).first()
    element = Scrape(status="STARTED", provider_id=provider.id)
    db.session.add(element)
    db.session.commit()
    return element


def scrape(provider, element_id):
    if provider == CentralMayorista.url_name:
        scraper = CentralMayoristaScraper()
    elif provider == LaCaserita.url_name:
        scraper = LaCaseritaScraper()
    elif provider == Alvi.url_name:
        scraper = AlviScraper()
    elif provider == Lider.url_name:
        scraper = LiderScraper()
    elif provider == Jumbo.url_name:
        scraper = JumboScraper()
    else:
        raise Exception("Proveedor no disponible")

    element = Scrape.query.get(element_id)
    try:
        filename = scraper.scrape()
        scraper.finish_session()

        element.filename = filename
        element.status = "SUCCESS"
    except Exception as e:
        element.status = "ERROR: " + str(e)

    element.updated_at = str(datetime.now())
    db.session.add(element)
    db.session.commit()
