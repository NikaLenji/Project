import pytest
from unittest.mock import Mock

from application import interfaces, dataclasses


@pytest.fixture(scope='function')
def users():
    return dataclasses.User(
        id_user=1,
        name_user='User3',
        login='login3',
        password='password3'
    )


@pytest.fixture(scope='function')
def chats():
    return dataclasses.Chat(
        id_chat=1,
        name_chat='TestChat',
        description='something',
        author_of_chat=1
    )


@pytest.fixture(scope='function')
def members():
    return dataclasses.MembersChat(
        id_chat=1,
        id_user=1
    )


@pytest.fixture(scope='function')
def message():
    return dataclasses.MessagesChat(
        id_chat=1,
        id_user=1,
        text_message='something'
    )


@pytest.fixture(scope='function')
def users_repo(users):
    users_repo = Mock(interfaces.UserRepo)
    users_repo.get_by_user_id = Mock(return_value=users)
    return users_repo


@pytest.fixture(scope='function')
def chats_repo(chats):
    chats_repo = Mock(interfaces.ChatRepo)
    chats_repo.get_by_chat_id = Mock(return_value=chats)
    return chats_repo


@pytest.fixture(scope='function')
def members_chat_repo(members):
    members_chat_repo = Mock(interfaces.MembersChatRepo)
    members_chat_repo.get_chat_members = Mock(return_value=members)
    return members_chat_repo


@pytest.fixture(scope='function')
def messages_chat_repo(message):
    messages_chat_repo = Mock(interfaces.MessagesChatRepo)
    messages_chat_repo.get_chat_messages = Mock(return_value=message)
    return messages_chat_repo
