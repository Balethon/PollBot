from json import load, dump
from os import path
from sqlite3 import connect
from time import time

from balethon.objects import User

from polls import Poll

__path__ = path.dirname(__file__)

with open(path.join(__path__, "polls.json"), encoding="utf-8") as polls_json:
    polls = load(polls_json)

with open(path.join(__path__, "groups.json"), encoding="utf-8") as f:
    groups = load(f)

with open(path.join(__path__, "channels.json"), encoding="utf-8") as f:
    channels = load(f)


class Database:
    connection = connect("users.db", check_same_thread=False)

    @classmethod
    def create_table(cls):
        sql = """CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, first_name TEXT, signup_time INTEGER)"""
        cursor = cls.connection.cursor()
        cursor.execute(sql)
        cls.connection.commit()

    @staticmethod
    def get_polls(user_id):
        user_polls = []
        for poll in polls.values():
            if poll["creator"] == user_id:
                user_polls.append(Poll.create(**poll))
        return user_polls

    @staticmethod
    def save_poll(poll):
        polls[poll.code] = poll.to_dict()
        with open(f"{__path__}/polls.json", "w") as polls_json:
            dump(polls, polls_json, indent=4)

    @staticmethod
    def load_poll(code):
        return Poll.create(**polls[code])

    @classmethod
    def insert_user(cls, user, is_member):
        sql = """INSERT INTO users VALUES (?, ?, ?)"""
        cursor = cls.connection.cursor()
        signup_time = round(time()) if is_member else None
        cursor.execute(sql, (user.id, user.first_name, signup_time))
        cls.connection.commit()

    @classmethod
    def update_user(cls, user):
        sql = """UPDATE users SET first_name = ? WHERE user_id = ?"""
        cursor = cls.connection.cursor()
        cursor.execute(sql, (user.first_name, user.id))
        cls.connection.commit()

    @classmethod
    def save_user(cls, user, is_member):
        result = cls.select_user(user.id)
        if result is None:
            cls.insert_user(user, is_member)
        else:
            cls.update_user(user)

    @classmethod
    def select_user(cls, user_id):
        sql = """SELECT * FROM users WHERE user_id = ?"""
        cursor = cls.connection.cursor()
        cursor.execute(sql, (user_id,))
        return cursor.fetchone()

    @classmethod
    def select_users(cls, user_ids):
        sql = f"""SELECT * FROM users WHERE user_id in ({", ".join(map(str, user_ids))})"""
        cursor = cls.connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def load_user(cls, user_id):
        user = cls.select_user(user_id)
        if user is None:
            return User(user_id)
        return User(id=user[0], first_name=user[1], signup_time=user[2])

    @classmethod
    def load_users(cls, user_ids):
        result = cls.select_users(user_ids)
        result = [User(id=user[0], first_name=user[1], signup_time=user[2]) for user in result]
        return result

    @staticmethod
    def get_groups():
        return groups

    @staticmethod
    def save_group(group):
        groups.append(group)
        with open(f"{__path__}/groups.json", "w") as f:
            dump(groups, f, indent=4)

    @staticmethod
    def get_channels():
        return channels

    @staticmethod
    def save_channel(channel):
        channels.append(channel)
        with open(f"{__path__}/channels.json", "w") as f:
            dump(channels, f, indent=4)


Database.create_table()
