
CREATE TABLE "User" (
	"id_user" SERIAL PRIMARY KEY,
	"name_user" varchar(100) UNIQUE CHECK ("name_user" != ''),
	"login" varchar(100) UNIQUE CHECK ("login" != ''),
	"password" varchar(100) UNIQUE CHECK ("password" != '')
);

CREATE TABLE "Chat" (
	"id_chat" SERIAL PRIMARY KEY,
	"name_chat" varchar(100) UNIQUE CHECK ("name_chat" != ''),
	"description" varchar(500),
	"author_of_chat" int,
	"creation_date" timestamp,
	"update_date" timestamp
);

CREATE TABLE "MessagesChat" (
	"id_chat" int PRIMARY KEY,
	"id_user" int,
	"text_message" varchar,
	"date_message" timestamp
);

CREATE TABLE "MembersChat" (
	"id_chat" int PRIMARY KEY,
	"id_user" int,
	"alive" bool DEFAULT TRUE,
	"date_unlive" timestamp,
	"blocked" bool DEFAULT FALSE
);

ALTER TABLE "Chat" ADD FOREIGN KEY ("author_of_chat") REFERENCES "User" ("id_user");

ALTER TABLE "MembersChat" ADD FOREIGN KEY ("id_chat") REFERENCES "Chat" ("id_chat");

ALTER TABLE "MembersChat" ADD FOREIGN KEY ("id_user") REFERENCES "User" ("id_user");

ALTER TABLE "MessagesChat" ADD FOREIGN KEY ("id_chat") REFERENCES "Chat" ("id_chat");

ALTER TABLE "MessagesChat" ADD FOREIGN KEY ("id_user") REFERENCES "User" ("id_user");
