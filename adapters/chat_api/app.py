

from classic.http_api import App
from application import services
from adapters.chat_api import controllers


def create_app(
        users: services.Users,
        chats: services.Chats) -> App:

    app = App(prefix='/api')
    app.register(controllers.Users(users=users))
    app.register(controllers.Chats(chats=chats))

    return app
