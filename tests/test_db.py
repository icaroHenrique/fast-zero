from dataclasses import asdict

from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        user = User(
            username='icaro', email='icaro@mail.com', password='secreto'
        )
        session.add(user)
        session.commit()

    result = session.scalar(
        select(User).where(User.email == 'icaro@mail.com')
    )

    print(result.created_at)

    assert asdict(result) == {
        'id': 1,
        'username': 'icaro',
        'password': 'secreto',
        'email': 'icaro@mail.com',
        'created_at': time,
    }
