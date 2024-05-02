from .poll import Poll


class MultipleAnswersPoll(Poll):
    type = "multiple_answers"

    def vote(self, user_id, option_index):
        if self.is_closed:
            return None
        option = self.options[option_index]
        if user_id in option.voters:
            option.voters.remove(user_id)
            return False
        option.voters.append(user_id)
        return True
