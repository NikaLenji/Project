import datetime
from typing import Optional

import attr


@attr.dataclass
class User:
    name_user: str
    login: str
    password: str
    id_user: Optional[int] = None


@attr.dataclass
class Chat:
    author_of_chat: User
    creation_date: datetime.datetime = None
    name_chat: Optional[str] = None
    description: Optional[str] = None
    update_date: datetime.datetime = None
    id_chat: Optional[int] = None


@attr.dataclass
class MessagesChat:
    id_chat: Chat
    id_user: User
    text_message: Optional[str]


@attr.dataclass
class MembersChat:
    id_chat: Chat
    id_user: User
