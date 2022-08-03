import json
from random import random

import pytest
import sqlalchemy
from Globals import TEST_LOGIN, TEST_USUARIO
from application.app import app as _app, db as _db
from config import BASE_DIR



def pytest_sessionstart():
    with _app.app_context():
        _app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5432/web_app_test'
        _db.drop_all()
        _db.create_all()

        session = _db.session()

        sql_file = open(BASE_DIR + "/utils/db/start.sql", "r")
        escaped_sql = sqlalchemy.text(sql_file.read())
        session.execute(escaped_sql)
        session.flush()

        session.commit()

        session.close()


def pytest_sessionfinish():
    _db.drop_all()
    _db.create_all()
    _db.session.commit()

@pytest.fixture
def app():
    return _app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def token_admin(app):
    with app.app_context():
        client = app.test_client()

        url = "/login"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {"email/cpf/pis": "admin@local.com", "senha": "senha_de_admin"}
        response = client.post(url, data=json.dumps(data), headers=headers)

        res = json.loads(response.get_data())
        header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(res["access_token"])}
        assert response.status_code == 200

        return header

@pytest.fixture
def create_login(app, token_admin):
    with app.app_context():
        client = app.test_client()

        #cria o login
        url = "/login/add"
        email = TEST_LOGIN["email"]+str(random())
        data = {"email": email, "senha": TEST_LOGIN["senha"],
                "usuario_id": TEST_LOGIN["usuario_id"], "acesso_id": TEST_LOGIN["acesso_id"]}
        response = client.put(url, data=json.dumps(data), headers=token_admin)

        #realiza o login com o login
        url = "/login"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {"email/cpf/pis": email, "senha": TEST_LOGIN["senha"]}
        response = client.post(url, data=json.dumps(data), headers=headers)
        #Cria token de acesso com o login feito acima
        res = json.loads(response.get_data())
        header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(res["access_token"])}

        url = "/loginview"
        response = client.get(url, headers=header)
        output = json.loads(response.get_data())

        assert response.status_code == 200
        return output
