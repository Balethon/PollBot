from json import load, dump
from os import path

from polls import Poll


__path__ = path.dirname(__file__)


with open(path.join(__path__, "polls.json"), encoding="utf-8") as polls_json:
    polls = load(polls_json)


class Database:

    @staticmethod
    def get_polls():
        return polls

    @staticmethod
    def save_poll(poll):
        polls[poll.code] = poll.to_dict()
        with open(f"{__path__}/polls.json", "w") as polls_json:
            dump(polls, polls_json, indent=4)

    @staticmethod
    def load_poll(code):
        return Poll.create(**polls[code])
