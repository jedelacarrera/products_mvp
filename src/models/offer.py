from src.dbconfig import db


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey("provider.id"), nullable=False)
    price = db.Column(db.Integer, nullable=True)  # Precio
    sale_price = db.Column(db.Integer, nullable=True)  # Precio con descuento
    comment = db.Column(db.Text, unique=False, nullable=True)
    source = db.Column(db.Text, unique=False, nullable=True)

    @property
    def dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "provider": self.provider.dict,
            "price": self.price,
            "sale_price": self.sale_price,
            "comment": self.comment,
            "source": self.source,
        }

    def best_price(self):
        if self.price and self.sale_price:
            return min(self.price, self.sale_price), True
        if self.price and not self.sale_price:
            return self.price, False
        if not self.price and self.sale_price:
            return self.sale_price, True
        return None, None

    def __repr__(self):
        return "<Offer {}>".format(self.id)
