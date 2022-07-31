from application.database import db

class Login(db.Model):
    __tablename__ = "login"

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    usuario_id = db.Column(db.BigInteger, db.ForeignKey("usuario.id"), nullable=False)
    acesso_id = db.Column(db.Integer, db.ForeignKey("acesso.id"), nullable=False)

    usuario = db.relationship('Usuario', backref='login', lazy=True, uselist=False)