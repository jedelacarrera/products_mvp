import time
from datetime import datetime
import os
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapers.base_scraper import BaseScraper


class CentralMayoristaScraper(BaseScraper):
    url = "https://centralmayorista.walmartdigital.cl/"

    def __init__(self, destination_folder="tmp/scrapes/central_mayorista/", url=None):
        if url:
            self.url = url
        if destination_folder[-1] != "/":
            destination_folder += "/"
        self.destination_folder = destination_folder
        self.previous_page_source = None

        self.products = []
        self.codes = set()
        self.page = 1

        # self.options = Options();
        # self.options.add_experimental_option("prefs", {"safebrowsing.enabled": True})
        # self.options.add_argument('--kiosk-printing')
        # chrome_path = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver'

        # chrome_exec_shim = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")
        # self.selenium = webdriver.Chrome(executable_path=chrome_exec_shim)

        self.options = Options()
        self.options.experimental_options["prefs"] = {
            "profile.default_content_settings": {"images": 2},
            "profile.managed_default_content_settings": {"images": 2},
        }

        if os.environ.get("FLASK_ENV") == "development":
            CHROMEDRIVER_PATH = (
                os.path.dirname(os.path.abspath(__file__)) + "/../chromedriver"
            )
            # self.options.add_argument("window-size=1200x600")

        else:
            self.options.binary_location = os.environ.get(
                "GOOGLE_CHROME_BIN", "chromedriver"
            )
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-dev-shm-usage")
            CHROMEDRIVER_PATH = os.environ.get(
                "CHROMEDRIVER_PATH", "/app/.chromedriver/bin/chromedriver"
            )

        self.browser = webdriver.Chrome(
            executable_path=CHROMEDRIVER_PATH, chrome_options=self.options
        )

    def finish_session(self):
        self.browser.close()

    def scrape(self):
        self.browser.set_page_load_timeout(20)
        self.browser.get(self.url)

        time.sleep(1)
        while True:
            time.sleep(1)
            status = self.scrap_source()
            print("Products: ", len(self.products), ". Page: ", self.page)
            if not status:
                break
            next_page_button = self.browser.find_element_by_xpath(
                "(//span[@class='ais-Pagination-link'])[2]"
            )
            next_page_button.click()
            self.page += 1
        file = self.save_products()
        return file

    def scrap_source(self):
        html_source = self.browser.page_source
        source = BeautifulSoup(html_source, "html.parser")

        items = source.find_all("li", class_="ais-Hits-item")
        for item in items:
            try:
                if not self.add_product(item) and self.page > 210:
                    return False
            except Exception as e:
                print(e)
                print(item.prettify())
        return True

    def add_product(self, item):
        (
            code,
            image_url,
            brand,
            name,
            condition,
            sale_price,
            normal_price,
            description,
            price_unit,
        ) = ("", "", "", "", "", "", "", "", "")
        code = item.find("div", class_="campaign-label")
        if code is None:
            raise Exception("No code in product")
        code = code.text.strip()
        code = code.strip("Item: ")

        if code in self.codes:
            print("Finishing, code already found: ", code)
            return False

        # Get image_url
        img = item.find("img", class_="img-fluid m-auto")
        if img is None:
            raise Exception("No image in product")
        image_url = img.get("src")

        # Get name and brand
        description = item.find("div", class_="product-description")
        span_items = description.find_all("span")
        if len(span_items) != 2:
            raise Exception("No name or brand in product")
        brand = span_items[0].text.strip()
        name = span_items[1].text.strip()

        # Get offer attributes: prices and conditions
        price_elements = item.find_all("span", class_="price-tag") + item.find_all(
            "span", class_="last-price-tag"
        )
        price_blocks = item.find_all("span", class_="price-block") + item.find_all(
            "span", class_="last-price-block"
        )
        if len(price_elements) == 1 and "x $" in price_elements[0].text:
            units, total_price = map(int, price_elements[0].text.split(" x $"))
            sale_price = "$" + str(int((total_price / units) // 1))
            condition += f"Oferta: Packs de {units} unidades. "

            normal_price_info = price_elements[0].next_sibling
            price_unit = normal_price_info.find(text=True, recursive=False)
            normal_price = normal_price_info.find("strong").text.strip()
        elif len(price_elements) < 2:
            raise Exception("No price in product")
        else:
            normal_price = price_elements[0].text.strip()
            price_unit = price_elements[1].text.strip()

        if len(price_elements) > 2:
            sale_price = price_elements[-2].text.strip()
            condition += "Oferta: " + price_blocks[-1].text.strip() + "."

        minimin_to_buy = item.find("div", class_="text-center minimum-to-buy")
        internet_condition = item.find("span", class_="internet-exclusive-text")
        if minimin_to_buy:
            condition += minimin_to_buy.text.strip() + ". "
        if internet_condition:
            condition += internet_condition.text.strip() + ". "

        # Get product description
        description = item.find_all("div", class_="mb-15")[-1].text.strip()

        # print(code, ' - ', image_url.split('/')[-1], ' - ', brand, ' - ', name, ' - ', price, ' - ', price_unit, ' - ', condition, ' - ', description)
        product = Product(
            name,
            description,
            brand,
            normal_price,
            sale_price,
            price_unit,
            image_url,
            code,
            condition,
            item.text,
        )
        self.products.append(product)
        self.codes.add(code)
        return True

    def save_products(self):
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


class Product:
    def __init__(
        self,
        name,
        description,
        brand,
        price,
        sale_price,
        price_unit,
        image_url,
        code,
        condition="",
        all_info="",
    ):
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
        self.all_info = all_info

    def __str__(self):
        return f"{self.code};{self.brand};{self.name};Central Mayorista;{CentralMayoristaScraper.url};{self.price_unit};{self.description};Sin Categoría;;{self.condition};{self.price};{self.sale_price};{self.image_url};{self.all_info}\n"


if __name__ == "__main__":
    scraper = CentralMayoristaScraper()
    # scraper.scrape()
    # scraper.finish_session()
