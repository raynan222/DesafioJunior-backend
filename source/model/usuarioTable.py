from typing import Optional
from validate_docbr import CPF, PIS
import Messages
from application.database import db
from pydantic import BaseModel, constr, validator


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.BigInteger, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    pis = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(50), unique=True, nullable=False)
    endereco_id = db.Column(db.BigInteger, db.ForeignKey("endereco.id"), nullable=False)

    @validator("nome", pre=True)
    def is_str(cls, v):
        if not isinstance(v, str):
            raise ValueError(Messages.INVALID_TYPE.format(type(v)))
        return v

    @validator("pis", pre=True)
    def is_int(cls, v):
        if not PIS().validate(v):
            raise ValueError(Messages.INVALID_PIS.format(type(v)))
        return v

    @validator("cpf", pre=True)
    def is_int(cls, v):
        if not CPF().validate(v):
            raise ValueError(Messages.INVALID_CPF.format(type(v)))
        return v


class UsuarioModel(BaseModel):
    nome: Optional[constr(max_length=255)]
    pis: Optional[constr(max_length=50)]
    cpf: Optional[constr(max_length=50)]
    endereco_id: Optional[int]

    class Config:
        orm_mode = True
