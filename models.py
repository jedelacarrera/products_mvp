from dbconfig import db
import constants

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    profiles_count = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=False)  # PENDING, STARTED, FINISHED, ERROR

    profiles = db.relationship('Profile', backref='search', lazy=True, cascade="all,delete")

    @property
    def progress(self):
        if self.status == constants.PENDING:
            return 0
        if self.status == constants.STARTED:
            profiles = len(self.profiles)
            return profiles / self.profiles_count
        return 1  # FINISHED or ERROR

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'profiles_count': self.profiles_count,
            'date': self.date,
            'status': self.status,
        }


    def __repr__(self):
        return '<Search {} - {}>'.format(self.id, self.name)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey('search.id', ondelete='CASCADE'), nullable=False)
    first_name = db.Column(db.String(120), unique=False, nullable=True)
    second_name = db.Column(db.String(120), unique=False, nullable=True)
    first_lastname = db.Column(db.String(120), unique=False, nullable=True)
    second_lastname = db.Column(db.String(120), unique=False, nullable=True)
    rut = db.Column(db.String(120), unique=False, nullable=True)
    url1 = db.Column(db.String(120), unique=False, nullable=True)
    url2 = db.Column(db.String(120), unique=False, nullable=True)
    url3 = db.Column(db.String(120), unique=False, nullable=True)
    count = db.Column(db.Integer, unique=False, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'search_id': self.search_id,
            'first_name': self.first_name,
            'second_name': self.second_name,
            'first_lastname': self.first_lastname,
            'second_lastname': self.second_lastname,
            'rut': self.rut,
            'url1': self.url1,
            'url2': self.url2,
            'url3': self.url3,
            'count': self.count,
        }

    def to_csv(self):
        string = ''
        string += (self.rut or '') + ','
        string += (self.first_name or '') + ','
        string += (self.second_name or '') + ','
        string += (self.first_lastname or '') + ','
        string += (self.second_lastname or '') + ','
        string += (self.url1 or '') + ','
        string += (self.url2 or '') + ','
        string += (self.url3 or '') + ','
        string += str(self.count or 0)

        return string

    def __repr__(self):
        return '<Profile {}>'.format(self.id)
