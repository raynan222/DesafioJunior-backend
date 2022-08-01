from application.database import db
from pydantic import BaseModel, constr


class Acesso(db.Model):
    __tablename__ = "acesso"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)

    logins = db.relationship("Login", backref="acesso", lazy=True)


class AcessoModel(BaseModel):
    nome: constr(max_length=255)

    class Config:
        orm_mode = True
