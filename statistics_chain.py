from balethon.conditions import private, group, channel, regex
from balethon.objects import Message, CallbackQuery
from balethon.dispatcher import Chain

from database import Database

statistics_chain = Chain("statistics")


@statistics_chain.on_message(private)
def private_user(message: Message):
    Database.save_user(message.author, is_member=True)


@statistics_chain.on_message(group)
def group_user(message: Message):
    if message.chat.id not in Database.get_groups():
        Database.save_group(message.chat.id)


@statistics_chain.on_message(channel)
def group_user(message: Message):
    if message.chat.id not in Database.get_channels():
        Database.save_channel(message.chat.id)


@statistics_chain.on_callback_query(regex("^vote"))
def voter(callback_query: CallbackQuery):
    Database.save_user(callback_query.author, is_member=False)
