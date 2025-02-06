poll = """
💠 *{question}*

{options}

👥 تعداد آراء: {votes_count}
_{type_name} - {mode_name}_
_کد نظرسنجی: {code}_

📊 *نظرسنجی ساخته شده با: [بات نظرسنجی](ble.ir/VoterBot)*
⚡ _قدرت گرفته از: [Balethon](balethon.ir/posts/about)_
""".strip()

poll_is_closed = """
🚫 *این نظرسنجی توسط سازنده بسته شده* 🚫
""".strip()

option = """
{i}) {text}
🔹 _%{percentage} | {voters_count} نفر_
""".strip()

poll_info = """
💬 *سوال:* _{question}_

🔘 *گزینه ها:*

{options}

📊 *تعداد آراء:* _{votes_count}_
| *نوع:* _{type_name}_
| *حالت:* _{mode_name}_

🏷️ *کد:* _{code}_
🕓 *زمان ساخت:*
_{create_time}_

🔗 *لینک:*
{link}
🤖 *دستور ارسال:*
{command}

🚩 *وضعیت:* {status}
""".strip()

multiple_answers_poll_info = """
👥 *تعداد رای دهنده ها:* _{voters_count}_
""".strip()

quiz_poll_info = """
🟢 *گزینه درست:* _{correct_option}_
☑️ *دلیل درستی گزینه:* _{explanation}_
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

public = """
عمومی
""".strip()

anonymous = """
خصوصی
""".strip()

opened = """
باز
""".strip()

closed = """
بسته
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
⁉️ | *نحوه افزودن ربات به کانال/گروه*

( *1* ) _ابتدا باید در_ ( *نسخه وب بله* web.bale.ai ) _وارد حساب کاربری خود شوید_

( *2* ) _سپس کانال یا گروه خود را انتخاب کنید و مراحل بالا را انجام دهید_

🔒 _دسترسی های لازم برای برای بات:_
( *ارسال پیام* ) و ( *ویرایش پیام* )
""".strip()

poll_types = """
⁉️ | *فرق انواع نظرسنجی*

• *نظرسنجی عادی*
> _هرکس میتواند رای دهد و رای خود را پس بگیرد_

• *نظرسنجی چند جوابی*
> _هرکس میتواند به هر چند گزینه که بخواهد رای دهد و هرکدام از رای های خود را پس بگیرد_

• *نظرسنجی آزمون*
> _هرکس رای بدهد دیگر نمیتواند رای خود را عوض کند یا پس بگیرد_
""".strip()

poll_modes = """
⁉️ | *فرق حالت های نظرسنجی*

• *حالت عمومی*
> _امکان مشاهده رای دهنگان نظرسنجی برای همه فراهم خواهد بود
> همه میتوانند با داشتن کد نظرسنجی آن را به چت ها ارسال کنند_

• *حالت خصوصی*
> _امکان مشاهده رای دهنگان نظرسنجی برای هیچکس فراهم نخواهد بود
> فقط شما میتوانید نظرسنجی را به چت ها ارسال کنید_
""".strip()

create_poll = """
⁉️ | *نحوه ساخت نظرسنجی و ارسال به کانال/گروه*

•  _پس از افزودن ربات به کانال/گروه و ادمین کردن بات، مراحل بالا را برای ساخت نظرسنجی انجام دهید_

• [نحوه اضافه کردن بات به کانال/گروه؟](send:/help invite_to_chat)
""".strip()

access = """
🔒 *دسترسی های لازم برای بات نظرسنجی :*
( *ارسال پیام* ) و ( *ویرایش پیام* )
""".strip()

poll_link = """
⁉️‌ | *لینک اشتراک گذاری نظرسنجی چه کاربردی دارد ؟*

• _در صورتی که نمیخواهید نظرسنجی را به کانال/گروه ارسال کنید، کافی است لینکی که ربات بعد از ساخت نظرسنجی ارسال میکند را با هرکسی که میخواهید به اشتراک بگذارید_

• _و هرکسی با استفاده از لینک، ربات را استارت کند نظرسنجی را دریافت خواهد کرد_
""".strip()

limitations = """
⛔️ | *محدودیت های ساخت نظرسنجی*

• تعداد نویسه سوال ( *256* )
• تعداد نویسه گزینه ها ( *64* )
• تعداد نویسه دلیل درستی ( *128* )
• تعداد گزینه هر نظرسنجی ( *10* )
""".strip()

no_polls = """
شما هیچ نظرسنجی ندارید
""".strip()

my_polls = """
🔴 *یکی از گزینه ها را انتخاب کنید:*
""".strip()

show_voters = """
مشاهده رای دهندگان
""".strip()

support = """
💬 *نظرات، پیشنهادات، انتقادات و مشکلات خود را در گروه زیر مطرح کنید :*
ble.ir/join/882iEVRkeq

🔻 *همچنین برای اطلاع از آپدیت و اخبار بات نظرسنجی، به کانال ما بپویندید:*
https://ble.ir/voter_channel

👤 سازنده ها: @rascalx و @sajiminer0
""".strip()

ads = """
🔘 | *تعرفه تبلیغات در بات نظرسنجی* |

• *ارسال/فوروارد به کاربران*
> _50,000_ تومان

• *ارسال/فوروارد به گروه ها*
> _50,000_ تومان

• *ارسال/فوروارد همگانی*
> _75,000_ تومان

• *تبلیغات زیر نظرسنجی ها*
> ماهیانه _100,000_ تومان

• *عضویت اجباری*
> ماهیانه _250,000_ تومان

🔴 *پشتیبانی و خرید* : @sajiminer0
""".strip()

admins_panel = """
به پنل ادمین ها خوش آمدید
""".strip()

give_message = """
پیام رو وارد کن
""".strip()

sending_started = """
ارسال شروع شد
""".strip()

sending_finished = """
ارسال تمام شد
تعداد موفق: {success_count}
""".strip()

statistics = """
📊 تعداد نظرسنجی: *{polls}*
👥 تعداد کاربران: *{users}* نفر
👥 تعداد ممبرها: *{members}* نفر
تعداد گروه ها: *{groups}*
تعداد کانال ها: *{channels}*
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
‼️ تعداد نویسه سوال نباید بیشتر از *256* باشد؛ سوال خود را اصلاح کنید و مجدد ارسال کنید
""".strip()

give_first_option = """
🟢 بسیار‌عالی! *گزینه اول سوال را ارسال کنید*
""".strip()

option_too_long = """
‼️ تعداد نویسه گزینه نباید بیشتر از *64* باشد؛ گزینه خود را اصلاح کنید و مجدد ارسال کنید
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

explanation_too_long = """
‼️ تعداد نویسه دلیل درستی نباید بیشتر از *128* باشد؛ گزینه خود را اصلاح کنید و مجدد ارسال کنید
""".strip()

command_usage = """
• [نحوه ساخت نظرسنجی و ارسال به کانال/گروه؟](send:/help create_poll)

از این دستور برای ارسال نظرسنجی به چت ها استفاده کنید👇
""".strip()

link_usage = """
• [لینک اشتراک گذاری نظرسنجی چیست؟](send:/help poll_link)

این لینک رو هرکسی میتونه برای دیدن نظرسنجی استفاده کنه👇
""".strip()
