from typing import List, Optional

from sqlalchemy import select
from classic.components import component
from classic.sql_storage import BaseRepository

from application import interfaces
from application.dataclasses import User, Chat, MembersChat, MessagesChat


@component
class UserRepo(BaseRepository, interfaces.UserRepo):
    def check_user_login(self, user_login: str) -> Optional[User]:
        query = select(User).where(User.login == user_login)
        result = self.session.execute(query).scalars().one_or_none()
        return result

    def add_user(self, user: User):
        self.session.add(user)
        self.session.flush()
        return user

    def get_by_user_id(self, user_id: int) -> Optional[User]:
        query = select(User).where(User.id_user == user_id)
        result = self.session.execute(query).scalars().one_or_none()
        return result


@component
class ChatRepo(BaseRepository, interfaces.ChatRepo):
    def add_chat(self, chat: Chat):
        self.session.add(chat)
        self.session.flush()

    def get_by_chat_id(self, chat_id: int) -> Optional[Chat]:
        query = select(Chat).where(Chat.id_chat == chat_id)
        result = self.session.execute(query).scalars().one_or_none()
        return result

    def remove_chat(self, chat: Chat):
        members = self.session.query(MembersChat).where(MembersChat.id_chat == chat.id_chat).all()
        [self.session.delete(member) for member in self.session.query(MembersChat).where(
            MembersChat.id_chat == chat.id_chat).all()]
        self.session.commit()

        self.session.delete(chat)
        self.session.commit()

    def get_author_id(self, chat_id: int) -> Optional[int]:
        return select(Chat.author_of_chat).where(Chat.id_chat == chat_id)


@component
class MembersChatRepo(BaseRepository, interfaces.MembersChatRepo):
    def add_user(self, user: MembersChat):
        self.session.add(user)
        self.session.flush()

    def get_right_member(self, chat_id: int, user_id: int) -> Optional[MembersChat]:
        # query = select(MembersChat).filter(MembersChat.id_chat == chat_id, MembersChat.id_user == user_id)
        query = select(MembersChat).where(MembersChat.id_chat == chat_id, MembersChat.id_user == user_id)
        return self.session.execute(query).scalars().one_or_none()

    def get_chat_members(self, chat_id: int) -> Optional[List[MembersChat]]:
        return self.session.execute(select(MembersChat).where(MembersChat.id_chat == chat_id)).scalars().all()

    def leave_chat(self, member: MembersChat):
        self.session.delete(member)
        self.session.flush()


@component
class MessagesChatRepo(BaseRepository, interfaces.MessagesChatRepo):
    def send_message(self, message: MessagesChat):
        self.session.add(message)
        self.session.commit()

    def get_chat_messages(self, chat_id: int) -> Optional[List[MessagesChat]]:
        return self.session.execute(select(MessagesChat).where(MessagesChat.id_chat == chat_id)).scalars().all()
