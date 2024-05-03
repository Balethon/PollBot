class Option:
    
    def __init__(
            self,
            text: str,
            voters: list
    ):
        self.text = " ".join(text.split())
        self.voters = voters

    @property
    def voters_count(self):
        return len(self.voters)

    def __str__(self):
        return f"{self.text} | {self.voters})"
 