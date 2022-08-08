import json


def test_list_usuarios(app, token_admin):
    with app.app_context():
        client = app.test_client()

        url = "/usuario/list"
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200


def test_add_usuario(app, token_admin):
    with app.app_context():
        client = app.test_client()

        url = "/usuario/add"
        usuario = {
            "nome": "Seu Jorge",
            "cpf": "57171487040",
            "pis": "51057824007",
            "endereco_id": 1,
        }
        response = client.put(url, data=json.dumps(usuario), headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200


def test_view_usuario(app, token_admin, create_login):
    with app.app_context():
        client = app.test_client()

        id = create_login["id"]
        url = "/usuario/view/" + str(id)
        response = client.get(url, headers=token_admin)
        print(response)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200


def test_delete_usuario(app, create_login, token_admin):

    with app.app_context():

        client = app.test_client()

        id = create_login["id"]

        url = "/login/delete/complete/" + str(id)
        response = client.delete(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert response.status_code == 200
        assert not output["error"]

        url = "/usuario/view/" + str(id)
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200


def test_update_usuario(app, create_login, token_admin):
    with app.app_context():

        client = app.test_client()

        login = create_login
        url = "/usuario/update/" + str(login["usuario_id"])
        update = {"nome": "Olavo Novo"}
        response = client.put(url, data=json.dumps(update), headers=token_admin)
        output = json.loads(response.get_data())
        assert response.status_code == 200
        assert not output["error"]

        url = "/usuario/view/" + str(login["usuario_id"])
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert output["nome"] == update["nome"]
        assert response.status_code == 200
