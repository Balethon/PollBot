from time import time

from balethon import Client
from balethon.conditions import regex, at_state, text, private, author
from balethon.objects import Message, CallbackQuery, User, ReplyKeyboardRemove
from balethon.dispatcher import MonitoringChain
from balethon.states import StateMachine

import config
import texts
import keyboards
from database import Database
from polls import Poll, QuizPoll
from chains import commands_chain, admins_chain, statistics_chain
from chains.commands_chain import help_

bot = Client(config.TOKEN)

incomplete_polls = {}

User.state_machine = StateMachine("user_states.db")


@bot.on_message(private & at_state(None) & regex("ایجاد نظرسنجی"))
async def create_poll(message: Message):
    message.author.set_state("POLL_TYPE")
    await message.reply(texts.select_poll_type, keyboards.poll_types)


@bot.on_message(private & at_state(None) & regex("نظرسنجی های من"))
async def my_polls(message: Message):
    polls = Database.get_polls(message.author.id)

    if not polls:
        return await message.reply(texts.no_polls)

    polls = texts.my_polls + "\n\n" + "\n\n".join(f"💠 * [{poll.type_name} - {poll.mode_name}) {poll.question}](send:/poll {poll.code}) *" for poll in polls)
    await message.reply(polls)


@bot.on_message(private & at_state(None) & regex("راهنمایی"))
async def guide(client: Client, message: Message):
    await help_(client=client, message=message)


@bot.on_message(private & at_state(None) & regex("پشتیبانی"))
async def support(message: Message):
    await message.reply(texts.support)


@bot.on_message(private & at_state(None) & regex("تعرفه تبلیغات"))
async def ads(message: Message):
    await message.reply_photo(config.ADS_FILE_ID, caption=texts.ads)


@bot.on_message(private & at_state(None) & regex("پنل ادمین ها") & author(*config.ADMINS))
async def admins_panel(message: Message):
    message.author.set_state("ADMINS_PANEL")
    await message.reply_document("users.db", texts.admins_panel, keyboards.admins_panel)


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

    if len(message.text) > 256:
        return await message.reply(texts.question_too_long)

    poll.question = " ".join(message.text.split())
    message.author.set_state("OPTIONS")
    await message.reply(texts.give_first_option)


@bot.on_message(private & at_state("OPTIONS") & text)
async def options(client: Client, message: Message):
    poll = incomplete_polls[message.author.id]

    if len(message.text) > 64:
        return await message.reply(texts.option_too_long)

    if (len(poll.options) >= 2 and message.text == "تکمیل نظرسنجی ☑️") or len(poll.options) >= 9:
        if message.text != "تکمیل نظرسنجی ☑️":
            poll.add_option(message.text)

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
        reply_markup = keyboards.admin_start if message.author.id in config.ADMINS else keyboards.start
        await client.send_message(message.chat.id, f"https://ble.ir/VoterBot?start={poll.code}", reply_markup)
        message.author.del_state()
        return

    if len(poll.options) >= 1:
        poll.add_option(message.text)
        options = "\n".join(f"• _{option.text}_" for option in poll.options)
        await message.reply(texts.more_options.format(options=options), keyboards.complete_poll)
        return

    poll.add_option(message.text)
    await message.reply(texts.give_second_option)


@bot.on_message(private & at_state("EXPLANATION"))
async def explanation(client: Client, message: Message):
    poll = incomplete_polls[message.author.id]

    if len(message.text) > 128:
        return await message.reply(texts.explanation_too_long)

    poll.explanation = message.text
    poll.create_time = round(time())
    Database.save_poll(poll)

    await message.reply(str(poll), poll.to_inline_keyboard())
    await client.send_message(message.chat.id, texts.command_usage)
    await client.send_message(message.chat.id, f"/start {poll.code}")
    await client.send_message(message.chat.id, texts.link_usage)
    reply_markup = keyboards.admin_start if message.author.id in config.ADMINS else keyboards.start
    await client.send_message(message.chat.id, f"https://ble.ir/VoterBot?start={poll.code}", reply_markup)
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


@bot.on_callback_query(regex("^close"))
async def close(callback_query: CallbackQuery):
    _, code = callback_query.data.split(".")

    poll = Database.load_poll(code)

    poll.is_closed = True
    Database.save_poll(poll)

    await callback_query.message.edit_text(poll.to_info())


if __name__ == "__main__":
    bot.include(MonitoringChain(), commands_chain, admins_chain, statistics_chain)
    bot.run()
