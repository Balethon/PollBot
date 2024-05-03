from json import load, dump
from os import path

from ..polls import Poll


__path__ = path.dirname(__file__)


with open(f"{__path__}/polls.json") as polls_json:
    polls = load(polls_json)


class Database:
    
    @staticmethod
    def get_polls():
        return polls
    
    @staticmethod
    def dump(poll):
        polls[poll.code] = poll.__dict__
        with open(f"{__path__}/polls.json", "w") as polls_json:
            dump(polls, polls_json, indent=4, ensure_ascii=False)
    
    @staticmethod
    def get_poll(code):
        return Poll.create(**polls[code])
