import pytest
from src.models import Task, User
from src.utils import get_hashed_password, check_password
from tests.test_utils import create_test_task, create_test_user


@pytest.fixture(autouse=True)
def add_tasks(db_session):
    # Clear existing data
    db_session.query(User).delete()
    db_session.query(Task).delete()
    db_session.commit()

    user = create_test_user(db_session, email='user-1@email.com')
    create_test_task(db_session, user)
    create_test_task(db_session, user, todo='Second Todo', description="Second Todo's Description")

    create_test_user(db_session, email='user-2@email.com', first_name='john', last_name='doe')


def test_get_specific_user(client, db_session):
    response = client.get('/users/1')
    result = response.json()

    assert response.status_code == 200

    assert result['first_name'] == 'John'
    assert result['last_name'] == 'Doe'
    assert result['email'] == 'user-1@email.com'

    response = client.get('/users/111')
    result = response.json()
    assert response.status_code == 404
    assert result['detail'] == "User with id '111' not found"


def test_create_user(client, db_session):
    assert db_session.query(User).count() == 2

    new_user = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'user-3@email.com',
        'password': 'abc',
        'confirm_password': 'pqr',
    }
    response = client.post('/users', json=new_user)
    assert response.status_code == 422
    result = response.json()
    assert 'Passwords do not match!' in result['detail'][0]['msg']

    new_user = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'user-3@email.com',
        'password': 'abc',
        'confirm_password': 'abc',
    }
    response = client.post('/users', json=new_user)
    assert response.status_code == 200

    result = response.json()
    assert result['first_name'] == 'Jane'
    assert result['last_name'] == 'Doe'
    assert result['email'] == 'user-3@email.com'

    assert db_session.query(User).count() == 3


def test_update_user(client, db_session):
    update_user = {'first_name': 'Updated Jane', 'password': 'abc'}

    response = client.patch('/users/1', json=update_user)
    assert response.status_code == 422

    result = response.json()
    assert 'Both password fields are required!' in result['detail'][0]['msg']

    update_user = {'first_name': 'Updated Jane', 'password': 'abc', 'new_password': 'abc'}

    response = client.patch('/users/1', json=update_user)
    assert response.status_code == 422

    result = response.json()
    assert 'Password fields cannot be same!' in result['detail'][0]['msg']

    update_user = {'first_name': 'Updated Jane', 'password': 'abc', 'new_password': 'pqr'}
    response = client.patch('/users/1', json=update_user)
    assert response.status_code == 200

    result = response.json()
    updated_user = db_session.query(User).filter(User.id == 1).first()
    assert result['first_name'] == update_user['first_name']
    assert check_password('pqr', updated_user.password)

    response = client.patch('/users/111', json=update_user)
    result = response.json()

    assert response.status_code == 404
    assert result['detail'] == "User with id '111' not found"


def test_delete_tasks(client, db_session):
    response = client.post('/users/delete/1')
    assert response.status_code == 200

    assert not db_session.query(User).filter(User.id == 1).first().is_active
