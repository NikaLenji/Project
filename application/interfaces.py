from abc import ABC, abstractmethod
from typing import Optional, List

from application.dataclasses import User, Chat, MembersChat, MessagesChat


class UserRepo(ABC):
    @abstractmethod
    def check_user_login(self, user_login: str) -> User: pass

    @abstractmethod
    def add_user(self, user: User): pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[User]: pass


class ChatRepo(ABC):
    @abstractmethod
    def add_chat(self, data: Chat): pass

    @abstractmethod
    def get_by_chat_id(self, chat_id: int) -> Optional[Chat]: pass

    @abstractmethod
    def remove_chat(self, chat: Chat): pass

    @abstractmethod
    def get_author_id(self, chat_id: int) -> Optional[int]: pass


class MembersChatRepo(ABC):
    @abstractmethod
    def add_user(self, user: MembersChat): pass

    @abstractmethod
    def get_right_member(self, chat_id: int, user_id: int) -> Optional[MembersChat]: pass

    @abstractmethod
    def get_chat_members(self, chat_id: int) -> Optional[List[MembersChat]]: pass

    @abstractmethod
    def leave_chat(self, member: MembersChat): pass


class MessagesChatRepo(ABC):
    @abstractmethod
    def send_message(self, message: MessagesChat): pass

    @abstractmethod
    def get_chat_messages(self, chat_id: int) -> Optional[List[MessagesChat]]: pass
