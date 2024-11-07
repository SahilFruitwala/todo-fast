from src.models import User, Task
from src.utils import get_hashed_password


def create_test_user(db_session, **kwargs) -> User:
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe' ,
        'email': 'testemail@email.com',
        'password': 'abc',
        **kwargs
    }
    user_data['password'] = get_hashed_password(user_data['password'])
    user = User(**user_data)

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def create_test_task(db_session, user=None, **kwargs) -> Task:
    db_user = user or create_test_user(db_session)

    task_data = {
        'todo': 'First Todo',
        'description': "First Todo's Description",
        'user_id': db_user.id,
        **kwargs
    }
    task = Task(**task_data)

    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    return task
