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

    def to_poll(self, i, percentage):
        return texts.option.format(
            i=i,
            text=self.text,
            percentage=percentage,
            voters_count=self.voters_count
        )
