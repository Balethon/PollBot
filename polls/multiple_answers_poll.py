from .poll import Poll
import texts


class MultipleAnswersPoll(Poll):
    type = "multiple_answers_poll"
    type_name = texts.multiple_answers_poll

    def vote(self, user_id, option_index):
        if self.is_closed:
            return None
        option = self.options[option_index]
        if user_id in option.voters:
            option.voters.remove(user_id)
            return False
        option.voters.append(user_id)
        return True

    def to_info(self):
        return super().to_info() + "\n\n" + texts.multiple_answers_poll_info.format(
            voters_count=self.voters_count
        )
