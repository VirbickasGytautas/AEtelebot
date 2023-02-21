import telebot
from telebot import types
from telebot.types import ReplyKeyboardRemove

bot = telebot.TeleBot("6263321082:AAEzGyx-G7xiktNXujjCVWd9Ud7rHgG3O-8")

@bot.message_handler(commands=['post'])
def command(message):
    if message.text.split(" ", 1)[0] == "/post":
        bot.send_message(groupID, message.text.split(" ", 1)[1])
@bot.message_handler(content_types=['new_chat_members'])
def handler_new_member(message):
    user_name = message.new_chat_members[0].first_name
    bot.send_message(message.chat.id, f"Добро пожаловать!, {user_name}! \nДля начала взаимодействия с ботом, напишите /start")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	stic = open('stic/misha.webp', 'rb')  # стикер
	global markup
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	but1 = types.KeyboardButton("Миша - Гей")
	markup.add(but1)
	bot.reply_to(message, "{0.first_name}\nДобрый день! Я бот, который напоминает Вам о том, что Михаил - Гей!\nНе благодарите!"
				 .format(message.from_user), parse_mode='html', reply_markup=markup)
	bot.send_sticker(message.chat.id, stic)

@bot.message_handler(commands=['dell'])
def all_messages(message):
	bot.send_message(message.from_user.id, "Минус меню", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: True)
def menu(message):
	if message.text == "Миша - Гей":
		cid = message.chat.id
		inMurkup = types.InlineKeyboardMarkup(row_width=1)
		but10 = types.InlineKeyboardButton("Сегодня", callback_data='Сегодня')
		but11 = types.InlineKeyboardButton("Вчера", callback_data='Вчера')
		inMurkup.add(but10, but11)
		bot.send_message(message.chat.id, "Когда Миша Гей?:", reply_markup=inMurkup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		if call.data == 'Сегодня':
			bot.send_message(call.message.chat.id, 'Вы правы, Миша сегодня Гей')
			bot.send_message(call.message.chat.id, "Минус меню", reply_markup=ReplyKeyboardRemove())
		elif call.data == 'Вчера':
			bot.send_message(call.message.chat.id, 'Вы правы, Миша вчера тоже был Гей')
			bot.send_message(call.message.chat.id, "Минус меню", reply_markup=ReplyKeyboardRemove())
		#удаляем инлайновую клаву
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Результат:",
			reply_markup=None)
		#Создаём уведомление
		bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
			text='Выполнено!')

bot.polling(none_stop=True)
