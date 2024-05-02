from .poll import Poll


class QuizPoll(Poll):
    type = "quiz_poll"

    def vote(self, user_id, option_index):
        if user_id in self.voters:
            return False
        return super().vote(user_id, option_index)

    def __init__(
            self,
            correct_option: int = None,
            explanation: str = "",
            *args,
            **kwargs
    ):
        self.correct_option = correct_option
        self.explanation = explanation
        super().__init__(*args, **kwargs)
