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
        return f"{self.text}\n▫️ _%{self.percentage} | {self.voters} رأی_\n\n".format_map(self.__dict__)
 