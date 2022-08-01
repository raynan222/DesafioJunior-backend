from typing import Optional

from application.database import db
from pydantic import BaseModel, constr


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.BigInteger, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    pis = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(50), unique=True, nullable=False)
    #desativar nullable
    endereco_id = db.Column(db.BigInteger, db.ForeignKey("endereco.id"), nullable=True)


class UsuarioModel(BaseModel):
    nome: Optional[constr(max_length=255)]
    pis: Optional[constr(max_length=50)]
    cpf: Optional[constr(max_length=50)]
    endereco_id: Optional[int]

    class Config:
        orm_mode = True
