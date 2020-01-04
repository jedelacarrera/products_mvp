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
        pack = ''
        for offer in self.offers:
            if offer.price:
                best = min(best, offer.price)
            if offer.sale_price is not None:
                best = min(best, offer.sale_price)

        if best == Product.MAX_PRICE:
            return offer.pack_price
        return '$ ' + str(int(best // 1))

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
        return Product.query.filter_by(category=self.category).all()

    def __repr__(self):
        return '<Product {id}: {description}>'.format(self.__dict__)
