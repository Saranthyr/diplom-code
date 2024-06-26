create database test;
create extension IF NOT EXISTS "uuid-ossp";

\c test;

CREATE TABLE "users" (
  "pk" serial PRIMARY KEY,
  "id" uuid UNIQUE,
  "username" varchar(64) UNIQUE,
  "password" varchar(512),
  "first_name" varchar(64),
  "last_name" varchar(64),
  "nickname" varchar(64) UNIQUE,
  "avatar" uuid,
  "header" uuid,
  "about" text,
  "created_at" timestamp default current_timestamp,
  "updated_at" timestamp default current_timestamp,
  "location" int default 1,
  "link_tg" varchar(128),
  "role" int,
  "rating" real default 0,
  "posts_total" int default 0,
  "active" bool default false,
  "notification_channel" int default 1
);

CREATE TABLE "posts" (
  "pk" serial PRIMARY KEY,
  "id" uuid UNIQUE,
  "region" int,
  "tourism_type" int,
  "name" varchar(128),
  "header" varchar(512),
  "body" text,
  "author" uuid,
  "created_at" timestamp default current_timestamp,
  "rating" double precision,
  "longitude" numeric(5,2),
  "latitude" numeric(5,2),
  "link" varchar(512),
  "draft" bool default true,
  "archived" bool default false,
  "approved" int default 1,
  "thumbnail" uuid
);

CREATE TABLE "post_attachments" (
  "post_id" uuid,
  "attachment" uuid,
  PRIMARY KEY ("post_id", "attachment")
);

CREATE TABLE "post_hashtags" (
  "post_id" uuid,
  "tag" int,
  PRIMARY KEY ("post_id", "tag")
);

CREATE TABLE "hashtags" (
    "id" SERIAL PRIMARY KEY,
    "name" varchar(64) UNIQUE
);

CREATE TABLE "files" (
  "pk" serial PRIMARY KEY,
  "id" uuid UNIQUE,
  "name" varchar(256),
  "content" json,
  "created_at" timestamp default current_timestamp
);

CREATE TABLE "regions" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(128) UNIQUE,
  "thumbnail" uuid,
  "longitude" numeric(5,2),
  "latitude" numeric(5,2),
  "description" text
);

CREATE TABLE "user_roles" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(64) UNIQUE
);

CREATE TABLE "tourism_types" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(64) UNIQUE,
  "photo" uuid
);

CREATE TABLE "post_rates" (
  "post_id" uuid,
  "user_id" uuid,
  "rating" numeric(2,1),
  PRIMARY KEY ("post_id", "user_id")
);

CREATE TABLE "region_photos" (
  "region_id" int,
  "photo_id" uuid,
  PRIMARY KEY ("region_id", "photo_id")
);

create table "user_telegram_chats" (
  "user_id" uuid PRIMARY key,
  "chat" int
);

ALTER TABLE "posts" ADD FOREIGN KEY ("region") REFERENCES "regions" ("id");

ALTER TABLE "posts" ADD FOREIGN KEY ("tourism_type") REFERENCES "tourism_types" ("id");

ALTER TABLE "posts" ADD FOREIGN KEY ("author") REFERENCES "users" ("id");

ALTER TABLE "posts" ADD FOREIGN KEY ("thumbnail") REFERENCES "files" ("id");

ALTER TABLE "post_rates" ADD FOREIGN KEY ("post_id") REFERENCES "posts" ("id");

ALTER TABLE "post_rates" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "post_attachments" ADD FOREIGN KEY ("post_id") REFERENCES "posts" ("id") on update cascade on delete cascade;

ALTER TABLE "post_attachments" ADD FOREIGN KEY ("attachment") REFERENCES "files" ("id") on update cascade on delete cascade;

ALTER TABLE "regions" ADD FOREIGN KEY ("thumbnail") REFERENCES "files" ("id") on update cascade on delete set null;

ALTER TABLE "region_photos" ADD FOREIGN KEY ("region_id") REFERENCES "regions" ("id") on update cascade on delete cascade;

ALTER TABLE "region_photos" ADD FOREIGN KEY ("photo_id") REFERENCES "files" ("id") on update cascade on delete cascade;

ALTER TABLE "users" ADD FOREIGN KEY ("avatar") REFERENCES "files" ("id") on update cascade on delete set null;

ALTER TABLE "users" ADD FOREIGN KEY ("header") REFERENCES "files" ("id")  on update cascade on delete set null;

ALTER TABLE "users" ADD FOREIGN KEY ("location") REFERENCES "regions" ("id");

ALTER TABLE "users" ADD FOREIGN KEY ("role") REFERENCES "user_roles" ("id");

ALTER TABLE "tourism_types" ADD FOREIGN KEY ("photo") REFERENCES "files" ("id") on update cascade on delete set null;

alter table "post_hashtags" add FOREIGN key ("post_id") REFERENCES "posts" ("id");

alter table "post_hashtags" add FOREIGN key ("tag") REFERENCES "hashtags" ("id");

alter table "user_telegram_chats" add FOREIGN key ("user_id") REFERENCES "users" ("id") on update cascade on delete cascade;

insert into "user_roles" (id, name) overriding system value values (1, 'Admin'), (2, 'Moderator'), (3, 'User');

insert into "tourism_types" (id, name) overriding system value values (1, 'Природный'), (2, 'Культурный'), (3, 'Исторический'), (4, 'Пляжный'), (5, 'Гастрономический'),  (6, 'Экстремальный'), (7, 'Религиозный'), (8, 'Авантюрный');

insert into "regions" (id, name, latitude, longitude) overriding system value values (1, 'Москва', 55.76, 37.62), (2, 'Петербург', 59.93, 30.34), (3, 'Крым', 45.04, 34.37), (4, 'Кавказ', 42.24, 43.97), (5, 'Урал', 56.52, 61.26), (6, 'Сибирь', 55.17, 73.89), (7, 'Байкал', 53.56, 108.17), (8, 'Камчатка', 53.41, 158.25), (9, 'Карелия', 61.92, 29.75), (10, 'Золотое кольцо', 57.99, 40.97);

insert into "users" (id, username, password, first_name, last_name, nickname, role, active) values ('b3d1f532-aef0-4417-b888-39557ae0cdaf', 'admin@f-42.ru', '$2b$12$T0fF7PyvxZB.YxfiTIkUL.ETG9lTQ7QFxTV8LDaksluzpqAll2VK.', 'Admin', 'Admin', 'admin', 1, true), ('a6e53530-5c3c-448f-bc71-a49dc173898a', 'moderator@f-42.ru', '$2b$12$t5I7w3S2X/1KWuCqgJCNEOH45rQftGZglsxPJO3raQCY9qk7JNEJ6', 'Moderator', 'Moderator', 'moderator', 2, true);

CREATE OR REPLACE FUNCTION posts_total()
returns trigger as $$
begin
if new.approved = 2 then
  update users
  set posts_total = posts_total + 1
  where id = new.author;
end if;
return NEW;
END;
$$ language plpgsql;

create trigger tr_posts_total
after update of approved on posts
for each row
execute FUNCTION posts_total();

CREATE OR REPLACE FUNCTION user_rating()
returns trigger as $$
begin
update users
set rating = (select avg(rating)::numeric(2,1) from posts where author = new.author)
where id = new.author;
return new;
end;
$$ language plpgsql;

create trigger tr_rating
after update of rating on posts
for each row
execute function user_rating();
