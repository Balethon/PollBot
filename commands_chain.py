from balethon import Client
from balethon.dispatcher import Chain
from balethon.conditions import private
from balethon.objects import Message, InlineKeyboard

import config
import texts
import keyboards
from database import Database
from polls import QuizPoll

commands_chain = Chain(__name__)


@commands_chain.on_command()
async def start(poll_code=None, *, client: Client, message: Message):
    if poll_code is not None:
        poll = Database.load_poll(poll_code)
        if poll.creator != message.author.id and poll.is_anonymous:
            return
        await client.send_message(message.chat.id, str(poll), poll.to_inline_keyboard())

    elif message.chat.type == "private":
        reply_markup = keyboards.admin_start if message.author.id in config.ADMINS else keyboards.start
        await message.reply(texts.start.format(user=message.author), reply_markup)
        if message.author.get_state():
            message.author.del_state()

    elif message.chat.type == "group":
        await message.reply(texts.start_group.format(user=message.author))


@commands_chain.on_command(name="help")
async def help_(topic=None, *, message: Message):
    if topic is None:
        await message.reply(texts.help)
    elif topic == "invite_to_chat":
        await message.reply_video(config.INVITE_TO_CHAT_FILE_ID, caption=texts.invite_to_chat)
    elif topic == "poll_types":
        await message.reply(texts.poll_types)
    elif topic == "poll_modes":
        await message.reply(texts.poll_modes)
    elif topic == "create_poll":
        await message.reply_video(config.CREATE_POLL_FILE_ID, caption=texts.create_poll)
    elif topic == "access":
        await message.reply_photo(config.ACCESS_FILE_ID, caption=texts.access)
    elif topic == "poll_link":
        await message.reply(texts.poll_link)
    elif topic == "limitations":
        await message.reply(texts.limitations)


@commands_chain.on_command(private)
async def poll(poll_code, *, message: Message):
    poll = Database.load_poll(poll_code)

    if poll.creator != message.author.id and (poll.is_anonymous or isinstance(poll, QuizPoll)) and message.author.id not in poll.voters:
        return

    if poll.creator == message.author.id and not poll.is_closed:
        reply_markup = InlineKeyboard([("متوقف کردن نظرسنجی", f"close.{poll.code}")])
    else:
        reply_markup = None

    await message.reply(poll.to_info(), reply_markup)
