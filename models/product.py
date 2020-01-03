from dbconfig import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    code = db.Column(db.String(120), unique=False, nullable=True)
    tags = db.Column(db.Text, unique=False, nullable=True)
    url = db.Column(db.Text, unique=False, nullable=True)

    offers = db.relationship('Offer', backref='product', lazy=True, cascade = "all,delete")

    @property
    def best_price(self):
        best = 1000000000
        for offer in self.offers:
            best = min(best, offer.price)
            if offer.discount_price is not None:
                best = min(best, offer.discount_price)
        return int(best // 1)

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "tags": self.tags,
            "url": self.url,
            "best_price": self.best_price,
        }

    @property
    def similar_products(self):
        return Product.query.filter_by(tags=self.tags)

    def __repr__(self):
        return '<Product {id}: {name}>'.format(self.__dict__)
