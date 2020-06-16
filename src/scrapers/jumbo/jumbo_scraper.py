# coding=utf-8
import json
from datetime import datetime
import requests

from src.scrapers.base_scraper import BaseScraper
from src.scrapers.jumbo.jumbo_categories import JUMBO_CATEGORIES, REPLACE_STRINGS


class JumboScraper(BaseScraper):
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
                print(f"{url:60} prods: {len(self.products)}")
                page += 1

        return self._save_products()

    def _add_products(self, products):
        for product_dict in products:
            product = JumboProduct(product_dict)
            if product.code in self.codes:
                print(f"Product {product.code} ({product.name}) was already found")
                continue
            if not product.available:
                continue

            self.products.append(product)
            self.codes.add(product.code)

    def _save_products(self):
        now = datetime.now()
        date = now.strftime("%Y_%m_%d_%H_%M_%S")
        filename = date + ".csv"
        with open(self.destination_folder + filename, "w") as file:
            file.write(
                "Código;Marca;Descripción;Proveedor;Fuente;Peso;Descripción Completa;Categoría;Subcategoría;Observación;Normal;Oferta;URL Foto Producto\n"  # pylint: disable=line-too-long
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

        try:
            return json.loads(content)["plp"]["plp_products"]["data"]
        except Exception as error:  # pylint: disable=broad-except
            with open("product_error.json", "w") as file:
                file.write(content)
                raise error


class JumboProduct:
    def __init__(self, product_dict):
        item = product_dict["items"][0]
        offer = item["sellers"][0]["commertialOffer"]
        self.available = True
        self.code = product_dict["productId"]
        self.brand = product_dict["brand"]
        self.name = product_dict["productName"]
        self.image_url = item["images"][0]["imageUrl"]
        self.url = product_dict["link"]

        if len(product_dict["items"]) > 1:
            print(f"Product {self.code} ({self.name}) has more than one item")
        if len(item["sellers"]) > 1:
            self.raise_error(product_dict, "more than one product seller")

        try:
            self.category = product_dict["categories"][-1].replace("/", "")
            self.subcategory = product_dict["categories"][0].split("/")[1]
        except:  # pylint: disable=bare-except
            self.raise_error(product_dict, "error with categories")
        self.price_unit = item["measurementUnit"]
        if not offer.get("Price") or not offer.get("PriceWithoutDiscount"):
            print(f"No stock for product {self.name}")
            self.available = False
            return
        if offer["Price"] < offer["PriceWithoutDiscount"]:
            self.sale_price = offer["Price"]
            self.price = offer["PriceWithoutDiscount"]
        else:
            self.price = offer["Price"]
            self.sale_price = ""

        # print(product_dict)

    def raise_error(self, product_dict, error):
        with open("product_error.json", "w") as file:
            json.dump(product_dict, file, ensure_ascii=False, indent=4)
            raise Exception(error)

    def __str__(self):
        return f"{self.code};{self.brand};{self.name};Jumbo;{self.url};{self.price_unit};;{self.category};{self.subcategory};;{self.price};{self.sale_price};{self.image_url}\n"


# if __name__ == "__main__":
#     scraper = JumboScraper()
#     scraper.scrape()
