import random
from src.dbconfig import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(120), unique=True, index=True)
    brand = db.Column(db.String(120), unique=False, nullable=True, index=True)
    description = db.Column(db.Text, unique=False, nullable=True, index=True)
    complete_description = db.Column(db.Text, unique=False, nullable=True)
    quantity = db.Column(db.String(120), unique=False, nullable=True)
    category = db.Column(db.String(120), unique=False, nullable=True)
    subcategory = db.Column(db.String(120), unique=False, nullable=True, index=True)
    url = db.Column(db.Text, unique=False, nullable=True)

    offers = db.relationship(
        "Offer", backref="product", lazy=False, cascade="all,delete"
    )

    def best_price(self):
        best = 1000000000
        provider = None
        is_sale = False
        for offer in self.offers:
            offer_best_price, is_sale = offer.best_price()
            if offer_best_price is not None and offer_best_price < best:
                best = offer_best_price
                provider = offer.provider
        if provider is None:
            return None

        return {"price": best, "provider": provider.dict, "is_sale": is_sale}

    def dict_by_provider_id(self, provider_id):
        for offer in self.offers:
            if offer.provider_id != provider_id:
                continue
            offer_price, is_sale = offer.best_price()
            if offer_price is None:
                continue
            product_dict = self.dict
            product_dict["best_price"] = {
                "price": offer_price,
                "provider": offer.provider.dict,
                "is_sale": is_sale,
            }
            return product_dict
        return None

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
            "best_price": self.best_price(),
        }

    @property
    def similar_products(self):
        if not self.subcategory:
            return []
        products = Product.query.filter_by(subcategory=self.subcategory).limit(30).all()
        products = list(filter(lambda prod: prod.id != self.id, products))
        products = list(
            filter(
                lambda product: len(product.offers) > 0
                and product.best_price() is not None,
                products,
            )
        )
        random.shuffle(products)
        return products[:3]

    def __repr__(self):
        return "<Product {id}: {description}>".format(**self.__dict__)
