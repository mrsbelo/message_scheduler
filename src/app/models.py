from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=True)
    phone = db.Column(db.String, unique=True, nullable=True)


db.create_all()
