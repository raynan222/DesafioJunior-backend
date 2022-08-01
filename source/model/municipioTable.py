from application.database import db
from pydantic import BaseModel, constr

class Municipio(db.Model):
    __tablename__ = "municipio"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    uf_id = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)


class MunicipioModel(BaseModel):
    nome: constr(max_length=255)
    uf_id: int

    class Config:
        orm_mode = True
