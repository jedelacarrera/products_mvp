import time
from datetime import datetime
import os
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .base_scraper import BaseScraper


class AlviScraper(BaseScraper):
    url = 'https://www.alvi.cl/ofertas'

    def __init__(self, destination_folder='tmp/scrapes/alvi/', url=None):
        if url:
            self.url = url
        if destination_folder[-1] != '/':
            destination_folder += '/'
        self.destination_folder = destination_folder

        self.products = []

        # self.options = Options();
        # self.options.add_experimental_option("prefs", {"safebrowsing.enabled": True})
        # self.options.add_argument('--kiosk-printing')
        # chrome_path = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver'

        # chrome_exec_shim = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")
        # self.selenium = webdriver.Chrome(executable_path=chrome_exec_shim)

        self.options = Options()
        self.options.experimental_options["prefs"] = {
            "profile.default_content_settings": {"images": 2},
            "profile.managed_default_content_settings": {"images": 2}
        }

        if os.environ.get('FLASK_ENV') == 'development':
            CHROMEDRIVER_PATH = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver'

        else:
            self.options.binary_location = os.environ.get('GOOGLE_CHROME_BIN', "chromedriver")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument('--headless')
            self.options.add_argument('window-size=1200x600')
            CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH', "/app/.chromedriver/bin/chromedriver")

        self.browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=self.options)

    def finish_session(self):
        self.browser.close()

    def scrape(self):
        self.browser.set_page_load_timeout(20)
        self.browser.get(self.url)

        time.sleep(1)

        self.scrap_source()
        file = self.save_products()

        return file

    def scrap_source(self):
        html_source = self.browser.page_source
        source = BeautifulSoup(html_source, 'html.parser')

        items = source.find_all('app-offer-item')
        for item in items:
            try:
                self.add_product(item)
            except Exception as e:
                print(e)
                print(item.prettify())
        return

    def add_product(self, item):
        image_url, name, condition, sale_price, normal_price, description, price_unit = '', '', '', '', '', '', ''

        # Get image_url
        img = item.find('img', class_='img-fluid')
        if img is None:
            raise Exception('No image in product')
        image_url = img.get('src')[2:]
        name = item.find('h3').text.strip()
        description = item.find('p').text.strip()

        sale_info = item.find_all('div', class_='sticker-value')[0].find('span').text.strip()
        splitted_sale = sale_info.split('$')
        if len(splitted_sale) != 2:
            description += '. ' + sale_info
            product = Product(name, description, 'No valid price in product', '', '', '', image_url, 'Error en este producto', '', item.text)
            self.products.append(product)
            raise Exception('No valid price in product')

        condition += f'Oferta: Precio Socio, mínimo {splitted_sale[0].strip()}.'
        sale_price = splitted_sale[1].split('c/')[0].strip()
        price_unit = 'c/' + splitted_sale[1].split('c/')[1].strip()

        normal_price_info = item.find('div', class_='card-footer text-center h8').span.text.strip()
        normal_price = normal_price_info.split('$')[1].split('c/')[0].strip()

        product = Product(name, description, '', normal_price, sale_price, price_unit, image_url, '', condition, item.text)
        self.products.append(product)
        return True

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
    ID = 1001

    def __init__(self, name, description, brand, price, sale_price, price_unit, image_url, code, condition='', all_info=''):
        super(Product, self).__init__()
        self.name = name
        self.brand = brand
        self.price = price.replace('$', '').replace('.', '')
        self.sale_price = sale_price.replace('$', '').replace('.', '')
        self.price_unit = price_unit
        self.image_url = 'http://' + image_url
        self.code = code
        if not self.code:
            self.code = self.ID
            Product.ID += 1
        self.condition = condition
        self.description = description
        self.all_info = all_info

    def __str__(self):
        return f'{self.code};{self.brand};{self.name};Alvi;{AlviScraper.url};{self.price_unit};{self.description};Sin Categoría;;{self.condition};{self.price};{self.sale_price};{self.image_url};{self.all_info}\n'


if __name__ == '__main__':
    scraper = AlviScraper()
    scraper.scrape()
    scraper.finish_session()
    for prod in scraper.products:
        print(str(prod))
