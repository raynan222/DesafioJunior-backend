import re
from typing import Optional

import Globals
from application.app import db
from pydantic import BaseModel, constr, validator


class Login(db.Model):
    __tablename__ = "login"

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.BigInteger, db.ForeignKey("usuario.id"), nullable=False)
    acesso_id = db.Column(db.Integer, db.ForeignKey("acesso.id"), nullable=False)

    usuarios = db.relationship("Usuario", backref="login", lazy=True)

    @validator("senha", pre=True)
    def is_str(cls, v):
        if not isinstance(v, str):
            raise ValueError(Globals.INVALID_TYPE.format(type(v)))
        return v

    @validator("usuario_id", "acesso_id", pre=True)
    def is_int(cls, v):
        if not isinstance(v, int):
            raise ValueError(Globals.INVALID_TYPE.format(type(v)))
        return v

    @validator("email", pre=True)
    def is_email(cls, v):
        reg = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if isinstance(re.fullmatch(reg, v), re.Match):
            raise ValueError(Globals.INVALID_EMAIL.format(type(v)))
        return v

    def to_dict(self):
        return {"email": self.email, "usuario_id": self.email, "acesso_id": self.acesso_id}

    def to_dict_complete(self):
        return {
                "error": False,
                "id": self.id,
                "email": self.email,
                "usuario_id": self.usuario_id,
                "usuario": {
                    "id": self.usuario.id,
                    "nome": self.usuario.nome,
                    "cpf": self.usuario.cpf,
                    "pis": self.usuario.pis,
                    "endereco": {
                        "cep": self.usuario.endereco.cep,
                        "rua": self.usuario.endereco.rua,
                        "numero": self.usuario.endereco.numero,
                        "bairro": self.usuario.endereco.bairro,
                        "complemento": self.usuario.endereco.complemento,
                        "municipio": self.usuario.endereco.municipio.nome,
                        "estado": self.usuario.endereco.municipio.estado.nome,
                        "estado_sigla": self.usuario.endereco.municipio.estado.sigla,
                        "pais": self.usuario.endereco.municipio.estado.pais.nome,
                    },
                    "endereco_id": self.usuario.endereco_id,
                }if self.usuario_id is not None
                else None,
                "acesso_id": self.acesso_id,
                "acesso": {"id": self.acesso.id, "nome": self.acesso.nome},
              }


class LoginModel(BaseModel):
    email: Optional[constr(max_length=255)]
    senha: Optional[constr(max_length=255)]
    usuario_id: Optional[int]
    acesso_id: Optional[int]

    class Config:
        orm_mode = True