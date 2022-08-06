import re
from typing import Optional
import Globals
from application.app import db
from pydantic import BaseModel, constr, validator


class Endereco(db.Model):
    __tablename__ = "endereco"

    id = db.Column(db.BigInteger, primary_key=True)
    cep = db.Column(db.String(255), nullable=False)
    rua = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(255), nullable=False)
    bairro = db.Column(db.String(255), nullable=False)
    complemento = db.Column(db.String(255), nullable=True)
    municipio_id = db.Column(
        db.BigInteger, db.ForeignKey("municipio.id"), nullable=False
    )
    usuarios = db.relationship("Usuario", backref="endereco", lazy=True)

    def to_dict(self):
        return {"id": self.id,
                "cep": self.cep,
                "rua": self.rua,
                "numero": self.numero,
                "bairro": self.bairro,
                "complemento": self.complemento,
                "municipio_id": self.municipio_id}

    def to_dict_complete(self):
        return {"id": self.id,
                "cep": self.cep,
                "rua": self.rua,
                "numero": self.numero,
                "bairro": self.bairro,
                "complemento": self.complemento,
                "municipio": self.municipio.nome,
                "estado": self.municipio.estado.nome,
                "estado_sigla": self.municipio.estado.sigla,
                "pais": self.municipio.estado.pais.nome}


class EnderecoModel(BaseModel):
    cep: Optional[constr(max_length=255)]
    rua: Optional[constr(max_length=255)]
    numero: Optional[constr(max_length=255)]
    bairro: Optional[constr(max_length=255)]
    complemento: Optional[constr(max_length=255)]
    municipio_id: Optional[int]

    class Config:
        orm_mode = True

    @validator("cep", "rua", "numero", "bairro", "complemento", pre=True)
    def is_str(cls, v):
        if not isinstance(v, str):
            print("pau na strings endereco")
            raise ValueError(Globals.INVALID_TYPE.format(type(v)))
        return v

    @validator("municipio_id", pre=True)
    def is_int(cls, v):
        if not isinstance(v, int):
            print("pau no municpio ID")
            raise ValueError(Globals.INVALID_TYPE.format(type(v)))
        return v

    @validator("cep", pre=True)
    def is_cep(cls, v):
        cep = re.sub("[^\d]", "", v)
        reg = "^\d{5}\-\d{3}"
        if len(cep) != 8 or re.fullmatch(reg, v) is None:
            print("pau na strings CEP")
            raise ValueError(Globals.INVALID_TYPE.format(type(v)))
        return v
