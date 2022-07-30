from application.database import db

class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.BigInteger, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    pis = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(50), unique=True, nullable=False)

    endereco_id = db.Column(db.BigInteger, db.ForeignKey("endereco.id"), nullable=False)
