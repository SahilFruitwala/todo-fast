import pytest
from src.models import Task, User


@pytest.fixture(autouse=True)
def add_tasks(db_session):
    # Clear existing data
    db_session.query(User).delete()
    db_session.query(Task).delete()
    db_session.commit()

    user = User(email='user-1@email.com')
    db_session.add(user)

    user1 = User(email='user-2@email.com', first_name='john', last_name='doe')
    db_session.add(user1)

    task1 = Task(todo='First Todo', description="First Todo's Description", user=user)
    db_session.add(task1)

    task2 = Task(todo='Second Todo', description="Second Todo's Description", user=user)
    db_session.add(task2)

    db_session.commit()


def test_get_users(client):
    response = client.get('/users')
    result = response.json()

    assert response.status_code == 200
    assert len(result) == 2

    assert result[0]['first_name'] is None
    assert result[0]['last_name'] is None
    assert result[0]['email'] == 'user-1@email.com'

    assert result[1]['first_name'] == 'john'
    assert result[1]['last_name'] == 'doe'
    assert result[1]['email'] == 'user-2@email.com'


def test_get_specific_user(client, db_session):
    response = client.get('/users/1')
    result = response.json()

    assert response.status_code == 200

    assert result['first_name'] is None
    assert result['last_name'] is None
    assert result['email'] == 'user-1@email.com'

    response = client.get('/users/111')
    result = response.json()
    assert response.status_code == 404
    assert result['detail'] == "User with id '111' not found"


def test_create_user(client, db_session):
    assert db_session.query(User).count() == 2

    new_user = {'first_name': 'Jane', 'last_name': 'Doe', 'email': 'user-3@email.com'}
    response = client.post('/users', json=new_user)
    assert response.status_code == 200

    result = response.json()
    assert result['first_name'] == 'Jane'
    assert result['last_name'] == 'Doe'
    assert result['email'] == 'user-3@email.com'

    assert db_session.query(User).count() == 3


def test_update_user(client, db_session):
    update_user = {'first_name': 'Updated Jane'}
    response = client.patch('/users/1', json=update_user)
    assert response.status_code == 200

    result = response.json()
    assert result['first_name'] == update_user['first_name']

    response = client.patch('/users/111', json=update_user)
    result = response.json()

    assert response.status_code == 404
    assert result['detail'] == "User with id '111' not found"


def test_delete_tasks(client, db_session):
    response = client.post('/users/delete/1')
    assert response.status_code == 200

    assert not db_session.query(User).filter(User.id == 1).first().is_active
