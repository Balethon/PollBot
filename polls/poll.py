from secrets import token_hex
from time import time

from .option import Option
from .statistics import Statistics


class Poll:
    type = "default"

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
        cls.create(
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
        voters = set()
        for option in self.options:
            voters |= set(option.voters)
        return voters

    @property
    def voters_count(self):
        return len(self.voters)

    def __init__(
            self,
            question: str,
            options: list[Option],
            code: str,
            creator: str,
            is_closed: bool,
            is_anonymous: int,
            create_time: int,
    ):
        self.type = self.type
        self.question = "*" + " ".join(question.split()) + "*"
        self.options = options
        self.code = code
        self.creator = creator
        self.is_closed = is_closed 
        self.is_anonymous = is_anonymous
        self.create_time = create_time

    def __str__(self):
        text = self.question + "\n\n"
        for i, option in enumerate(self.options):
            try:
                percentage = round((option.voters_count / self.voters_count) * 100)
            except ZeroDivisionError:
                percentage = 0
            text += str(Option(option, i, percentage, option.voters_count))
        text += str(Statistics(**self.__dict__, total_voter_count=self.voters_count))
        return text

    def vote(self, user_id, option_index):
        if self.is_closed:
            return None
        option = self.options[option_index]
        if user_id in option.voters:
            option.voters.remove(user_id)
            return False
        if user_id in self.voters:
            pass
        option.voters.append(user_id)
        return True
