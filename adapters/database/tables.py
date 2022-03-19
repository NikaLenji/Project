import datetime

from sqlalchemy import (Column,
                        ForeignKey,
                        Integer,
                        MetaData,
                        String,
                        Table,
                        DateTime,
                        BigInteger)


metadata = MetaData()

users = Table(
    'Users',
    metadata,
    Column('id_user', BigInteger, primary_key=True, autoincrement=True),
    Column('name_user', String(100), nullable=False),
    Column('login', String(100), nullable=False),
    Column('password', String(100), nullable=False),
)

chats = Table(
    'Chat',
    metadata,
    Column('id_chat', BigInteger, primary_key=True, autoincrement=True),
    Column('name_chat', String(100), nullable=False),
    Column('description', String(500), nullable=False),
    Column('author_of_chat', Integer, ForeignKey('Users.id_user'), nullable=False),
)

messages_chat = Table(
    'MessagesChat',
    metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('id_chat', Integer, ForeignKey('Chat.id_chat')),
    Column('id_user', Integer, ForeignKey('Users.id_user')),
    Column('text_message', String(1000)),
)

members_chat = Table(
    'MembersChat',
    metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('id_chat', Integer, ForeignKey('Chat.id_chat')),
    Column('id_user', Integer, ForeignKey('Users.id_user')),
)
