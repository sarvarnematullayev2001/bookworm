# Aiogram
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ContentTypes, InlineKeyboardButton, InlineKeyboardMarkup


# Utility functions
from calculations import calculate_a4, calculate_a5
from datetime import date, timedelta, datetime

API_TOKEN = '5605471489:AAFouSIVt-3KjKhLjD5bCdpSY4_Gg29_1k0'


a4 = KeyboardButton('A4')
a5 = KeyboardButton('A5')
bk_format = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(a4, a5)


black_and_white = KeyboardButton('oq-qora')
colorful = KeyboardButton('rangli')
color_of_pages = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(black_and_white, colorful)


soft = KeyboardButton('yumshoq')
hard = KeyboardButton('qattiq')
cover = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(soft, hard)

phone_number = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Telefon raqamini ulashish', request_contact=True))

yes = InlineKeyboardButton(text='Ha', callback_data='YeS')
no = InlineKeyboardButton(text="Yo'q", callback_data='nO')
my_response = InlineKeyboardMarkup().add(yes, no)


confirm = InlineKeyboardButton(text='Tasdiqlayman', callback_data='confirm')
cancel = InlineKeyboardButton(text="Bekor qilaman", callback_data='cancel')
confirmation = InlineKeyboardMarkup().add(confirm, cancel)


book_type = dict()
order = 0
channel_id = '-1001877791425'
delivery_date = datetime.strftime(date.today() + timedelta(days=5), "%d-%m-%Y")


# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'buyurtma'])
async def send_welcome(message: types.Message):
    global book_type
    book_type = {}
    await message.answer(f"Assalomu Alaykum {message.from_user.full_name}!,\nIltimos nashr etmoqchi bo'lgan kitobingizni PDF formatda yuklang")


@dp.message_handler(commands=['video'])
async def send_video(message: types.Message):
    global book_type
    book_type = {}
    video = open('images/video.mp4', 'rb')
    await message.reply('Video yuklanmoqda... Iltimos biroz kuting!')
    await bot.send_video(chat_id=message.chat.id, video=video, caption="Kitob buyurtma berish uchun /buyurtma komandasidan foydalaning.")
    video.close()


@dp.message_handler(commands=['cover'])
async def send_video(message: types.Message):
    hard, soft = open('images/hard.jpeg', 'rb'), open('images/soft.jpeg', 'rb')
    await bot.send_photo(chat_id=message.chat.id, photo=hard, caption='Qattiq muqovali')
    await bot.send_photo(chat_id=message.chat.id, photo=soft, caption='Yumshoq muqovali')
    await message.reply("Kitob muqovasi qattiq bo'lsinmi yoki yumshoq?", reply_markup=cover)
    hard.close()
    soft.close()


@dp.message_handler(commands=['admin'])
async def send_admin(message: types.Message):
    await message.answer("Telefon raqam: +998335551301\nTelegram username: @sarvar_nematullayev")


@dp.message_handler(content_types=ContentTypes.DOCUMENT)
async def doc_handler(message: types.Message):
    if message.document.file_name.endswith('.pdf'):
        global book
        book = message.document.file_id
        await message.reply(f"Kitob yuklandi!.\nKitobingizning formati qanday bo'lsin?", reply_markup=bk_format)
    else:
        await message.reply("Kechirasiz siz yuklagan file formati PDF emas, iltimos qayta urining.")


@dp.message_handler(content_types=ContentTypes.CONTACT)
async def doc_handler(message: types.Message):
    global number, book_type
    number = message.contact.phone_number
    book_type['phone_number'] = number
    book_type['client'] = message.from_user.username
    await message.answer("Nashr etishga doir qo'shimcha ma'lumot kiritishni xohlaysizmi?", reply_markup=my_response)


