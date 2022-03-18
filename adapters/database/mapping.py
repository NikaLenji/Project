from sqlalchemy.orm import registry

from application import dataclasses
from adapters.database import tables


mapper = registry()

mapper.map_imperatively(dataclasses.User, tables.users)
mapper.map_imperatively(dataclasses.Chat, tables.chats)
mapper.map_imperatively(dataclasses.MessagesChat, tables.messages_chat)
mapper.map_imperatively(dataclasses.MembersChat, tables.members_chat)
