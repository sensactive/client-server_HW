from sqlalchemy import (
    create_engine, Table, Column,
    MetaData, String, Integer
)

from sqlalchemy.orm import mapper


engine = create_engine('sqlite:///../../alchemy.db')

metadata = MetaData()

user_table = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True),
    Column('login', String),
    Column('info', String)
)

metadata.create_all(engine)


class User:
    def __init__(self, login, info):
        self.login = login
        self.info = info


mapper(User, user_table)
