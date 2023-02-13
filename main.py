import telebot
from datetime import datetime
import datetime
from telebot import types
from collections import defaultdict
#import xlrd не подходит
import csv

bot = telebot.TeleBot("5941676589:AAExTrhG3aZCkG13obkHyzPE-Z8F5NTxq_A") #API телеграмм бота

@bot.message_handler(commands=['start'])
def send_welcome(message):
	stic = open('stic/welcome.webp', 'rb') #стикер

	#Меню, клавиатура
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	but1 = types.KeyboardButton("Статистика со стенда ДСТ УУР")
	but2 = types.KeyboardButton("Статистика со стенда Настройки БУ БиД")
	markup.add(but1, but2)

	bot.reply_to(message, "Здравствуй, {0.first_name}\nБот в режиме разработки, многие функции недоступны, "
						  "но пофиг пшл нх птчк".format(message.from_user),parse_mode='html',reply_markup=markup)
	bot.send_sticker(message.chat.id,stic)

#Ответ бота на определенные команды
@bot.message_handler(func=lambda message: True)
def menu(message):
	if message.chat.type == 'private':
		if message.text == "Статистика со стенда ДСТ УУР":
			with open("tmpID.csv", encoding='utf-8') as r_file:
				values = defaultdict(int)
				file_reader = csv.reader(r_file, delimiter=";")
				count = 0
				for row in file_reader:
					count == 0
					count += 1
					#Подсчет строк
					#if count == 0:
					#	print(f'Файл содержит столбцы: {", ".join(row)}')
					#else:
					#	print(f'{row[3]} - {row[0]} - {row[1]} - {row[2]} {row[4]}')
					#count += 1
				dateNOWstr = datetime.datetime.now()

			bot.send_message(message.chat.id, dateNOWstr)
			bot.send_message(message.chat.id, count)
		elif message.text == "Статистика со стенда Настройки БУ БиД":
			#инлайновая клавиатура
			inMurkup = types.InlineKeyboardMarkup(row_width=1)
			but1 = types.InlineKeyboardButton("Умная кнопка 1", callback_data='book1')
			but2 = types.InlineKeyboardButton("Умная кнопка 2", callback_data='book2')
			but3 = types.InlineKeyboardButton("Умная кнопка 3", callback_data='book3')
			but4 = types.InlineKeyboardButton("Умная кнопка 4", callback_data='book4')
			inMurkup.add(but1, but2, but3, but4)
			bot.send_message(message.chat.id, "ВОТ СПИСОК УМНЫХ НЕ РАБОЧИХ КНОПОК", reply_markup=inMurkup)
		else:
			bot.send_message(message.chat.id, "Я не знаю что и ответить")

#обработка callback
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'Отчет1':
				doc = open('boo/Файл1.pdf', 'rb')
				bot.send_document(call.message.chat.id, doc)
			elif call.data == 'Отчет2':
				doc = open('boo/boo/Файл2.pdf','rb')
				bot.send_document(call.message.chat.id, doc)
			elif call.data == 'Отчет3':
				doc = open('boo/Файл3.pdf', 'rb')
				bot.send_document(call.message.chat.id, doc)
			elif call.data == 'Отчет4':
				doc = open('boo/Файл4.pdf', 'rb')
				bot.send_document(call.message.chat.id, doc)
			#удаляем инлайновую клаву
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Форматы отчетов в разработке",
				reply_markup=None)
			#Создаём уведомление
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
				text='Всего доброго!')
	except Exception as e:
		print(repr(e))

bot.polling(none_stop=True)