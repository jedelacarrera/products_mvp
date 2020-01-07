from dbconfig import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(120), unique=False, nullable=True)
    brand = db.Column(db.String(120), unique=False, nullable=True)
    description = db.Column(db.String(120), unique=False, nullable=True)
    complete_description = db.Column(db.String(120), unique=False, nullable=True)
    quantity = db.Column(db.String(120), unique=False, nullable=True)
    category = db.Column(db.String(120), unique=False, nullable=True)
    subcategory = db.Column(db.String(120), unique=False, nullable=True)
    url = db.Column(db.Text, unique=False, nullable=True)

    offers = db.relationship('Offer', backref='product', lazy=True, cascade = "all,delete")

    MAX_PRICE = 1000000000

    @property
    def best_price(self):
        best = Product.MAX_PRICE
        prices = []
        providers = []
        for offer in self.offers:
            if offer.price:
                prices.append(offer.price)
                providers.append(offer.provider)
            if offer.sale_price:
                prices.append(offer.sale_price)
                providers.append(offer.provider)
        if len(prices) == 0:
            return None

        best = min(prices)
        provider = providers[prices.index(best)]
        best = int(best // 1)

        return {'price': '$' + str(best), 'provider': provider.dict, 'formatted_price': '$' + format(best, ',d').replace(',', '.')}

    @property
    def dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "brand": self.brand,
            "description": self.description,
            "complete_description": self.complete_description,
            "quantity": self.quantity,
            "category": self.category,
            "subcategory": self.subcategory,
            "url": self.url,
            "best_price": self.best_price,
        }

    @property
    def similar_products(self):
        if not self.category:
            return []
        products = Product.query.filter_by(category=self.category).all()
        products = list(filter(lambda prod: prod.id != self.id, products))
        products = list(filter(lambda product: len(product.offers) > 0 and product.best_price != None, products))
        return products[:3]


    def __repr__(self):
        return '<Product {id}: {description}>'.format(**self.__dict__)
