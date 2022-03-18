from classic.app.errors import AppError


class NoUser(AppError):
    msg_template = "User with id '{user_id}' does not exist"
    code = 'user.no_chat'


class NoChat(AppError):
    msg_template = "Chat with id '{chat_id}' does not exist"
    code = 'chat.no_chat'


class NoMember(AppError):
    msg_template = "User with id '{user_id}' is not member of chat"
    code = 'chat.not_member'


class NoAuthor(AppError):
    msg_template = "User with id '{user_id}' is not creator of chat"
    code = 'chat.not_owner'
