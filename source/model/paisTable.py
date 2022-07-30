from application.database import db

class Pais(db.Model):
    __tablename__ = "pais"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

    estados = db.relationship('Estado', backref='pais_id', lazy=True)
