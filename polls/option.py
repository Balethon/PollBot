import texts


class Option:
    
    def __init__(
            self,
            text: str,
            voters: list = None
    ):
        self.text = " ".join(text.split())
        self.voters = voters or []

    @property
    def voters_count(self):
        return len(self.voters)

    def __str__(self):
        return f"{self.text} | {self.voters_count}"

    def get_formatted_voters(self):
        from database import Database
        if len(self.voters) > 100:
            voters = self.voters[-100:]
        else:
            voters = self.voters
        voters = Database.load_users(voters)
        voters = "\n".join(str(voter) for voter in voters)
        return f"```[{texts.show_voters}]{voters}```"

    def to_anonymous_poll(self, i, percentage):
        return texts.option.format(
            i=i,
            text=self.text,
            percentage=percentage,
            voters_count=self.voters_count
        )

    def to_public_poll(self, i, percentage):
        return f"{self.to_anonymous_poll(i, percentage)}\n{self.get_formatted_voters()}"

    def to_dict(self):
        return self.__dict__
