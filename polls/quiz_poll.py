from .poll import Poll
import texts


class QuizPoll(Poll):
    type = "quiz_poll"
    type_name = texts.quiz_poll

    def vote(self, user_id, option_index):
        if user_id in self.voters:
            return None
        return super().vote(user_id, option_index)

    @property
    def correct_option_number(self):
        return self.correct_option + 1

    def __init__(
            self,
            correct_option: int = 0,
            explanation: str = "",
            *args,
            **kwargs
    ):
        self.correct_option = correct_option
        self.explanation = explanation
        super().__init__(*args, **kwargs)

    def to_info(self):
        return super().to_info() + "\n\n" + texts.quiz_poll_info.format(
            correct_option=self.correct_option_number,
            explanation=self.explanation
        )
