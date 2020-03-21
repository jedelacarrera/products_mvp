import time
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class LiderCategory:
    base_url = 'https://www.lider.cl/supermercado/category/'
    products_per_page = 100

    def __init__(self, id, name, subname):
        self.id = id
        self.name = name
        self.pagessubname = subname

    @property
    def urls(self):
        url = f'{self.base_url}{self.name}/id/{self.id}/?product_list_limit=36&p='
        return [url + str(page+1) for page in range(self.pages)]
    

class LiderScraper(BaseScraper):
    categories = [
        LiderCategory(3, 'limpieza', 7),
        LiderCategory(4, 'cuidado-personal', 6),
        LiderCategory(5, 'despensa', 8),
        LiderCategory(6, 'lacteos-y-frambres', 4),
        LiderCategory(8, 'frescos-y-congelados', 3),  # Por si acaso, queda muy justo con 2
        LiderCategory(9, 'bebidas-y-licores', 3),
        LiderCategory(10, 'confites-y-cocktail', 1),
        LiderCategory(11, 'bazar', 1),
    ]

    cookies = {
        'setea_comuna': '43',
        'setea_entrega': 'true',
        'setea_region': '13',
        'setea_tipo_entrega': '1',
        'store': '8000-26-1',
    }

    base_url = 'https://www.lider.cl'

    def __init__(self, destination_folder='tmp/scrapes/lider/'):
        if destination_folder[-1] != '/':
            destination_folder += '/'
        self.destination_folder = destination_folder

        self.products = []
        self.codes = set()

    @property
    def urls(self):
        urls = []
        for category in self.categories:
            urls += category.urls
        return urls

    def scrape(self):
        response = requests.get('https://www.lider.cl/supermercado/category/?No=400&isNavRequest=Yes&Nrpp=400&page=2')
        soup = BeautifulSoup(response.content, 'html.parser')
        with open('fileeeee.html', 'w') as file:
            file.write(soup.prettify())
        self.scrap_source(response.content)
        return self.save_products()
        # responses = [requests.get(url, cookies=self.cookies) for url in self.urls]
        # category_names = []
        # for category in self.categories:
        #     for i in range(category.pages):
        #         category_names.append(category.name + '_' + str(i+1))
        # for response, category_name in zip(responses, category_names):
        #     self.scrap_source(response.content, category_name)

    def scrap_source(self, content, category_name='Sin categoría'):
        soup = BeautifulSoup(content, 'html.parser')
        products_section = soup.find('div', id='content-prod-boxes')
        if products_section is None:
            print(soup)
            return

        for product in products_section.find_all('div', class_='box-product'):
            try:
                self.add_product(product, category_name)
            except Exception as e:
                print(e)
                print(product.prettify())

    def add_product(self, item, category_name):
        condition, sale_price = '', ''

        # gtmProductClick('Pack 12 Shampoo Head &amp; Shoulders Purificación Capilar Carbón Activado','BNDLSKU_20000087','Exclusivo Internet','Especial Packs','CLP','/supermercado/product/Exclusivo-Internet-Pack-12-Shampoo-Head-Shoulders-Purificación-Capilar-Carbón-Activado/BNDLSKU_20000087','-1')
        info = item.find('a', class_='product-link').get('onclick')[17:-2].replace("','", '___').split('___')
        name, code, brand, category, _, url, _ = info

        if code in self.codes:
            print(f'Repeated code: {code}, {category_name}')
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

        product = Product(name, brand, normal_price, sale_price, price_unit, image_url, code, condition, item.text, url, category)
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
    def __init__(self, name, brand, price, sale_price, price_unit, image_url, code, condition='', all_info='', url='', category='La Caserita'):
        super(Product, self).__init__()
        self.name = name
        self.brand = brand
        self.price = price
        self.sale_price = sale_price
        self.price_unit = price_unit
        self.image_url = image_url
        self.code = code
        self.condition = condition
        self.all_info = ''
        self.url = url
        self.category = category

    def __str__(self):
        return f'{self.code};{self.brand};{self.name};Lider;{self.url};{self.price_unit};;{self.category};;{self.condition};{self.price};{self.sale_price};{self.image_url};{self.all_info}\n'


if __name__ == '__main__':
    scraper = LiderScraper()
    scraper.scrape()
    # scraper.finish_session()
