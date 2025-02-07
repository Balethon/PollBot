from balethon import Client
from balethon.dispatcher import Chain
from balethon.conditions import private, at_state, regex
from balethon.objects import Message

import texts
from database import Database
from commands_chain import start

admins_chain = Chain(__name__, condition=private)


@admins_chain.on_message(at_state("ADMINS_PANEL") & regex("فوروارد به پیوی ها"))
async def private_forward(message: Message):
    message.author.set_state("GIVE_PRIVATE_FORWARD_MESSAGE")
    await message.reply(texts.give_message)


@admins_chain.on_message(at_state("GIVE_PRIVATE_FORWARD_MESSAGE"))
async def private_forward(message: Message):
    users = Database.load_users()

    await message.reply(texts.sending_started)

    count = 0

    for user in users:
        try:
            await message.forward(user.id)
        except Exception as e:
            print(e)
        else:
            count += 1
            print(f"{user.id} Successful")

    message.author.del_state()
    await message.reply(texts.sending_finished.format(success_count=count))


@admins_chain.on_message(at_state("ADMINS_PANEL") & regex("فوروارد به گروه ها"))
async def group_forward(message: Message):
    message.author.set_state("GIVE_GROUP_FORWARD_MESSAGE")
    await message.reply(texts.give_message)


@admins_chain.on_message(at_state("GIVE_GROUP_FORWARD_MESSAGE"))
async def private_forward(client: Client, message: Message):
    groups = Database.get_groups()

    await message.reply(texts.sending_started)

    count = 0

    for group_id in groups:
        try:
            group = await client.get_chat(group_id)
            if group.type != "group":
                continue
            await message.forward(group_id)
        except Exception as e:
            print(e)
        else:
            count += 1
            print(f"{group_id} Successful")

    message.author.del_state()
    await message.reply(texts.sending_finished.format(success_count=count))


@admins_chain.on_message(at_state("ADMINS_PANEL") & regex("آمار"))
async def statistics(message: Message):
    users = Database.load_users()
    polls = Database.get_polls()
    groups = Database.get_groups()
    channels = Database.get_channels()
    await message.reply(
        texts.statistics.format(
            polls=len(polls),
            users=len(users),
            members=len([user for user in users if user["signup_time"]]),
            groups=len(groups),
            channels=len(channels)
        )
    )


@admins_chain.on_message(at_state("ADMINS_PANEL") & regex("برگشت 🔙"))
async def back(client: Client, message: Message):
    await start(client=client, message=message)
