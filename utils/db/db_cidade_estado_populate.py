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

#Gerenciador de comandos para ser executado por manager
class Populate(Command):
    def run(self):
        main()

def main():
    with open('./utils/db/cidade_estados.json', encoding="utf8") as f:
        data = json.load(f)

    pais_id = insert_pais("Brasil")
    for value in data.values():
        for estado in value:
            uf_id = insert_estado(nome=estado["nome"], sigla=estado["sigla"], pais_id=pais_id)
            insert_cidades(lista_cidades=estado["cidades"], uf_id=uf_id)
