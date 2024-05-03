from balethon.objects import ReplyKeyboard, InlineKeyboard

start = InlineKeyboard(
    [("📊 ایجاد نظرسنجی", "create_poll")],
    # [("📕 راهنمایی", "guide"), ("👤 پشتیبانی", "support")]
    # [("حمایت از ما", "support_us")]
)

poll_types = InlineKeyboard(
    [("نظرسنجی عادی", "simple_poll")],
    [("نظرسنجی چند جوابی", "multiple_answers_poll")],
    [("آزمون", "quiz")]
)

poll_modes = InlineKeyboard(
    [("ناشناس", "anonymous"), ("عمومی", "public")],
    # 1    [("لغو", "cancel")]
)

cancel = InlineKeyboard(
    [("لغو", "cancel")]
)

complete_poll = InlineKeyboard(
    [("افزودن گزینه جدید ➕", "new_option")],
    [("تکمیل نظرسنجی ☑️", "complete_poll")]
)
