from application.database import db
from pydantic import BaseModel, constr

class Pais(db.Model):
    __tablename__ = "pais"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

    estados = db.relationship('Estado', backref='pais', lazy=True)


class PaisModel(BaseModel):
    nome: constr(max_length=255)

    class Config:
        orm_mode = True