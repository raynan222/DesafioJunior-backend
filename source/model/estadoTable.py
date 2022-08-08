from application.app import db
from pydantic import BaseModel, constr


class Estado(db.Model):
    __tablename__ = "estado"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    sigla = db.Column(db.String(2), nullable=False, unique=True)
    pais_id = db.Column(db.Integer, db.ForeignKey("pais.id"), nullable=False)

    municipios = db.relationship("Municipio", backref="estado", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "sigla": self.sigla,
            "pais_id": self.pais_id,
        }


class EstadoModel(BaseModel):
    nome: constr(max_length=255)
    sigla: constr(max_length=2)
    pais_id: int

    class Config:
        orm_mode = True
