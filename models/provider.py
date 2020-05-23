from dbconfig import db


class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, unique=False, nullable=True)
    # latitude = db.Column(db.Float, nullable=True)
    # longitude = db.Column(db.Float, nullable=True)
    url = db.Column(db.Text, unique=False, nullable=True)

    offers = db.relationship(
        "Offer", backref="provider", lazy=True, cascade="all,delete"
    )

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description or "",
            # "latitude": self.latitude,
            # "longitude": self.longitude,
            "url": self.url,
        }

    def __repr__(self):
        return "<Provider {}>".format(self.name)
