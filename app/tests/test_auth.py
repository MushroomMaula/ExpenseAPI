from app import crud
from app.core.security import manager
from app.tests.utils import random_string


def test_login(client, user_data_factory, db):
    # create user in db
    user_data = user_data_factory()
    user_data.password = 'hunter2'
    crud.user.create(db, user_data)
    resp = client.post(
        '/auth/login',
        data={
            'username': user_data.email,
            'password': 'hunter2'
        }
    )
    assert resp.status_code == 200
    token = resp.json().get('access_token')
    assert token == manager.create_access_token(
        data={'sub': user_data.email}
    )


def test_invalid_user(client):
    resp = client.post(
        '/auth/login',
        data={'username': 'email@doesnot.exist', 'password': random_string()}
    )
    assert resp.status_code == 401


def test_invalid_password(client, db_user_factory, db):
    user = db_user_factory()
    resp = client.post(
        '/auth/login',
        data={'username': user.email, 'password': 'wrongpassword'}
    )
    assert resp.status_code == 401
