from auth.models import User
from database import Session
from decorators import logged


@logged
def create_user(request):
    name = request.get('name')
    password = request.get('password')
    user = User(name=name, password=password)
    session = Session()
    session.add(user)
    session.commit()


@logged
def update_user(request):
    session = Session()
    user = session.query(User).filter_by(id=request.user.user_id)
    user.name = request.get('name')
    user.password = request.get('password')
    session.add(user)
    session.commit()


@logged
def delete_user(request):
    session = Session()
    user = session.query(User).filter_by(id=request.user.id)
    session.delete(user)
    session.commit()
