from balethon import Client
from balethon.conditions import regex, at_state, text, private
from balethon.objects import Message, CallbackQuery, User, InlineKeyboard
from balethon.event_handlers import MessageHandler
from balethon.states import StateMachine

import config
import texts
import keyboards
from polls import Poll, QuizPoll, MultipleAnswersPoll
from database import test

bot = Client(config.TOKEN)
incomplete_polls = {}

User.state_machine = StateMachine("user_states.db")


class UserHandler(MessageHandler):
    async def __call__(self, client, event):
        poll = incomplete_polls[event.author.id]
        return await super().__call__(client=client, message=event, poll=poll)


def create_keyboard_poll_options(poll, prefix="vote"):
    keyboard = InlineKeyboard()
    for index, option in enumerate(poll.options):
        keyboard.add_row((option, f"{prefix}.{poll.code}.{index}"))
    return keyboard


async def complete_poll(event):
    poll = incomplete_polls[event.author.id]
    chat_id = event.chat_instance or event.chat.id
    await bot.send_message(chat_id, str(poll), create_keyboard_poll_options(poll))


@bot.on_command()
async def start(*, message: Message):
    await message.reply(texts.start.format(user=message.author), keyboards.start)


@bot.on_callback_query(regex("^create_poll$"))
async def create_poll(callback_query: CallbackQuery):
    await callback_query.answer(texts.poll_types, keyboards.poll_types)


@bot.on_callback_query(regex("simple_poll|multiple_answers_poll|quiz_poll"))
async def poll_types(callback_query: CallbackQuery):
    await callback_query.message.edit_text(texts.poll_modes, keyboards.poll_modes)
    incomplete_polls[callback_query.author.id] = Poll.create(callback_query.data)
    callback_query.author.set_state("MODE")


@bot.on_callback_query(at_state("MODE") & regex("public|anonymous"))
async def poll_modes(callback_query: CallbackQuery):
    mode = True if callback_query.data == "anonymous" else False
    incomplete_polls[callback_query.author.id].is_anonymous = mode
    await callback_query.message.edit_text(texts.question, keyboards.cancel)
    callback_query.author.set_state("QUESTION")


@bot.add_event_handler(
    UserHandler,
    condition=at_state("QUESTION") & text #& private
)
async def question(message: Message, poll):
    if len(message.text) > 255:
        return await message.reply(texts.question_limitation)
    poll.question = message.text
    await message.reply(texts.first_option)
    
    message.author.set_state("OPTIONS")


@bot.add_event_handler(
    UserHandler,
    condition=at_state("OPTIONS") & text #& private
)
async def options(message: Message, poll):
    if len(message.text) > 70:
        return await message.reply(texts.option_limitation)
    poll.options.append(message.text)

    if len(poll.options) >= 2:
        options = "\n".join(f"• _{option}_" for option in poll.options)
        await message.reply(texts.other_options.format(options=options), keyboards.complete_poll)
        message.author.set_state("SELECTING")
        return  # await message.delete()

    await message.reply(texts.second_option)


@bot.on_callback_query(at_state("SELECTING") & regex("^new_option$"))
async def new_option(callback_query: CallbackQuery):
    await callback_query.message.edit_text(texts.new_option)
    callback_query.author.set_state("OPTIONS")


@bot.on_callback_query(at_state("SELECTING") & regex("^complete_poll$"))
async def complete(callback_query: CallbackQuery):
    poll = incomplete_polls[callback_query.author.id]
    if poll.type == "quiz" and poll.correct_option is None:
        await callback_query.answer(texts.select_correct_option, create_keyboard_poll_options(poll, "correct"))
        return 
    await complete_poll(callback_query)
    callback_query.author.del_state()


@bot.on_callback_query(regex("^cancel$") & ~at_state(None))
async def cancel(callback_query: CallbackQuery):
    callback_query.author.del_state()
    await callback_query.message.delete()


if __name__ == "__main__":
    bot.run()
