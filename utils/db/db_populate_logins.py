def insert_user():
    from application.app import db
    from source.model import Endereco, Usuario, Login
    from werkzeug.security import generate_password_hash
    from random import randint

    endereco = {
        "cep": "60862101",
        "rua": "Rua 10",
        "numero": "122",
        "bairro": "Jd Castelinho",
        "complemento": "Não há",
        "municipio_id": randint(0, 5596),
    }
    endereco_insert = Endereco()
    for campo in endereco.keys():
        setattr(endereco_insert, campo, endereco.get(campo))
    db.session.add(endereco_insert)

    try:
        db.session.commit()
    except Exception as e:
        print("insert de endereco nao realizado ->", e)

    usuario = {
        "nome": "Osvaldo Souza",
        "pis": "21794821777",
        "cpf": "76764822085",
        "endereco_id": 1,
    }
    usuario_insert = Usuario()
    for campo in usuario.keys():
        setattr(usuario_insert, campo, usuario.get(campo))
    db.session.add(usuario_insert)

    try:
        db.session.commit()
    except Exception as e:
        print("insert de usuario nao realizado ->", e)

    login = {
        "email": "admin@local.com",
        "senha": generate_password_hash("admin", method="sha256"),
        "acesso_id": 1,
        "usuario_id": 1,
    }
    login_insert = Login()
    for campo in login.keys():
        setattr(login_insert, campo, login.get(campo))
    db.session.add(login_insert)

    try:
        db.session.commit()
    except Exception as e:
        print("insert de adm nao realizado ->", e)
