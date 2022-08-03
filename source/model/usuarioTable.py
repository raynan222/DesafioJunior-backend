from typing import Optional
from validate_docbr import CPF, PIS
import Globals
from application.app import db
from pydantic import BaseModel, constr, validator


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.BigInteger, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    pis = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(50), unique=True, nullable=False)
    endereco_id = db.Column(db.BigInteger, db.ForeignKey("endereco.id"), nullable=False)

    logins = db.relationship("Login", backref="usuario", lazy=True, viewonly=True)

    @validator("nome", pre=True)
    def is_str(cls, v):
        if not isinstance(v, str):
            raise ValueError(Globals.INVALID_TYPE.format(type(v)))
        return v

    @validator("pis", pre=True)
    def is_pis(cls, v):
        if not PIS().validate(v):
            raise ValueError(Globals.INVALID_PIS.format(type(v)))
        return v

    @validator("cpf", pre=True)
    def is_cpf(cls, v):
        if not CPF().validate(v):
            raise ValueError(Globals.INVALID_CPF.format(type(v)))
        return v

    def to_dict(self):
        return {"id": self.id,
                "nome": self.nome,
                "pis": self.pis,
                "cpf": self.cpf,
                "endereco_id": self.endereco_id}


class UsuarioModel(BaseModel):
    nome: Optional[constr(max_length=255)]
    pis: Optional[constr(max_length=50)]
    cpf: Optional[constr(max_length=50)]
    endereco_id: Optional[int]

    class Config:
        orm_mode = True
