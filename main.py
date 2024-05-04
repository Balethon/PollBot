from balethon import Client
from balethon.conditions import regex, at_state, text
from balethon.objects import Message, CallbackQuery, User
from balethon.states import StateMachine

import config
import texts
import keyboards
from polls import Poll

bot = Client(config.TOKEN)

incomplete_polls = {}

User.state_machine = StateMachine("user_states.db")


@bot.on_command()
async def start(*, message: Message):
    await message.reply(texts.start.format(user=message.author), keyboards.start)


@bot.on_callback_query(regex("^create_poll$"))
async def create_poll(callback_query: CallbackQuery):
    await callback_query.answer(texts.select_poll_type, keyboards.poll_types)


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
        return  # await message.delete()

    await message.reply(texts.give_second_option)


@bot.on_callback_query(at_state("SELECTING") & regex("^new_option$"))
async def new_option(callback_query: CallbackQuery):
    await callback_query.message.edit_text(texts.give_new_option)
    callback_query.author.set_state("OPTIONS")


@bot.on_callback_query(at_state("SELECTING") & regex("^complete_poll$"))
async def complete(callback_query: CallbackQuery):
    poll = incomplete_polls[callback_query.author.id]

    if poll.type == "quiz" and poll.correct_option is None:
        await callback_query.answer(texts.select_correct_option, poll.to_inline_keyboard("correct"))
        return

    await callback_query.answer(str(poll), poll.to_inline_keyboard())
    callback_query.author.del_state()


@bot.on_callback_query(regex("^cancel$") & ~at_state(None))
async def cancel(callback_query: CallbackQuery):
    callback_query.author.del_state()
    await callback_query.message.delete()


if __name__ == "__main__":
    bot.run()
