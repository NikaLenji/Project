

from application import services
from classic.components import component
from adapters.chat_api.join_points import join_point
from falcon import Request, Response


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
        print(request.media)
        self.chats.add_chat(**request.media)

    # @join_point
    # def on_post_add_member(self, request: Request, response: Response):
    #     self.chats.
