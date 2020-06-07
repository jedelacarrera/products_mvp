class BaseScraper:
    # pylint: disable=no-self-use
    def scrape(self):
        raise Exception("Not implemented")

    def finish_session(self):
        return
