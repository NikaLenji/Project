from wsgiref import simple_server

from classic.sql_storage import TransactionContext
from sqlalchemy import create_engine

from adapters import database, chat_api
from application import services


class Settings:
    db = database.Settings()
    chat_api = chat_api.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine, expire_on_commit=False)

    user_repo = database.repositories.UserRepo(context=context)
    chats_repo = database.repositories.ChatRepo(context=context)
    members_chat_repo = database.repositories.MembersChatRepo(context=context)
    messages_chat_repo = database.repositories.MessagesChatRepo(context=context)


class Application:
    users = services.Users(
        user_repo=DB.user_repo,
    )
    chats = services.Chats(
        chats_repo=DB.chats_repo,
        members_chat_repo=DB.members_chat_repo,
        messages_chat_repo=DB.messages_chat_repo,
    )

    is_dev_mode = Settings.chat_api.IS_DEV_MODE
    allow_origins = Settings.chat_api.ALLOW_ORIGINS


class Aspects:
    services.join_points.join(DB.context)
    chat_api.join_points.join(DB.context)


app = chat_api.create_app(
    is_dev_mode=Application.is_dev_mode,
    allow_origins=Application.allow_origins,
    users=Application.users,
    chats=Application.chats,
)

if __name__ == "__main__":
    with simple_server.make_server('', 8000, app=app) as server:
        server.serve_forever()
