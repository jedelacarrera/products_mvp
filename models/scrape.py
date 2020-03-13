import datetime
from dbconfig import db

STARTED = 'STARTED'
SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'

class Scrape(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    status = db.Column(db.Text, default=STARTED, nullable=False)
    filename = db.Column(db.Text, nullable=True)

    @property
    def dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "filename": self.filename,
        }

    def __repr__(self):
        return '<Scrape {}>'.format(self.id)
