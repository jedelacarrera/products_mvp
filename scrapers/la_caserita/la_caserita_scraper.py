import time
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper

class LaCaseritaCategory:
    base_url = 'https://www.caserita.cl/catalog/category/view/s/'

    def __init__(self, id, name, pages):
        self.id = id
        self.name = name
        self.pages = pages

    @property
    def urls(self):
        url = f'{self.base_url}{self.name}/id/{self.id}/?product_list_limit=36&p='
        return [url + str(page+1) for page in range(self.pages)]
    

class LaCaseritaScraper(BaseScraper):
    categories = [
        LaCaseritaCategory(3, 'limpieza', 7),
        LaCaseritaCategory(4, 'cuidado-personal', 6),
        LaCaseritaCategory(5, 'despensa', 8),
        LaCaseritaCategory(6, 'lacteos-y-frambres', 4),
        LaCaseritaCategory(8, 'frescos-y-congelados', 3),  # Por si acaso, queda muy justo con 2
        LaCaseritaCategory(9, 'bebidas-y-licores', 3),
        LaCaseritaCategory(10, 'confites-y-cocktail', 1),
        LaCaseritaCategory(11, 'bazar', 1),
    ]

    cookies = {
        'setea_comuna': '43',
        'setea_entrega': 'true',
        'setea_region': '13',
        'setea_tipo_entrega': '1',
        'store': '8000-26-1',
    }

    def __init__(self, destination_folder='tmp/scrapes/la_caserita/'):
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
        responses = [requests.get(url, cookies=self.cookies) for url in self.urls]
        category_names = []
        for category in self.categories:
            for i in range(category.pages):
                category_names.append(category.name + '_' + str(i+1))
        for response, category_name in zip(responses, category_names):
            self.scrap_source(response.content, category_name)
        return self.save_products()

    def scrap_source(self, content, category_name):
        soup = BeautifulSoup(content, 'html.parser')
        products_section = soup.find('section', class_='grilla-productos')
        if products_section is None:
            print(soup)
            return

        for product in products_section.find_all(class_='item-producto'):
            try:
                self.add_product(product, category_name)
            except Exception as e:
                print(e)
                print(product.prettify())

    def add_product(self, item, category_name):
        code, image_url, brand, name, condition, sale_price, normal_price, description, price_unit, url = '', '', '', '', '', '', '', '', '', ''
        image = item.find('img', class_="product-image-photo")

        brand = item.find('p', class_="item-productor").text.strip()
        image_url = image.get('src').strip()
        name = image.get('alt').strip()
        url = item.find('a').get('href').strip()
        code = image_url.split('/')[-1].split('_')[0].split('.')[0].strip()
        if not code.isdecimal():
            code = url.split('-')[-2]

        if code in self.codes:
            # raise Exception(f'Repeated code: {code}')
            print(f'Repeated code: {code}, {category_name}')
            return

        price_elements = item.find_all('span', class_='gradiente-number-con-peso')

        # price_elements[0].text == '$'
        normal_price = price_elements[1].text
        price_unit = price_elements[2].text

        sale_price_elements = item.find_all('span', class_='rango-siguiente-plp')
        if len(sale_price_elements) > 0:
            best_sale_price_element = sale_price_elements[-1]
            if '¡Mejor Precio!' in best_sale_price_element.text:
                best_sale_price_element = sale_price_elements[-2]
            sale_text = best_sale_price_element.text.strip(' .').split(' c/u x ')
            sale_price = sale_text[0]
            minimium = sale_text[1].replace('unid', ' unid')
            condition += f'Oferta: Mínimo {minimium}'

        # print(code, ' - ', image_url.split('/')[-1], ' - ', brand, ' - ', name, ' - ', price, ' - ', price_unit, ' - ', condition, ' - ', description)
        product = Product(name, description, brand, normal_price, sale_price, price_unit, image_url, code, condition, item.text, url, category_name)
        self.products.append(product)
        self.codes.add(code)
        # print(product)

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
    url = 'https://www.caserita.cl/'
    def __init__(self, name, description, brand, price, sale_price, price_unit, image_url, code, condition='', all_info='', url='', category='La Caserita'):
        super(Product, self).__init__()
        self.name = name
        self.brand = brand
        self.price = price
        self.sale_price = sale_price
        self.price_unit = price_unit
        self.image_url = image_url
        self.code = code
        self.condition = condition
        self.description = description
        self.all_info = ''
        if url:
            self.url = url
        self.category = category

    def __str__(self):
        return f'{self.code};{self.brand};{self.name};La Caserita;{self.url};{self.price_unit};{self.description};{self.category};;{self.condition};{self.price};{self.sale_price};{self.image_url};{self.all_info}\n'


if __name__ == '__main__':
    scraper = LaCaseritaScraper()
    scraper.scrape()
    # scraper.finish_session()
