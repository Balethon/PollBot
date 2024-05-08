poll = """
💠 *{question}*

{options}

👥 تعداد آراء: {votes_count}
{type_name}
_کد نظرسنجی: {code}_

📊 *نظرسنجی ساخته شده با: [بات نظرسنجی](ble.ir/VoterBot)*
⚡ *قدرت گرفته از: [بلتون](balethon.ir/posts/about)*
""".strip()

option = """
{i}) {text}
🔹 _%{percentage} | {voters_count} نفر_
""".strip()

default_poll = """
نظرسنجی عادی
""".strip()

multiple_answers_poll = """
نظرسنجی چند جوابی
""".strip()

quiz_poll = """
نظرسنجی آزمون
""".strip()

start = """
• سلام ( {user} )

📊 با استفاده از این بازو میتوانید *نظرسنجی* ایجاد کنید و داخل کانال یا گروهتان ارسال کنید

🔺 *این بات از [Balethon](balethon.ir/posts/about) قدرت گرفته است*
""".strip()

start_group = """
• سلام ( {user} )

📊 بات نظرسنجی در این گروه حضور دارد و میتوانید نظرسنجی های خود را ارسال کنید

• [راهنما](send:/help)

🔺 *این بات از [Balethon](balethon.ir/posts/about) قدرت گرفته است*
""".strip()

help = """
⁉️ *راهنمایی بات*

• [نحوه اضافه کردن بات به کانال/گروه؟](send:/help invite_to_chat)

• [فرق انواع نظرسنجی؟](send:/help poll_types)

• [فرق حالت های نظرسنجی؟](send:/help poll_modes)

• [نحوه ساخت نظرسنجی و ارسال به کانال/گروه؟](send:/help create_poll)

• [دسترسی های لازم برای بات؟](send:/help access)

• [لینک اشتراک گذاری نظرسنجی چیست؟](send:/help poll_link)

• [محدودیت ها](send:/help limitations)

🆔 @voter_channel
""".strip()

invite_to_chat = """
⁉️ *نحوه افزودن ربات به کانال یا گروه*

🔹 ابتدا باید در نسخه وب بله web.bale.ai وارد حساب کاربری خود شوید.

🔺 سپس کانال یا گروه خود را انتخاب کنید و مراحل بالا را انجام دهید.

دسترسی های لازم برای برای ربات:
[ *ارسال پیام* ] و [ *ویرایش پیام* ]

🆔 @voter_channel | @VoterBot
""".strip()

poll_types = """
⁉️ *فرق انواع نظرسنجی*

*نظرسنجی عادی*
هرکس میتواند رای دهد و رای خود را پس بگیرد

*نظرسنجی چند جوابی*
هرکس میتواند به هر چند گزینه که بخواهد رای دهد و هرکدام از رای های خود را پس بگیرد

*نظرسنجی آزمون*
هرکس رای بدهد دیگر نمیتواند رای خود را عوض کند یا پس بگیرد
""".strip()

poll_modes = """
⁉️ *فرق حالت های نظرسنجی*

*حالت عمومی*
امکان مشاهده رای دهنگان نظرسنجی برای همه فراهم خواهد بود
همه میتوانند با داشتن کد نظرسنجی آن را به چت ها ارسال کنند

*حالت خصوصی*
امکان مشاهده رای دهنگان نظرسنجی برای هیچکس فراهم نخواهد بود
فقط شما میتوانید نظرسنجی را به چت ها ارسال کنید
""".strip()

create_poll = """
⁉️ *نحوه ساخت نظرسنجی و ارسال به گروه یا کانال*

🔹 پس از افزودن ربات به گروه/کانال و ادمین کردن آن، مراحل بالا را برای ساخت نظرسنجی انجام دهید !

🆔 @voter_channel | @VoterBot
""".strip()

access = """
دسترسی های لازم برای *ربات نظرسنجی* :
[ *ارسال پیام* ] و [ *ویرایش پیام* ]

🆔 @voter_channel | @VoterBot
""".strip()

poll_link = """
⁉️ *لینک اشتراک گذاری نظرسنجی چه کاربردی داره ؟*

🔘 *اگر نمیخواهید نظرسنجی را به کانال یا گروهی بفرستید، کافی است لینکی که ربات بعد از ساخت نظرسنجی میفرسته رو با هرکس که میخواید به اشتراک بذارید.*

🔘 *و هرکسی با استفاده از لینک، ربات را استارت کند نظرسنجی را دریافت میکند.*

🆔 @voter_channel | @VoterBot
""".strip()

limitations = """
⛔️ *محدودیت های نظرسنجی*

• محدودیت تعداد کارکتر سوال : *255*
• محدودیت تعداد کارکتر گزینه ها : *60*
• سقف تعداد گزینه هر نظرسنجی : *10*

🆔 @voter_channel | @VoterBot
""".strip()

my_polls = """
یکی از نظرسنجی ها را انتخاب کنید
""".strip()

no_polls = """
شما هیچ نظرسنجی ندارید
""".strip()

support = """
💬 *نظرات، پیشنهادات، انتقادات و مشکلات خود را در گروه زیر مطرح کنید :*
ble.ir/join/882iEVRkeq

🔻 *همچنین برای اطلاع از آپدیت و اخبار بات نظرسنجی، به کانال ما بپویندید:*
https://ble.ir/voter_channel

👤 سازنده ها: @rascalx و @sajiminer0
""".strip()

ads = """
*تعرفه تبلیغات*

ارسال به کاربران
50 هزار تومان

فوروارد به کاربران
50 هزار تومان

ارسال به گروه ها
50 هزار تومان

فوروارد به گروه ها
50 هزار تومان

ارسال همگانی
75 هزار تومان

فوروارد همگانی
75 هزار تومان

تبلیغات زیر نظرسنجی ها
ماهیانه 100 هزار تومان

عضویت اجباری
ماهیانه 250 هزار تومان

👤 جهت هماهنگی: @rascalx و @sajiminer0
""".strip()

select_poll_type = """
📊 *نوع نظرسنجی را انتخاب کنید*

• [فرق انواع نظرسنجی؟](send:/help poll_types)
""".strip()

select_poll_mode = """
🛃 *حالت نظرسنجی را انتخاب کنید*

• [فرق حالت های نظرسنجی؟](send:/help poll_modes)
""".strip()

give_question = """
🔺 *سوال نظرسنجی خود را ارسال کنید* :
""".strip()

question_too_long = """
‼️ تعداد نویسه سوال باید کمتر از *۲۵۵* باشد؛ سوال خود را اصلاح کنید و مجدد ارسال کنید
""".strip()

give_first_option = """
🟢 بسیار‌عالی! *گزینه اول سوال را ارسال کنید*
""".strip()

option_too_long = """
‼️ تعداد نویسه گزینه باید کمتر از *۷۰* باشد؛ گزینه خود را اصلاح کنید و مجدد ارسال کنید
""".strip()

give_second_option = """
🟢 *حالا گزینه دوم را ارسال کنید*
""".strip()

more_options = """
{options}

🟢 *«اگر گزینه دیگری دارید ارسال کنید، اگر نه دکمه تکمیل نظرسنجی را بزنید»* 👇
""".strip()

select_correct_option = """
✳️ *گزینه صحیح آزمون را انتخاب کنید*
""".strip()

give_explanation = """
✳️ *دلیل درست بودن گزینه را بنویسید*
""".strip()
