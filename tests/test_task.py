import pytest
from src.models import Task, User


@pytest.fixture(autouse=True)
def add_tasks(db_session):
    # Clear existing data
    db_session.query(User).delete()
    db_session.query(Task).delete()
    db_session.commit()

    user = User(email='testemail@email.com')
    db_session.add(user)

    task1 = Task(todo='First Todo', description="First Todo's Description", user=user)
    db_session.add(task1)

    task2 = Task(todo='Second Todo', description="Second Todo's Description", user=user)
    db_session.add(task2)

    db_session.commit()


def test_get_tasks(client):
    response = client.get('/tasks')
    result = response.json()

    assert response.status_code == 200
    assert len(result) == 2

    assert result[0]['todo'] == 'First Todo'
    assert result[0]['description'] == "First Todo's Description"

    assert result[1]['todo'] == 'Second Todo'
    assert result[1]['description'] == "Second Todo's Description"


def test_get_specific_task(client, db_session):
    response = client.get('/tasks/1')
    result = response.json()

    assert response.status_code == 200

    assert result['todo'] == 'First Todo'
    assert result['description'] == "First Todo's Description"

    response = client.get('/tasks/111')
    result = response.json()
    assert response.status_code == 404
    assert result['detail'] == "Task with id '111' not found"


def test_create_task(client, db_session):
    assert db_session.query(Task).count() == 2

    new_task = {'todo': 'New Task', 'description': 'New Task Description', 'user_id': 1}
    response = client.post('/tasks', json=new_task)
    assert response.status_code == 200

    result = response.json()
    assert result['todo'] == new_task['todo']
    assert result['description'] == new_task['description']

    assert db_session.query(Task).count() == 3


def test_update_task(client, db_session):
    update_task = {'todo': 'Updated Task'}
    response = client.patch('/tasks/1', json=update_task)
    assert response.status_code == 200

    result = response.json()
    assert result['todo'] == update_task['todo']

    response = client.patch('/tasks/111', json=update_task)
    result = response.json()

    assert response.status_code == 404
    assert result['detail'] == "Task with id '111' not found"


def test_completed_task(client, db_session):
    complete_tasks = {'ids': [1, 2], 'completed': True}
    response = client.patch('/tasks/complete/', json=complete_tasks)
    assert response.status_code == 200

    assert db_session.query(Task).filter(Task.id == 1).first().completed
    assert db_session.query(Task).filter(Task.id == 2).first().completed

    complete_tasks = {'ids': [1, 111], 'completed': True}
    response = client.patch('/tasks/complete/', json=complete_tasks)
    assert response.status_code == 404

    assert response.json()['detail'] == "Task with ids '111' not found"


def test_delete_tasks(client, db_session):
    delete_tasks = {'ids': [1, 2]}
    response = client.post('/tasks/delete', json=delete_tasks)
    assert response.status_code == 200

    assert db_session.query(Task).filter(Task.id == 1).first().deleted
    assert db_session.query(Task).filter(Task.id == 2).first().deleted


def test_permanent_delete_multiple_task(client, db_session):
    delete_tasks = {'ids': [1, 2]}
    response = client.post('/tasks/permanentDelete', json=delete_tasks)
    assert response.status_code == 200

    assert not db_session.query(Task).filter(Task.id == 1).first().is_active
    assert not db_session.query(Task).filter(Task.id == 2).first().is_active


def test_restore_multiple_task(client, db_session):
    task = db_session.query(Task).filter(Task.id == 1).first()
    task.deleted = True
    db_session.commit()

    restore_tasks = {'ids': [1]}
    response = client.patch('/tasks/restore/', json=restore_tasks)
    assert response.status_code == 200

    assert not db_session.query(Task).filter(Task.id == 1).first().deleted
