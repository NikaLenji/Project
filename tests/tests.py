import pytest
from attr import asdict

from application import services, errors


@pytest.fixture(scope='function')
def service_user(users_repo):
    return services.Users(user_repo=users_repo)


@pytest.fixture(scope='function')
def service_chat(chats_repo, members_chat_repo, messages_chat_repo):
    return services.Chats(chats_repo=chats_repo,
                          members_chat_repo=members_chat_repo,
                          messages_chat_repo=messages_chat_repo)


data_user = {
    'id_user': 1,
    'name_user': 'User3',
    'login': 'login3',
    'password': 'password3'
}

data_user1 = {
    'id_user': 2,
    'name_user': 'User2',
    'login': 'login2',
    'password': 'password2'
}

data_chat = {
    'id_chat': 1,
    'name_chat': 'TestChat',
    'description': 'something',
    'author_of_chat': 1,
}

data_member = {
    'id_chat': 1,
    'id_user': 2
}

data_chat_update = {
    'id_chat': 1,
    'author_of_chat': 1,
    'name_chat': 'TrueTestChat',
}

message = {
    'id_chat': 1,
    'id_user': 1,
    'text_message': 'something'
}

get_message = {
    'id_chat': 1,
    'id_user': 1,
    'text_message': 'something'
}

get_members = {
    'id_chat': 1,
    'id_user': 1
}


def test_add_user(service_user):
    with pytest.raises(errors.UserAlreadyExist):
        service_user.add_user(**data_user)


def test_get_user(service_user):
    user = service_user.get_user(user_id=data_user['id_user'])
    assert asdict(user) == data_user


def test_add_chat(service_chat):
    service_chat.add_chat(**data_chat)
    service_chat.chats_repo.add_chat.assert_called_once()


def test_get_chat_by_id(service_chat):
    chat = service_chat.get_chat_by_id(chat_id=data_chat['id_chat'], user_id=data_user['id_user'])
    assert asdict(chat) == data_chat


def test_add_member(service_chat):
    service_chat.add_member(
        chat_id=data_chat['id_chat'],
        author_id=data_user['id_user'],
        new_user_id=data_member['id_user'])
    service_chat.members_chat_repo.add_user.assert_called()


def test_update_chat(service_chat):
    service_chat.update_chat(**data_chat_update)
    # service_chat.update_chat.assert_called_once()


def test_delete_chat(service_chat):
    service_chat.delete_chat(chat_id=data_chat['id_chat'], user_id=data_user['id_user'])
    service_chat.chats_repo.remove_chat.assert_called_once()


def test_send_message(service_chat):
    service_chat.send_message(**message)
    service_chat.messages_chat_repo.send_message.assert_called_once()


def test_leave_chat(service_chat):
    service_chat.leave_chat(**data_member)
    service_chat.members_chat_repo.leave_chat.assert_called_once()


def test_get_chat_members(service_chat):
    members = service_chat.get_members_chat(
        chat_id=data_chat['id_chat'], user_id=data_user['id_user'])
    assert asdict(members) == get_members


def test_get_chat_messages(service_chat):
    messages = service_chat.get_messages_chat(
        chat_id=data_chat['id_chat'], user_id=data_user['id_user'])
    assert asdict(messages) == get_message
