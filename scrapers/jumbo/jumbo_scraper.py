import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# from scrapers.base_scraper import BaseScraper
from jumbo_categories import JUMBO_CATEGORIES, REPLACE_STRINGS


class JumboScraper:
    base_url = "https://www.jumbo.cl/"

    def __init__(self, destination_folder="tmp/scrapes/jumbo/"):
        if destination_folder[-1] != "/":
            destination_folder += "/"
        self.destination_folder = destination_folder

        self.products = []
        self.codes = set()

    def scrape(self):
        for category in JUMBO_CATEGORIES:
            product_count = 40
            page = 1
            while product_count == 40:
                url = self.base_url + category + "?page=" + str(page)
                response = requests.get(url)
                products = self._get_products_from_response(response)
                product_count = len(products)
                self._add_products(products)
                print(url, len(self.products))
                page += 1

        return self._save_products()

    def _add_products(self, products):
        for product_dict in products:
            product = Product(product_dict)
            if product.code in self.codes:
                return

            self.products.append(product)
            self.codes.add(product.code)

    def _save_products(self):
        now = datetime.now()
        date = now.strftime("%Y_%m_%d_%H_%M_%S")
        filename = date + ".csv"
        with open(self.destination_folder + filename, "w") as file:
            file.write(
                "Código;Marca;Descripción;Proveedor;Fuente;Peso;Descripción Completa;Categoría;Subcategoría;Observación;Normal;Oferta;URL Foto Producto\n"
            )
            for product in self.products:
                file.write(str(product))
        return filename

    @staticmethod
    def _get_products_from_response(response):
        content = response.content.decode("utf-8")
        initial_string = '<script> window.__renderData = "'
        content = content[content.find(initial_string) + len(initial_string) :]
        content = content[: content.find('";</script>')]

        for before, after in REPLACE_STRINGS:
            content = content.replace(before, after)

        return json.loads(content)["plp"]["plp_products"]["data"]


class Product:
    def __init__(self, product_dict):
        self.code = 3
        print(product_dict)

    def __str__(self):
        return "product"


if __name__ == "__main__":
    scraper = JumboScraper()
    scraper.scrape()
