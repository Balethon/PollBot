from secrets import token_hex
from time import time
from copy import deepcopy

from balethon.objects import InlineKeyboard

from .option import Option
import texts


class Poll:
    type = "default_poll"
    type_name = texts.default_poll

    @staticmethod
    def generate_code():
        return token_hex(5)

    @staticmethod
    def get_time():
        return round(time())

    @classmethod
    def create(cls, type, *args, **kwargs):
        if type == cls.type:
            return cls(*args, **kwargs)
        for subclass in cls.__subclasses__():
            if subclass.type == type:
                return subclass(*args, **kwargs)

    @classmethod
    def create_new(cls, type):
        return cls.create(
            type,
            question="",
            options=[],
            code=cls.generate_code(),
            creator="",
            is_closed=False,
            is_anonymous=False,
            create_time=cls.get_time()
        )

    @property
    def voters(self):
        voters = []
        for option in self.options:
            voters.extend(option.voters)
        return voters

    @property
    def votes_count(self):
        return len(self.voters)

    def __init__(
            self,
            question: str,
            options: list,
            code: str,
            creator: str,
            is_closed: bool,
            is_anonymous: int,
            create_time: int,
    ):
        self.type = self.type
        self.question = " ".join(question.split())
        self.options = [option if isinstance(option, Option) else Option(**option) for option in options]
        self.code = code
        self.creator = creator
        self.is_closed = is_closed 
        self.is_anonymous = is_anonymous
        self.create_time = create_time

    def add_option(self, text):
        self.options.append(Option(text))

    def get_option_percentage(self, index):
        option = self.options[index]
        try:
            return round((option.voters_count / self.votes_count) * 100)
        except ZeroDivisionError:
            return 0

    def __str__(self):
        options = "\n\n".join(option.to_poll(i + 1, self.get_option_percentage(i)) for i, option in enumerate(self.options))
        return texts.poll.format(
            question=self.question,
            options=options,
            votes_count=self.votes_count,
            type_name=self.type_name,
            code=self.code
        )

    def vote(self, user_id, option_index):
        if self.is_closed:
            return None
        option = self.options[option_index]
        if user_id in option.voters:
            option.voters.remove(user_id)
            return False
        if user_id in self.voters:
            self.get_vote(user_id).voters.remove(user_id)
        option.voters.append(user_id)
        return True

    def get_vote(self, user_id):
        for option in self.options:
            if user_id in option.voters:
                return option

    def to_inline_keyboard(self, prefix="vote"):
        inline_keyboard = InlineKeyboard()
        for i, option in enumerate(self.options):
            inline_keyboard.add_row((option.text, f"{prefix}.{self.code}.{i}"))
        return inline_keyboard

    def to_dict(self):
        poll = deepcopy(self)
        poll.options = [option.to_dict() for option in poll.options]
        return poll.__dict__
