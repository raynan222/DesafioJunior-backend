from application.database import db

class Endereco(db.Model):
    __tablename__ = "endereco"

    id = db.Column(db.BigInteger, primary_key=True)
    cep = db.Column(db.String(255), nullable=False)
    rua = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(255), nullable=False)
    bairro = db.Column(db.String(255), nullable=False)
    complemento = db.Column(db.String(255), nullable=True)

    municipio = db.Column(db.BigInteger, db.ForeignKey("municipio.id"), nullable=False)