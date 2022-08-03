from application.app import db
from pydantic import BaseModel, constr


class Acesso(db.Model):
    __tablename__ = "acesso"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)

    logins = db.relationship("Login", backref="acesso", lazy=True)

    def to_dict(self):
        return{"id": self.id,
               "nome": self.nome}


class AcessoModel(BaseModel):
    nome: constr(max_length=255)

    class Config:
        orm_mode = True
