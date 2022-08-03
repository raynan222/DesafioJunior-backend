import json
from Globals import TEST_USUARIO



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
        response = client.put(url, data=json.dumps(TEST_USUARIO), headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200

def test_view_usuario(app, token_admin):
    with app.app_context():
        client = app.test_client()

        url = "/login/list?email=" + "admin@local.com"
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert response.status_code == 200
        assert not output["error"]
        assert output["itens"][0]

        id = output["itens"][0]["usuario_id"]

        url = "/usuario/view/" + str(id)
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        print(output)
        assert not output["error"]
        assert response.status_code == 200

def test_delete_usuario(app, create_login, token_admin):


    with app.app_context():

        client = app.test_client()

        id = create_login["id"]

        url = "/login/delete/" + str(id)
        response = client.delete(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert response.status_code == 200
        assert not output["error"]

        url = "/usuario/view/" + str(id)
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200