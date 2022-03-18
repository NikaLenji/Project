

from typing import List, Optional, Tuple

from pydantic import conint, validate_arguments
import datetime
from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component

from application import interfaces
from .dataclasses import User, Chat, MembersChat, MessagesChat

join_points = PointCut()
join_point = join_points.join_point


class UserInfo(DTO):
    name_user: str
    login: str
    password: str
    id_user: Optional[int]


class ChatInfo(DTO):
    author_of_chat: int
    name_chat: Optional[str]
    description: Optional[str]
    id_chat: Optional[int]
    creation_date: datetime.datetime = datetime.datetime.utcnow()


class MembersChatInfo(DTO):
    id_chat: int
    id_user: int


class MessagesChatInfo(DTO):
    id_chat: int
    id_user: int
    text_message: str
    date_message: datetime.datetime = None


class ChatForChangeInfo(DTO):
    id_chat: int
    name_user: str
    description: str
    author_of_chat: int
    creation_date: datetime.datetime
    update_date: datetime.datetime = datetime.datetime.now()


@component
class Users:
    user_repo: interfaces.UserRepo

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        added_user = user_info.create_obj(User)
        self.user_repo.registry_user(added_user)

    @join_point
    @validate_arguments
    def get_user(self, user_id: int) -> User:
        received_user = self.user_repo.get_by_user_id(user_id=user_id)
        if received_user is None:
            raise Exception
        return received_user


@component
class Chats:
    chats_repo: interfaces.ChatRepo
    members_chat_repo: interfaces.MembersChatRepo
    messages_chat_repo: interfaces.MessagesChatRepo

    @join_point
    @validate_with_dto
    def add_chat(self, chat_info: ChatInfo):
        added_chat = chat_info.create_obj(Chat)
        self.chats_repo.add_chat(added_chat)

    @join_point
    @validate_arguments
    def get_chat_by_id(self, chat_id: int) -> Chat:
        # test_id_user = self.members_chat_repo.get_right_member(chat_id=chat_id, user_id=user_id)
        # if test_id_user is None:
        #     raise Exception
        # else:
        received_chat = self.chats_repo.get_by_chat_id(chat_id=chat_id)
        if received_chat is None:
            raise Exception
        else:
            return received_chat

    # @join_point
    # @validate_with_dto
    # def add_member(self, chat_id: int, author_id: int, new_user_id: int): pass

    @join_point
    @validate_with_dto
    def update_chat(self, chat_info: ChatForChangeInfo):
        chat = self.chats_repo.get_by_chat_id(chat_id=chat_info.id_chat)
        test_id_author = self.chats_repo.get_author_id(chat_id=chat_info.id_chat)
        if test_id_author:
            chat_info.populate_obj(chat)

    @join_point
    @validate_arguments
    def delete_chat(self, chat_id: int, user_id: int):
        chat = self.chats_repo.get_by_chat_id(chat_id=chat_id)
        test_id_author = self.chats_repo.get_author_id(chat_id=chat_id)
        if test_id_author == user_id:
            self.chats_repo.remove_chat(chat)

    @join_point
    @validate_arguments
    def get_members_chat(self, chat_id: int, user_id: int) -> Optional[List[MembersChat]]: pass

    @join_point
    @validate_arguments
    def get_messages_chat(self, chat_id: int, user_id: int) -> Optional[List[MessagesChat]]: pass
