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

    @validator("cep", "rua", "numero", "bairro", "complemento", pre=True)
    def is_str(cls, v):
        if not isinstance(v, str):
            raise ValueError(Globals.INVALID_TYPE.format(type(v)))
        return v

    @validator("municipio_id", pre=True)
    def is_int(cls, v):
        if not isinstance(v, int):
            raise ValueError(Globals.INVALID_TYPE.format(type(v)))
        return v

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
                "estado": self.municipio.estado,
                "estado_sigla": self.municipio.estado.sigla,
                "pais": self.municipio.estado.pais}



class EnderecoModel(BaseModel):
    cep: Optional[constr(max_length=255)]
    rua: Optional[constr(max_length=255)]
    numero: Optional[constr(max_length=255)]
    bairro: Optional[constr(max_length=255)]
    complemento: Optional[constr(max_length=255)]
    municipio_id: Optional[int]

    class Config:
        orm_mode = True
