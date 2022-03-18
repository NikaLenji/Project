import datetime
from typing import List, Optional

from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from pydantic import validate_arguments

from application import errors, interfaces
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
    id_chat: Optional[int]
    id_user: Optional[int]


class MessagesChatInfo(DTO):
    id_chat: Optional[int]
    id_user: Optional[int]
    text_message: Optional[str]


class ChatForChangeInfo(DTO):
    id_chat: int
    name_chat: Optional[str]
    description: Optional[str]
    author_of_chat: Optional[int]
    update_date: datetime.datetime = datetime.datetime.now()


@component
class Users:
    user_repo: interfaces.UserRepo

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        added_user = user_info.create_obj(User)
        self.user_repo.add_user(added_user)

    @join_point
    @validate_arguments
    def get_user(self, user_id: int) -> User:
        received_user = self.user_repo.get_by_user_id(user_id=user_id)
        if received_user is None:
            raise errors.NoUser(user_id=user_id)
        return received_user


@component
class Chats:
    chats_repo: interfaces.ChatRepo
    members_chat_repo: interfaces.MembersChatRepo
    messages_chat_repo: interfaces.MessagesChatRepo

    def is_right_member(self, chat_id: int, user_id: int) -> Optional[MembersChat]:
        test_user = self.members_chat_repo.get_right_member(chat_id=chat_id, user_id=user_id)
        if test_user is None:
            raise errors.NoMember(user_id=user_id)
        return test_user

    def is_right_author(self, chat_id: int, user_id: int):
        chat = self.is_no_chat(chat_id=chat_id)
        if chat.author_of_chat != user_id:
            raise errors.NoAuthor(user_id=user_id)

    def is_no_chat(self, chat_id: int) -> Chat:
        received_chat = self.chats_repo.get_by_chat_id(chat_id=chat_id)
        if received_chat is None:
            raise errors.NoChat(chat_id=chat_id)
        return received_chat

    def is_no_member(self, chat_id: int, user_id: int):
        test_user = self.members_chat_repo.get_right_member(chat_id=chat_id, user_id=user_id)
        if test_user is None:
            raise errors.NoMember(user_id=user_id)

    @join_point
    @validate_with_dto
    def add_chat(self, chat_info: ChatInfo):
        added_chat = chat_info.create_obj(Chat)
        self.chats_repo.add_chat(added_chat)

        chat = self.chats_repo.get_by_chat_id(chat_id=added_chat.id_chat)
        member_chat = MembersChatInfo(id_chat=chat.id_chat, id_user=chat.author_of_chat).create_obj(MembersChat)
        self.members_chat_repo.add_user(member_chat)

    @join_point
    @validate_arguments
    def get_chat_by_id(self, chat_id: int, user_id: int) -> Chat:
        self.is_right_member(chat_id=chat_id, user_id=user_id)
        return self.is_no_chat(chat_id=chat_id)

    @join_point
    @validate_arguments
    def add_member(self, chat_id: int, author_id: int, new_user_id: int):
        self.is_right_author(chat_id=chat_id, user_id=author_id)
        member_chat = MembersChatInfo(id_chat=chat_id, id_user=new_user_id).create_obj(MembersChat)
        self.members_chat_repo.add_user(member_chat)

    @join_point
    @validate_with_dto
    def update_chat(self, chat_info: ChatForChangeInfo):
        chat = self.is_no_chat(chat_id=chat_info.id_chat)
        self.is_right_author(chat_id=chat_info.id_chat, user_id=chat_info.author_of_chat)
        chat_info.populate_obj(chat)

    @join_point
    @validate_arguments
    def delete_chat(self, chat_id: int, user_id: int):
        chat = self.is_no_chat(chat_id=chat_id)
        if chat.author_of_chat == user_id:
            self.chats_repo.remove_chat(chat)

    @join_point
    @validate_with_dto
    def send_message(self, message: MessagesChatInfo):
        self.is_right_member(chat_id=message.id_chat, user_id=message.id_user)
        added_message = message.create_obj(MessagesChat)
        self.messages_chat_repo.send_message(added_message)

    @join_point
    @validate_arguments
    def get_members_chat(self, chat_id: int, user_id: int) -> Optional[List[MembersChat]]:
        self.is_right_member(chat_id=chat_id, user_id=user_id)
        return self.members_chat_repo.get_chat_members(chat_id=chat_id)

    @join_point
    @validate_arguments
    def get_messages_chat(self, chat_id: int, user_id: int) -> Optional[List[MessagesChat]]:
        self.is_right_member(chat_id=chat_id, user_id=user_id)
        return self.messages_chat_repo.get_chat_messages(chat_id=chat_id)

    @join_point
    @validate_with_dto
    def leave_chat(self, member: MembersChatInfo):
        chat = self.is_no_chat(chat_id=member.id_chat)
        test_member = self.members_chat_repo.get_right_member(chat_id=member.id_chat, user_id=member.id_user)
        if test_member is None:
            raise errors.NoMember(user_id=member.id_user)
        if test_member.id_user == chat.author_of_chat:
            self.chats_repo.remove_chat(chat)
        self.members_chat_repo.leave_chat(test_member)
