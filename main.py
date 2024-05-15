from time import time

from balethon import Client
from balethon.conditions import regex, at_state, text, private, group, channel
from balethon.objects import Message, CallbackQuery, User, ReplyKeyboardRemove
from balethon.states import StateMachine

import config
import texts
import keyboards
from database import Database
from polls import Poll, QuizPoll

bot = Client(config.TOKEN)

incomplete_polls = {}

User.state_machine = StateMachine("user_states.db")


@bot.on_message(private, chain="statistics")
def private_user(message: Message):
    Database.save_user(message.author, is_member=True)


@bot.on_message(group, chain="statistics")
def group_user(message: Message):
    if message.chat.id not in Database.get_groups():
        Database.save_group(message.chat.id)


@bot.on_message(channel, chain="statistics")
def group_user(message: Message):
    if message.chat.id not in Database.get_channels():
        Database.save_channel(message.chat.id)


@bot.on_callback_query(regex("^vote"), chain="statistics")
def voter(callback_query: CallbackQuery):
    Database.save_user(callback_query.author, is_member=False)


@bot.on_command()
async def start(poll_code=None, *, client: Client, message: Message):
    if poll_code is not None:
        poll = Database.load_poll(poll_code)
        if poll.creator != message.author.id and poll.is_anonymous:
            return
        await client.send_message(message.chat.id, str(poll), poll.to_inline_keyboard())

    elif message.chat.type == "private":
        await message.reply(texts.start.format(user=message.author), keyboards.start)
        if message.author.get_state():
            message.author.del_state()

    elif message.chat.type == "group":
        await message.reply(texts.start_group.format(user=message.author))


@bot.on_command()
async def help(topic=None, *, message: Message):
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


@bot.on_command(private)
async def poll(poll_code, *, message: Message):
    poll = Database.load_poll(poll_code)
    if poll.creator != message.author.id and (poll.is_anonymous or isinstance(poll, QuizPoll)) and message.author.id not in poll.voters:
        return
    await message.reply(poll.to_info())


@bot.on_message(private & regex("ایجاد نظرسنجی"))
async def create_poll(message: Message):
    message.author.set_state("POLL_TYPE")
    await message.reply(texts.select_poll_type, keyboards.poll_types)


@bot.on_message(private & regex("نظرسنجی های من"))
async def my_polls(message: Message):
    polls = Database.get_polls(message.author.id)

    if not polls:
        return await message.reply(texts.no_polls)

    polls = "\n\n".join(f"{poll.question}\n[/poll {poll.code}](send:/poll {poll.code})" for poll in polls)
    await message.reply(polls)


@bot.on_message(private & regex("راهنمایی"))
async def help_(message: Message):
    await help(message=message)


@bot.on_message(private & regex("پشتیبانی"))
async def support(message: Message):
    await message.reply(texts.support)


@bot.on_message(private & regex("تعرفه تبلیغات"))
async def ads(message: Message):
    await message.reply_photo(config.ADS_FILE_ID, caption=texts.ads)


@bot.on_message(private & at_state("POLL_TYPE") & regex("نظرسنجی عادی"))
async def default_poll(message: Message):
    incomplete_polls[message.author.id] = Poll.create_new("default_poll")
    incomplete_polls[message.author.id].creator = message.author.id
    message.author.set_state("POLL_MODE")
    await message.reply(texts.select_poll_mode, keyboards.poll_modes)


@bot.on_message(private & at_state("POLL_TYPE") & regex("نظرسنجی چند جوابی"))
async def multiple_answers_poll(message: Message):
    incomplete_polls[message.author.id] = Poll.create_new("multiple_answers_poll")
    incomplete_polls[message.author.id].creator = message.author.id
    message.author.set_state("POLL_MODE")
    await message.reply(texts.select_poll_mode, keyboards.poll_modes)


