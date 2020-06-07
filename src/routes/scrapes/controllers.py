# pylint: disable=no-member
from datetime import datetime
from src.scrapers import (
    CentralMayoristaScraper,
    LaCaseritaScraper,
    AlviScraper,
    LiderScraper,
    JumboScraper,
)
from src.models import Provider, Scrape, db
from src.constants import CentralMayorista, LaCaserita, Alvi, Lider, Jumbo


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
