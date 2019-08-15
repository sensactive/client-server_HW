from sqlalchemy import (
    create_engine, Table, Column,
    MetaData, String, Integer, DateTime
)

from sqlalchemy.orm import mapper


# engine = create_engine('sqlite:///../../alchemy.db')

metadata = MetaData()

user_history_table = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True),
    Column('date', DateTime),
    Column('ip_address', String)
)

# metadata.create_all(engine)


class UserHistory:
    def __init__(self, date, ip_address):
        self.date = date
        self.ip_address = ip_address


mapper(UserHistory, user_history_table)
