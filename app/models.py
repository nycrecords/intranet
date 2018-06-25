from app import db


class Sign_In(db.Model):
    __tablename__ = 'sign_in'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    affiliation = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(14))
    address = db.Column(db.String(128))
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))
    country = db.Column(db.String(2))
    library = db.Column(db.Boolean)
    archives = db.Column(db.Boolean)
    genealogy = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Sign_In %r>' % self.id
