from balethon.objects import ReplyKeyboard

start = ReplyKeyboard(
    ["📊 ایجاد نظرسنجی"],
    ["🗂 نظرسنجی های من"],
    ["📕 راهنمایی", "👤 پشتیبانی"],
    ["💰 تعرفه تبلیغات"]
)

poll_types = ReplyKeyboard(
    ["نظرسنجی عادی"],
    ["نظرسنجی چند جوابی"],
    ["نظرسنجی آزمون"]
)

poll_modes = ReplyKeyboard(
    ["خصوصی", "عمومی"]
)

complete_poll = ReplyKeyboard(
    ["تکمیل نظرسنجی ☑️"]
)
