from application.app import db
from pydantic import BaseModel, constr


class Regra(db.Model):
    __tablename__ = "regra"

    id = db.Column(db.String(20), nullable=False, primary_key=True)
    acesso_id = db.Column(
        db.Integer, db.ForeignKey("acesso.id"), nullable=False, primary_key=True
    )
    controller_id = db.Column(
        db.Integer, db.ForeignKey("controller.id"), nullable=False, primary_key=True
    )
    permicao = db.Column(db.Boolean, nullable=False)


class RegraModel(BaseModel):
    acesso_id: int
    controller_id: int
    permicao: bool

    class Config:
        orm_mode = True
