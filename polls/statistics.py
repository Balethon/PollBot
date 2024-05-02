class Statistics:
    KEYWORDS = (
        ("simple", "نظرسنجی"),
        ("multiple_answers", "نظرسنجی چندجوابی"),
        ("quiz", "آزمون"),
        ("anonymous", "ناشناس"),
        ("public", "عمومی")
    )

    @property
    def mode(self):
        return "anonymous" if self.is_anonymous else "public"

    def __init__(
            self,
            type: str,
            is_anonymous: bool,
            is_closed: bool,
            total_voter_count: int,
            *args,
            **kwargs
    ):
        self.type = type
        self.is_anonymous = is_anonymous
        self.is_closed = is_closed
        self.total_voter_count = total_voter_count

    def __str__(self):
        statistics = f"\n{self.type} {self.mode}\n"
        for words in self.KEYWORDS:
            statistics = statistics.replace(*words)
        statistics += f"""
👥 تعداد آراء : *{self.total_voter_count} نفر*            
{'🚫 *پایان یافته !*' if self.is_closed else ''}            
🔺ساخت نظرسنجی : @VoterBot            
        """.strip()
        return statistics
