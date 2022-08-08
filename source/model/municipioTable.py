from application.app import db
from pydantic import BaseModel, constr


class Municipio(db.Model):
    __tablename__ = "municipio"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    uf_id = db.Column(db.Integer, db.ForeignKey("estado.id"), nullable=False)

    enderecos = db.relationship("Endereco", backref="municipio", lazy=True)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "uf_id": self.uf_id}


class MunicipioModel(BaseModel):
    nome: constr(max_length=255)
    uf_id: int

    class Config:
        orm_mode = True
