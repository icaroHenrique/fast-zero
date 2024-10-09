from http import HTTPStatus


def test_root_return_ok_and_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_negative_get_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_negative_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'icarohenrique',
            'email': 'icaro@example.com',
            'password': 'password'
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_negative_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'icaro',
            'email': 'icaro@example.com',
            'password': 'password'
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
            'username': 'icaro',
            'email': 'icaro@example.com',
            'id': 1
        }


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [
        {
            'username': 'icaro',
            'email': 'icaro@example.com',
            'id': 1
        }
    ]}


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
            'username': 'icaro',
            'email': 'icaro@example.com',
            'id': 1
        }


def test_update_user(client):
    response = client.put(  # UserSchema
        '/users/1',
        json={
            'username': 'icarohenrique',
            'email': 'icaro@example.com',
            'password': 'password'
        }
    )

    assert response.json() == {
            'username': 'icarohenrique',
            'email': 'icaro@example.com',
            'id': 1
        }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_root_return_html(client):
    response = client.get('/html-test')
    assert '<h1> Olá Mundo </h1>' in response.text
