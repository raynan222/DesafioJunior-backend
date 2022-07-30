from application.database import db


class Acesso(db.Model):
    __tablename__ = "acesso"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)