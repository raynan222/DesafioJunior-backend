import re
from typing import Optional

import Messages
from application.database import db
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
            raise ValueError(Messages.INVALID_TYPE.format(type(v)))
        return v

    @validator("usuario_id", "acesso_id", pre=True)
    def is_int(cls, v):
        if not isinstance(v, int):
            raise ValueError(Messages.INVALID_TYPE.format(type(v)))
        return v

    @validator("email", pre=True)
    def is_email(cls, v):
        reg = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if isinstance(re.fullmatch(reg, v), re.Match):
            raise ValueError(Messages.INVALID_EMAIL.format(type(v)))
        return v


class LoginModel(BaseModel):
    email: Optional[constr(max_length=255)]
    senha: Optional[constr(max_length=255)]
    usuario_id: Optional[int]
    acesso_id: Optional[int]

    class Config:
        orm_mode = True
