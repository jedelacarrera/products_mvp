from dbconfig import db

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    price = db.Column(db.Float, nullable=True)  # Precio
    discount_price = db.Column(db.Float, nullable=True)  # Precio con descuento
    promotion_price = db.Column(db.Float, nullable=True)  # Precio con promocion
    description = db.Column(db.Text, unique=False, nullable=True)

    @property
    def dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "provider": self.provider.dict,
            "price": self.price,
            "discount_price": self.discount_price,
            "promotion_price": self.promotion_price,
            "description": self.description,
        }

    def __repr__(self):
        return '<Offer {}>'.format(self.id)