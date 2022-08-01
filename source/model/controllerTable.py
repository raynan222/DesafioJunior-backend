from application.database import db
from pydantic import BaseModel, constr


class Controller(db.Model):
    __tablename__ = "controller"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)

    regras = db.relationship("Regra", backref="controller", lazy=True)


class ControllerModel(BaseModel):
    nome: constr(max_length=255)

    class Config:
        orm_mode = True