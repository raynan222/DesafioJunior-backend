import json
from flask_script import Command


def insert_pais(nome: str):
    from application.app import db
    from source.model import Pais

    pais = Pais()
    pais.nome = nome
    db.session.add(pais)

    try:
        db.session.commit()
        return pais.id
    except Exception as e:
        print("Insert de pais nao realizado ->", e)


def insert_estado(nome: str, sigla: str, pais_id: int):
    from application.app import db
    from source.model import Estado

    estado = Estado()
    estado.nome = nome
    estado.sigla = sigla
    estado.pais_id = pais_id
    db.session.add(estado)

    try:
        db.session.commit()
        return estado.id
    except Exception as e:
        print("insert de estado nao realizado ->", e)


def insert_cidades(lista_cidades: list, uf_id: int):
    from application.app import db
    from source.model import Municipio

    for nome in lista_cidades:
        municipio = Municipio()
        municipio.nome = nome
        municipio.uf_id = uf_id
        db.session.add(municipio)
        try:
            db.session.commit()
        except Exception as e:
            print("insert de cidade nao realizado ->", e)


def insert_acessos():
    from application.app import db
    from source.model import Acesso

    acessos = ["administracao", "usuario", "visitante"]
    for nome in acessos:
        acesso = Acesso()
        acesso.nome = nome
        db.session.add(acesso)
        try:
            db.session.commit()
        except Exception as e:
            print("insert de acesso nao realizado ->", e)


def insert_adm():
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
        "municipio_id": randint(0, 5000),
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


# Gerenciador de comandos para que possa ser executado por manager
class Populate(Command):
    def run(self):
        main()


def main():
    # Script usado para popular o banco com os municípios e estados brasileiros
    # Adiciona os níveis de acesso e um usuário administrador com os dados de login
    # Email: admin@local.com  Senha: admin
    with open("./utils/db/cidade_estados.json", encoding="utf8") as f:
        data = json.load(f)

    pais_id = insert_pais("Brasil")
    for value in data.values():
        for estado in value:
            uf_id = insert_estado(
                nome=estado["nome"], sigla=estado["sigla"], pais_id=pais_id
            )
            insert_cidades(lista_cidades=estado["cidades"], uf_id=uf_id)

    insert_acessos()
    insert_adm()
