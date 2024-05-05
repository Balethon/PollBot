from balethon import Client
from balethon.conditions import regex, at_state, text
from balethon.objects import Message, CallbackQuery, User
from balethon.states import StateMachine

import config
import texts
import keyboards
from database import Database
from polls import Poll, QuizPoll

bot = Client(config.TOKEN)

incomplete_polls = {}

User.state_machine = StateMachine("user_states.db")


@bot.on_command()
async def start(*, message: Message):
    await message.reply(texts.start.format(user=message.author), keyboards.start)


@bot.on_command()
async def start(poll_code, *, message: Message):
    poll = Database.load_poll(poll_code)
    await message.reply(str(poll), poll.to_inline_keyboard())


@bot.on_command()
async def help(topic=None, *, message: Message):
    if topic == "invite_to_chat":
        await message.reply_video(config.INVITE_TO_CHAT_FILE_ID, caption=texts.invite_to_chat)
    elif topic == "create_poll":
        await message.reply_video(config.CREATE_POLL_FILE_ID, caption=texts.create_poll)
    elif topic == "access":
        await message.reply_photo(config.ACCESS_FILE_ID, caption=texts.access)
    elif topic == "poll_link":
        await message.reply(texts.poll_link)
    elif topic == "limitations":
        await message.reply(texts.limitations)


@bot.on_callback_query(regex("^create_poll$"))
async def create_poll(callback_query: CallbackQuery):
    await callback_query.answer(texts.select_poll_type, keyboards.poll_types)


@bot.on_callback_query(regex("^help$"))
async def help(callback_query: CallbackQuery):
    await callback_query.answer(texts.help)


@bot.on_callback_query(regex("^support$"))
async def support(callback_query: CallbackQuery):
    await callback_query.answer(texts.support)


@bot.on_callback_query(regex("^ads$"))
async def ads(callback_query: CallbackQuery):
    await callback_query.answer(texts.ads)


@bot.on_callback_query(regex("default_poll|multiple_answers_poll|quiz_poll"))
async def poll_types(callback_query: CallbackQuery):
    await callback_query.message.edit_text(texts.select_poll_mode, keyboards.poll_modes)
    incomplete_polls[callback_query.author.id] = Poll.create_new(callback_query.data)
    callback_query.author.set_state("MODE")


@bot.on_callback_query(at_state("MODE") & regex("public|anonymous"))
async def poll_modes(callback_query: CallbackQuery):
    mode = True if callback_query.data == "anonymous" else False
    incomplete_polls[callback_query.author.id].is_anonymous = mode
    await callback_query.message.edit_text(texts.give_question, keyboards.cancel)
    callback_query.author.set_state("QUESTION")


@bot.on_message(at_state("QUESTION") & text)
async def question(message: Message):
    poll = incomplete_polls[message.author.id]

    if len(message.text) > 255:
        return await message.reply(texts.question_too_long)

    poll.question = " ".join(message.text.split())
    await message.reply(texts.give_first_option)

    message.author.set_state("OPTIONS")


@bot.on_message(condition=at_state("OPTIONS") & text)
async def options(message: Message):
    poll = incomplete_polls[message.author.id]

    if len(message.text) > 70:
        return await message.reply(texts.option_too_long)

    poll.add_option(message.text)

    if len(poll.options) >= 2:
        options = "\n".join(f"• _{option.text}_" for option in poll.options)
        await message.reply(texts.more_options.format(options=options), keyboards.complete_poll)
        message.author.set_state("SELECTING")
        return

    await message.reply(texts.give_second_option)


@bot.on_callback_query(at_state("SELECTING") & regex("^new_option$"))
async def new_option(callback_query: CallbackQuery):
    await callback_query.message.edit_text(texts.give_new_option)
    callback_query.author.set_state("OPTIONS")


@bot.on_callback_query(at_state("SELECTING") & regex("^complete_poll$"))
async def complete(callback_query: CallbackQuery):
    poll = incomplete_polls[callback_query.author.id]

    if isinstance(poll, QuizPoll) and poll.correct_option is None:
        await callback_query.answer(texts.select_correct_option, poll.to_inline_keyboard("correct"))
        return

    Database.save_poll(poll)

    await callback_query.message.edit_text(str(poll), poll.to_inline_keyboard())
    callback_query.author.del_state()


@bot.on_callback_query(regex("^cancel$") & ~at_state(None))
async def cancel(callback_query: CallbackQuery):
    callback_query.author.del_state()
    await callback_query.message.delete()


@bot.on_callback_query(regex("^correct"))
async def vote(callback_query: CallbackQuery):
    poll = incomplete_polls[callback_query.author.id]

    _, __, option_index = callback_query.data.split(".")
    option_index = int(option_index)

    poll.correct_option = option_index
    Database.save_poll(poll)

    await callback_query.message.edit_text(str(poll), poll.to_inline_keyboard())
    callback_query.author.del_state()


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
