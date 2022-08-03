import json
from Globals import TEST_LOGIN


def test_list_logins(app, token_admin):
    with app.app_context():
        client = app.test_client()

        url = "/login/list"
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200

def test_add_login(app, token_admin):
    with app.app_context():
        client = app.test_client()

        url = "/login/add"
        response = client.put(url, data=json.dumps(TEST_LOGIN), headers=token_admin)
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


def test_delete_login(app, token_admin, create_login):
    with app.app_context():
        client = app.test_client()

        id = create_login["id"]
        url = "/login/delete/" + str(id)
        response = client.delete(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200


        url = "/login/view/" + str(id)
        response = client.get(url, headers=token_admin)
        output = json.loads(response.get_data())
        assert output["error"]
        assert response.status_code == 200