@bot.on_message(private & at_state("POLL_TYPE") & regex("نظرسنجی آزمون"))
async def quiz_poll(message: Message):
    incomplete_polls[message.author.id] = Poll.create_new("quiz_poll")
    incomplete_polls[message.author.id].creator = message.author.id
    message.author.set_state("POLL_MODE")
    await message.reply(texts.select_poll_mode, keyboards.poll_modes)


@bot.on_message(private & at_state("POLL_MODE") & regex("عمومی"))
async def public_poll(message: Message):
    incomplete_polls[message.author.id].is_anonymous = False
    message.author.set_state("QUESTION")
    await message.reply(texts.give_question, ReplyKeyboardRemove())


@bot.on_message(private & at_state("POLL_MODE") & regex("خصوصی"))
async def anonymous_poll(message: Message):
    incomplete_polls[message.author.id].is_anonymous = True
    message.author.set_state("QUESTION")
    await message.reply(texts.give_question, ReplyKeyboardRemove())


@bot.on_message(private & at_state("QUESTION") & text)
async def question(message: Message):
    poll = incomplete_polls[message.author.id]

    if len(message.text) > 255:
        return await message.reply(texts.question_too_long)

    poll.question = " ".join(message.text.split())
    message.author.set_state("OPTIONS")
    await message.reply(texts.give_first_option)


@bot.on_message(private & at_state("OPTIONS") & text)
async def options(client: Client, message: Message):
    poll = incomplete_polls[message.author.id]

    if len(message.text) > 70:
        return await message.reply(texts.option_too_long)

    if len(poll.options) >= 1:
        if message.text == "تکمیل نظرسنجی ☑️":
            if isinstance(poll, QuizPoll):
                message.author.set_state("SELECTING_CORRECT_OPTION")
                await message.reply(texts.select_correct_option, ReplyKeyboardRemove())
                await message.reply("گزینه ها", poll.to_inline_keyboard("correct"))
                return

            poll.create_time = round(time())
            Database.save_poll(poll)

            await message.reply(str(poll), poll.to_inline_keyboard())
            await client.send_message(message.chat.id, texts.command_usage)
            await client.send_message(message.chat.id, f"/start {poll.code}")
            await client.send_message(message.chat.id, texts.link_usage)
            await client.send_message(message.chat.id, f"https://ble.ir/VoterBot?start={poll.code}", keyboards.start)
            message.author.del_state()
            return

        poll.add_option(message.text)
        options = "\n".join(f"• _{option.text}_" for option in poll.options)
        await message.reply(texts.more_options.format(options=options), keyboards.complete_poll)
        return

    poll.add_option(message.text)

    await message.reply(texts.give_second_option)


@bot.on_message(private & at_state("EXPLANATION"))
async def explanation(client: Client, message: Message):
    poll = incomplete_polls[message.author.id]

    poll.explanation = message.text
    poll.create_time = round(time())
    Database.save_poll(poll)

    await message.reply(str(poll), poll.to_inline_keyboard())
    await client.send_message(message.chat.id, texts.command_usage)
    await client.send_message(message.chat.id, f"/start {poll.code}")
    await client.send_message(message.chat.id, texts.link_usage)
    await client.send_message(message.chat.id, f"https://ble.ir/VoterBot?start={poll.code}", keyboards.start)
    message.author.del_state()


@bot.on_callback_query(private & regex("^correct") & at_state("SELECTING_CORRECT_OPTION"))
async def correct(callback_query: CallbackQuery):
    poll = incomplete_polls[callback_query.author.id]

    _, __, option_index = callback_query.data.split(".")
    option_index = int(option_index)

    poll.correct_option = option_index

    callback_query.author.set_state("EXPLANATION")
    await callback_query.message.edit_text(texts.give_explanation)


@bot.on_callback_query(regex("^vote"))
async def vote(callback_query: CallbackQuery):
    _, code, option_index = callback_query.data.split(".")
    option_index = int(option_index)

    poll = Database.load_poll(code)

    poll.vote(callback_query.author.id, option_index)
    Database.save_poll(poll)

    await callback_query.message.edit_text(str(poll), poll.to_inline_keyboard())


if __name__ == "__main__":
    bot.run()