@dp.message_handler(content_types=['photo'])
async def send_photo(message: types.Message):
    if message.caption:
        if message.caption == '#kvitansiya':
            await book_info
            await bot.send_photo(chat_id=channel_id, photo=message.photo[-1].file_id, caption=f"#Buyurtma N{order}")
            await message.answer("Kitob tayyor bo'lgach uni shu manzildan olib ketsangiz bo'ladi")
            await bot.send_location(chat_id=message.chat.id, latitude=41.328213, longitude=69.227373)
            await message.answer("Agarda savollaringiz bo'lsa /admin komandasidan foydalanib biz bilan bog'lanishingiz mumkin.\nBoshqa kitobni buyurtma qilish uchun /buyurtma komandasidan foydalaning.", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer("Tag nomi shunday yozilishi shart: #kvitansiya", reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply("Iltimos botga to'g'ri ma'lumot kiriting.", reply_markup=ReplyKeyboardRemove())


@dp.message_handler()
async def reply_for_unknowns(message: types.Message):
    global book_type, order, book_info
    if message.text == 'A4' or message.text == 'A5':
        book_type['format'] = message.text
        if message.text == 'A5':
            await message.reply("Kitob muqovasi qattiq bo'lsinmi yoki yumshoq?\nQanday ko'rinishini ko'rish uchun /cover komandasidan foydalaning.", reply_markup=cover)
        else:
            await message.reply("Kitobingiz betlari rangli bo'lsinmi yoki oq-qora?", reply_markup=color_of_pages)
    elif message.text == 'yumshoq' or message.text == 'qattiq':
        book_type['cover'] = message.text
        await message.reply("Kitobingiz betlari rangli bo'lsinmi yoki oq-qora?", reply_markup=color_of_pages)
    elif message.text == 'oq-qora' or message.text == 'rangli':
        book_type['color'] = message.text
        await message.reply("Kitob betlari soni qancha. Son ko'rinishida kiriting.\nMasalan:\n250", reply_markup=ReplyKeyboardRemove())
    elif message.text.isdigit() and ('cover' in book_type.keys() or ('color' and 'format') in book_type.keys()) and 'pages' not in book_type.keys():
        if int(message.text) > 50:    
            book_type['pages'] = message.text
            await message.reply("Shu kitobdan nechta nashr etmoqchisiz?. Son ko'rinishida kiriting.\nMasalan:\n1", reply_markup=ReplyKeyboardRemove())
        else:
            await message.reply("Kitob nashr etish uchun minimum betlari soni 50 dan katta bo'lishi lozim", reply_markup=ReplyKeyboardRemove())
    elif message.text.isdigit() and 'pages' in book_type.keys():
        if int(message.text) > 0:
            book_type['number_of_books'] = message.text
            await message.answer("Siz bilan bog'lanishimiz uchun telefon raqamingizni qoldiring.", reply_markup=phone_number)
        else:
            await message.answer("Siz kamida bitta kitob nashr etish uchun buyurtma bera olasiz.", reply_markup=ReplyKeyboardRemove())
    elif message.text.startswith('!') and message.text.endswith('!'):
        book_type['add_info'] = message.text
        order += 1
        if book_type['format'] == 'A5':    
            caption_for_a5 = f"*#Buyurtma N{order}\n\n1.Buyurtmachi - @{book_type['client']}\n2.Telefon raqami - {book_type['phone_number']}\n3.Kitob formati - {book_type['format']}\n4.Kitob betlari rangi - {book_type['color']}\n5.Kitob muqovasi - {book_type['cover']}\n6.Kitob betlari soni - {book_type['pages']}betgacha\n7.Tirajlar soni - {book_type['number_of_books']}\n8.Qo'shimcha ma'lumot - {book_type['add_info'].strip('!')}\n9.Kitob narxi - {calculate_a5(book_type)[:-4]} so'm*\n\n_Kitob uzog'i {delivery_date} gacha tayyor bo'ladi_"
            await message.answer_document(book, caption=caption_for_a5, parse_mode='markdown', reply_markup=ReplyKeyboardRemove())
            book_info = bot.send_document(chat_id=channel_id, document=book, caption=caption_for_a5, parse_mode='markdown')
        else:
            caption_for_a4 = f"*#Buyurtma N{order}\n\n1.Buyurtmachi - @{book_type['client']}\n2.Telefon raqami - {book_type['phone_number']}\n3.Kitob formati - {book_type['format']}\n4.Kitob betlari rangi - {book_type['color']}\n5.Kitob betlari soni - {book_type['pages']}betgacha\n6.Tirajlar soni - {book_type['number_of_books']}\n7.Qo'shimcha ma'lumot - {book_type['add_info'].strip('!')}\n8.Kitob narxi - {calculate_a4(book_type)[:-4]} so'm*\n\n_Kitob uzog'i {delivery_date} gacha tayyor bo'ladi_"
            await message.answer_document(book, caption=caption_for_a4, parse_mode='markdown', reply_markup=ReplyKeyboardRemove())
            book_info = bot.send_document(chat_id=channel_id, document=book, caption=caption_for_a4, parse_mode='markdown')
        await message.answer("Buyurtmani tasdiqlaysizmi!", reply_markup=confirmation)
        book_type = {}
    else:
        await message.answer("Botdan to'g'ri foydalanish uchun video qo'llanmani ko'rish uchun /video ni bosing.")


@dp.callback_query_handler(text=['YeS', 'nO'])
async def respond_answer(call: types.CallbackQuery):
    if call.data == 'YeS':
        await call.message.reply("Unday bo'lsa ! belgisidan foydalanib ma'lumotingizni quyidagicha kiriting.\nMasalan: !Kitob 200 betgacha chiqarilsin!", reply_markup=ReplyKeyboardRemove())
    else:
        global order, book_type, book_info
        order += 1
        if book_type['format'] == 'A5':
            caption_for_a5 = f"*#Buyurtma N{order}\n\n1.Buyurtmachi - @{book_type['client']}\n2.Telefon raqami - {book_type['phone_number']}\n3.Kitob formati - {book_type['format']}\n4.Kitob betlari rangi - {book_type['color']}\n5.Kitob muqovasi - {book_type['cover']}\n6.Kitob betlari soni - {book_type['pages']}betgacha\n7.Tirajlar soni - {book_type['number_of_books']}\n8.Kitob narxi - {calculate_a5(book_type)[:-4]} so'm*\n\n_Kitob uzog'i {delivery_date} gacha tayyor bo'ladi_"
            await call.message.answer_document(book, caption=caption_for_a5, parse_mode='markdown', reply_markup=ReplyKeyboardRemove())
            book_info = bot.send_document(chat_id=channel_id, document=book, caption=caption_for_a5, parse_mode='markdown')
        else:
            caption_for_a4 = f"*#Buyurtma N{order}\n\n1.Buyurtmachi - @{book_type['client']}\n2.Telefon raqami - {book_type['phone_number']}\n3.Kitob formati - {book_type['format']}\n4.Kitob betlari rangi - {book_type['color']}\n5.Kitob betlari soni - {book_type['pages']}betgacha\n6.Tirajlar soni - {book_type['number_of_books']}\n7.Kitob narxi - {calculate_a4(book_type)[:-4]} so'm*\n\n_Kitob uzog'i {delivery_date} gacha tayyor bo'ladi_"
            await call.message.answer_document(book, caption=caption_for_a4, parse_mode='markdown', reply_markup=ReplyKeyboardRemove())
            book_info = bot.send_document(chat_id=channel_id, document=book, caption=caption_for_a4, parse_mode='markdown')
        await call.message.answer("Buyurtmani tasdiqlaysizmi!", reply_markup=confirmation)
        book_type = {}


@dp.callback_query_handler(text=['confirm', 'cancel'])
async def send_confirmation(call: types.CallbackQuery):
    if call.data == 'confirm':
        await call.message.answer("9860 6004 3152 6265\n*Sarvar Ne'matullayev*\n\n_Ushbu yuqorida ko'rsatilgan plastik raqamga to'lovni amalga oshiring, so'ngra to'lov kvitansiyasini yoki to'lov o'tkazilganligi haqidagi screenshotni #kvitansiya tagini yozgan holda yuboring._", parse_mode='markdown', reply_markup=ReplyKeyboardRemove())
    else:
        global book_type, order
        order -= 1 
        book_type = {}
        await call.message.answer("Buyurtmangiz bekor qilindi!. Qaytadan boshlash uchun /buyurtma komandasini bosing.", reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)