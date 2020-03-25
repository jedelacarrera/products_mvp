from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
from .lider_urls import LIDER_URLS


class LiderScraper(BaseScraper):
    base_url = 'https://www.lider.cl'

    def __init__(self, destination_folder='tmp/scrapes/lider/'):
        if destination_folder[-1] != '/':
            destination_folder += '/'
        self.destination_folder = destination_folder

        self.products = []
        self.codes = set()
        self.products_per_page = 1000
        self.aprox_total_products = 10000
        self.total_pages = self.aprox_total_products // self.products_per_page

    def scrape_original(self):  # Not possible to get categories
        common_url = 'https://www.lider.cl/supermercado/category/?No={0}&isNavRequest=Yes&Nrpp={1}&page={2}'
        urls = []
        for i in range(self.total_pages):
            url = common_url.format(self.products_per_page*i, self.products_per_page, i+1)
            response = requests.get(url)
            self.scrap_source(response.content)
            print(url, '. Products: ', len(self.products))

        return self.save_products()

    def scrape(self):  # By categories, if lider changes or adds categories, it will fail
        for lider_url in LIDER_URLS:
            response = requests.get(lider_url.url)
            self.scrap_source(response.content, lider_url)
            print(lider_url, 'Products: ', len(self.products))

        return self.save_products()

    def scrap_source(self, content, lider_url):
        soup = BeautifulSoup(content, 'html.parser')
        products_section = soup.find('div', id='content-prod-boxes')
        if products_section is None:
            print('No products in', lider_url)
            return

        for product in products_section.find_all('div', class_='box-product'):
            try:
                self.add_product(product, lider_url)
            except Exception as e:
                print(e)
                print(product.prettify())

    def add_product(self, item, lider_url):
        condition, sale_price = '', ''

        # gtmProductClick('Pack 12 Shampoo Head &amp; Shoulders Purificación Capilar Carbón Activado','BNDLSKU_20000087','Exclusivo Internet','Especial Packs','CLP','/supermercado/product/Exclusivo-Internet-Pack-12-Shampoo-Head-Shoulders-Purificación-Capilar-Carbón-Activado/BNDLSKU_20000087','-1')
        info = item.find('a', class_='product-link').get('onclick')[17:-2].replace("','", '___').split('___')
        name, code, brand, _, _, url, _ = info

        if code in self.codes:
            print(f'Repeated code: {code}, {lider_url}')
            return

        if brand == 'Exclusivo Internet':
            brand = ''
            condition += 'Exclusivo Internet. '
        url = self.base_url + url

        image_url = item.find('img', class_="img-responsive").get('src').strip()

        prices_container = item.find('div', class_='product-price')
        normal_price = prices_container.find('span', class_='price-sell').text
        price_unit = prices_container.find('span', class_='product-attribute').text

        sale_container =  prices_container.find('span', class_='price-internet')
        if sale_container:
            sale_price = normal_price
            normal_price = sale_container.find('b').text
            if 'Exclusivo Internet' not in condition:
                condition += 'Exclusivo Internet. '

        # <span class="label-icon label-llevamas_fondo">3 X$10.500<b>Ahorro:$3.870</b></span>
        sale_container = item.find('span', class_='label-icon label-llevamas_fondo')
        if sale_container:
            sale_info = sale_container.find(text=True, recursive=False)
            minimium, total_price = map(int, sale_info.replace('.', '').split(' X$'))
            sale_price = int(total_price // minimium)
            condition += f'Oferta: Mínimo {minimium}'

        product = Product(name, brand, normal_price, sale_price, price_unit, image_url, code, condition, item.text, url, lider_url)
        self.products.append(product)
        self.codes.add(code)

    def save_products(self):
        now = datetime.now()
        date = now.strftime('%Y_%m_%d_%H_%M_%S')
        filename = date + '.csv'
        with open(self.destination_folder + filename, 'w') as file:
            file.write('Código;Marca;Descripción;Proveedor;Fuente;Peso;Descripción Completa;Categoría;Subcategoría;Observación;Normal;Oferta;URL Foto Producto\n')
            for product in self.products:
                file.write(str(product))
        return filename


class Product():
    def __init__(self, name, brand, price, sale_price, price_unit, image_url, code, condition='', all_info='', url='', lider_url=None):
        super(Product, self).__init__()
        self.name = name
        self.brand = brand
        self.price = price.split(',')[0] if type(price) == str else int(price//1)
        self.sale_price = sale_price.split(',')[0] if type(sale_price) == str else int(sale_price//1)
        self.price_unit = price_unit
        self.image_url = image_url
        self.code = code
        self.condition = condition
        self.all_info = ''
        self.url = url
        self.category = lider_url.category
        self.subcategory = lider_url.subcategory

    def __str__(self):
        return f'{self.code};{self.brand};{self.name};Lider;{self.url};{self.price_unit};;{self.category};{self.subcategory};{self.condition};{self.price};{self.sale_price};{self.image_url};{self.all_info}\n'


if __name__ == '__main__':
    scraper = LiderScraper()
    scraper.scrape()
    # scraper.finish_session()
