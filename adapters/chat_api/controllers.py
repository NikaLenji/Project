from classic.components import component
from falcon import Request, Response

from adapters.chat_api.join_points import join_point
from application import services


@component
class Users:
    users: services.Users

    @join_point
    def on_get_show_user(self, request: Request, response: Response):
        user = self.users.get_user(**request.params)
        response.media = {
            'name_user': user.name_user,
        }

    @join_point
    def on_post_add_user(self, request: Request, response: Response):
        self.users.add_user(**request.media)
        response.media = {'message': 'User added'}


@component
class Chats:
    chats: services.Chats

    @join_point
    def on_get_show_chat(self, request: Request, response: Response):
        chat = self.chats.get_chat_by_id(**request.params)
        response.media = {
            'name_chat': chat.name_chat,
            'description': chat.description,
            'author of chat': chat.author_of_chat,
        }

    @join_point
    def on_post_add_chat(self, request: Request, response: Response):
        self.chats.add_chat(**request.media)
        response.media = {'message': 'Chat added'}

    @join_point
    def on_post_add_member(self, request: Request, response: Response):
        self.chats.add_member(**request.media)
        response.media = {'message': 'Member in chat added'}

    @join_point
    def on_post_update_chat(self, request: Request, response: Response):
        self.chats.update_chat(**request.media)
        response.media = {'message': 'Chat was updated'}

    @join_point
    def on_get_members_chat(self, request: Request, response: Response):
        members = self.chats.get_members_chat(**request.params)
        response.media = [
            {
            'name_user': member.id_user
            } for member in members
        ]

    @join_point
    def on_post_send_message(self, request: Request, response: Response):
        self.chats.send_message(**request.media)
        response.media = {'message': 'Message sended'}

    @join_point
    def on_get_messages_chat(self, request: Request, response: Response):
        messages = self.chats.get_messages_chat(**request.params)
        response.media = [
            {
                'id_user': message.id_user,
                'text_message': message.text_message
            } for message in messages
        ]

    @join_point
    def on_post_leave_chat(self, request: Request, response: Response):
        self.chats.leave_chat(**request.media)

    @join_point
    def on_delete_delete_chat(self, request: Request, response: Response):
        self.chats.delete_chat(**request.params)
