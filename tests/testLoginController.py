import json


def test_list_logins(app, token_admin):
    with app.app_context():
        client = app.test_client()

        url = "/login/list"
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200


def test_list_logins_complete(app, token_admin):
    with app.app_context():
        client = app.test_client()

        url = "/login/list/complete"
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200


def test_view_login(app, token_admin, create_login):
    with app.app_context():
        client = app.test_client()

        id = create_login["id"]

        url = "/login/view/" + str(id)
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200


def test_view_login_complete(app, token_admin, create_login):
    with app.app_context():
        client = app.test_client()

        id = create_login["id"]

        url = "/login/view/complete/" + str(id)
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200


def test_delete_login(app, token_admin, create_login):
    with app.app_context():
        client = app.test_client()

        id = create_login["id"]
        url = "/login/delete/complete/" + str(id)
        response = client.delete(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200

        url = "/login/view/" + str(id)
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert output["error"]
        assert response.status_code == 200


def test_update_login(app, token_admin, create_login):
    with app.app_context():
        client = app.test_client()

        id = create_login["id"]
        url = "/login/update/" + str(id)
        update = {"email": "novo@mail.com"}
        response = client.put(url, data=json.dumps(update), headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200

        url = "/login/view/" + str(id)
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert output["email"] == update["email"]
        assert response.status_code == 200

        url = "/login/delete/complete/" + str(id)
        response = client.delete(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200


def test_update_login_complete(app, token_admin, create_login):
    import re

    with app.app_context():
        client = app.test_client()

        id = create_login["id"]
        url = "/login/update/complete/" + str(id)
        update = {
            "email": "novo@mail.com",
            "rua": "Nova morada",
            "cpf": "232.422.040-77",
        }
        response = client.put(url, data=json.dumps(update), headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200

        url = "/login/view/complete/" + str(id)
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert output.get("login").get("email") == update["email"]
        assert output.get("login").get("usuario").get("cpf") == re.sub(
            "[^\d]", "", update["cpf"]
        )
        assert (
            output.get("login").get("usuario").get("endereco").get("rua")
            == update["rua"]
        )
        assert response.status_code == 200

        url = "/login/delete/complete/" + str(id)
        response = client.delete(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200


def test_update_senha(app, create_login, token_admin):
    from Globals import TEST_LOGIN

    with app.app_context():
        client = app.test_client()

        # Cria um token de acesso com o login usuario
        login = create_login
        id = login["id"]
        header_usuario = login["header"]

        url = "/login/update/senha"
        update = {
            "senha_antiga": "Senha-Secreta",
            "senha_nova1": "minha_nova_senha",
            "senha_nova2": "minha_nova_senha",
        }
        response = client.put(url, data=json.dumps(update), headers=header_usuario)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200

        url = "/login"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        data = {"email/cpf/pis": TEST_LOGIN["email"], "senha": "minha_nova_senha"}
        response = client.post(url, data=json.dumps(data), headers=headers)
        assert response.status_code == 200

        url = "/login/delete/complete/" + str(id)
        response = client.delete(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200
