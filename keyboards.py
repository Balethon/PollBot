from balethon.objects import InlineKeyboard

start = InlineKeyboard(
    [("📊 ایجاد نظرسنجی", "create_poll")],
    # [("📕 راهنمایی", "guide"), ("👤 پشتیبانی", "support")]
    # [("حمایت از ما", "support_us")]
)

poll_types = InlineKeyboard(
    [("نظرسنجی عادی", "default_poll")],
    [("نظرسنجی چند جوابی", "multiple_answers_poll")],
    [("آزمون", "quiz_poll")]
)

poll_modes = InlineKeyboard(
    [("ناشناس", "anonymous"), ("عمومی", "public")],
    # [("لغو", "cancel")]
)

cancel = InlineKeyboard(
    [("لغو", "cancel")]
)

complete_poll = InlineKeyboard(
    [("افزودن گزینه جدید ➕", "new_option")],
    [("تکمیل نظرسنجی ☑️", "complete_poll")]
)
