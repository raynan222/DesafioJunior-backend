from typing import Optional

from application.database import db
from pydantic import BaseModel, constr

class Login(db.Model):
    __tablename__ = "login"

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.BigInteger, db.ForeignKey("usuario.id"), nullable=False)
    acesso_id = db.Column(db.Integer, db.ForeignKey("acesso.id"), nullable=False)

    usuarios = db.relationship('Usuario', backref='login', lazy=True)


class LoginModel(BaseModel):
    email: Optional[constr(max_length=255)]
    senha: Optional[constr(max_length=255)]
    usuario_id: Optional[int]
    acesso_id: Optional[int]

    class Config:
        orm_mode = True