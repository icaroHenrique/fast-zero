from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_return_ok_and_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_negative_get_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_negative_update_user_not_found(client, token):
    response = client.put(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'icarohenrique',
            'email': 'icaro@example.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_negative_update_forbidden(client, token):
    client.post(
        '/users/',
        json={
            'username': 'icaro',
            'email': 'icaro@example.com',
            'password': 'password',
        },
    )

    response = client.put(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'icarohenrique',
            'email': 'icaro@example.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_negative_delete_user_not_found(client, token):
    response = client.delete(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_negative_delete_forbidden(client, token):
    client.post(
        '/users/',
        json={
            'username': 'icaro',
            'email': 'icaro@example.com',
            'password': 'password',
        },
    )

    response = client.delete(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'icaro',
            'email': 'icaro@example.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'icaro',
        'email': 'icaro@example.com',
        'id': 1,
    }


def test_negative_create_user_with_already_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'icaro@example.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_negative_create_user_with_already_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'icaro',
            'email': 'teste@teste.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_with_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_update_user(client, user, token):
    response = client.put(  # UserSchema
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'icarohenrique',
            'email': 'icaro@example.com',
            'password': 'password',
        },
    )

    assert response.json() == {
        'username': 'icarohenrique',
        'email': 'icaro@example.com',
        'id': 1,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.decrypted_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_negative_get_token_invalid_username(client, user):
    response = client.post(
        '/token',
        data={'username': 'false-email', 'password': user.decrypted_password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_negative_get_token_invalid_password(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': 'false-password'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_root_return_html(client):
    response = client.get('/html-test')
    assert '<h1> Olá Mundo </h1>' in response.text
