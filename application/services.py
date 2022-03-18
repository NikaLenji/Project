

from typing import List, Optional, Tuple

from pydantic import conint, validate_arguments
import datetime
from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component

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
            raise errors.NoUser(user_id=user_id)
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

        chat = self.chats_repo.get_by_chat_id(chat_id=added_chat.id_chat)
        member_chat = MembersChatInfo(id_chat=chat.id_chat, id_user=chat.author_of_chat).create_obj(MembersChat)
        self.members_chat_repo.add_user(member_chat)


    @join_point
    @validate_arguments
    def get_chat_by_id(self, chat_id: int, user_id: int) -> Chat:
        test_id_user = self.members_chat_repo.get_right_member(chat_id=chat_id, user_id=user_id)
        if test_id_user is None:
            raise errors.NoMember(user_id=test_id_user)
        else:
            received_chat = self.chats_repo.get_by_chat_id(chat_id=chat_id)
            if received_chat is None:
                raise errors.NoChat
            else:
                return received_chat

    @join_point
    @validate_arguments()
    def add_member(self, chat_id: int, author_id: int, new_user_id: int):
        chat = self.chats_repo.get_by_chat_id(chat_id=chat_id)
        if chat.author_of_chat != author_id:
            raise errors.NoAuthor(user_id=author_id)
        else:
            member_chat = MembersChatInfo(id_chat=chat_id, id_user=new_user_id).create_obj(MembersChat)
            self.members_chat_repo.add_user(member_chat)


    @join_point
    @validate_with_dto
    def update_chat(self, chat_info: ChatForChangeInfo):
        chat = self.chats_repo.get_by_chat_id(chat_id=chat_info.id_chat)
        if chat is None:
            raise errors.NoChat(chat_id=chat_info.id_chat)
        else:
            test_id_author = self.chats_repo.get_author_id(chat_id=chat_info.id_chat)
            if test_id_author == chat.author_of_chat:
                chat_info.populate_obj(chat)
            else:
                raise errors.NoAuthor(user_id=test_id_author)

    @join_point
    @validate_arguments
    def delete_chat(self, chat_id: int, user_id: int):
        chat = self.chats_repo.get_by_chat_id(chat_id=chat_id)
        if chat is None:
            raise errors.NoChat(chat_id=chat_id)
        else:
            test_id_author = self.chats_repo.get_author_id(chat_id=chat_id)
            if test_id_author == user_id:
                self.chats_repo.remove_chat(chat)
            else:
                raise errors.NoAuthor(user_id=user_id)

    @join_point
    @validate_with_dto
    def send_message(self, message: MessagesChatInfo): pass

    @join_point
    @validate_arguments
    def get_members_chat(self, chat_id: int, user_id: int) -> Optional[List[MembersChat]]: pass

    @join_point
    @validate_arguments
    def get_messages_chat(self, chat_id: int, user_id: int) -> Optional[List[MessagesChat]]: pass

    @join_point
    @validate_with_dto
    def leave_chat(self, member: MembersChatInfo):
        chat = self.chats_repo.get_by_chat_id(chat_id=member.id_chat)
        if chat is None:
            raise errors.NoChat(chat_id=member.id_chat)
        else:
            test_member = self.members_chat_repo.get_right_member(chat_id=member.id_chat, user_id=member.id_user)
            if test_member is None:
                raise errors.NoMember(user_id=member.id_user)
            else:
                member_leave = member.create_obj(MembersChat)
                self.members_chat_repo.leave_chat(member_leave)
