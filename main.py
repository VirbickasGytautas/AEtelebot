import telebot
from telebot import types
import random
import xlrd #не подходит
import csv

#from openpyxl import load_workbook

bot = telebot.TeleBot("5941676589:AAExTrhG3aZCkG13obkHyzPE-Z8F5NTxq_A")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	stic = open('stic/welcome.webp', 'rb')

	# клавиатура
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	but1 = types.KeyboardButton("Статистика со стенда ДСТ УУР")
	but2 = types.KeyboardButton("Статистика со стенда Настройки БУ БиД")
	markup.add(but1, but2)

	bot.reply_to(message, "Здравствуй, {0.first_name}\nБот в режиме разработке, многие функции недоступны, но пофиг пшл нх птчк".format(message.from_user),parse_mode='html',reply_markup=markup)
	bot.send_sticker(message.chat.id,stic)



@bot.message_handler(func=lambda message: True)
def menu(message):
	if message.chat.type == 'private':
		if message.text == "Статистика со стенда ДСТ УУР":

			#статистику из excel
			#rb = xlrd.open_workbook('stat/stat.xls', formatting_info=True)
			#sheet = rb.sheet_by_index(0)
			#for rownum in range(sheet.nrows):
			#	rand = int(random.randint(0, rownum))
			#	row = sheet.row_values(rand)
			with open("tmpID.csv", encoding='utf-8') as r_file:
				file_reader = csv.reader(r_file, delimiter=";")
				count = 0

				for row in file_reader:
					if count == 0:
						print(f'Файл содержит столбцы: {", ".join(row)}')
					else:
						print(f'{row[3]} - {row[0]} - {row[1]} - {row[2]} {row[4]}')
					count += 1

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
			if call.data == 'book1':
				doc = open('boo/Plotnikov_Ivan-Aleksandr_Vasilevich_Kolchak_Issledovatel_admiral_Verhovnyi_pravitel_Rossii.pdf', 'rb')
				bot.send_document(call.message.chat.id, doc)
			elif call.data == 'book2':
				doc = open('boo/Turkul_-_Drozdovtsy_v_ogne.pdf','rb')
				bot.send_document(call.message.chat.id, doc)
			elif call.data == 'book3':
				doc = open('boo/Vrangel_P_Zapiski_a4.pdf', 'rb')
				bot.send_document(call.message.chat.id, doc)
			elif call.data == 'book4':
				doc = open('boo/Drozdovsky_dnevnik_1963__ocr.pdf', 'rb')
				bot.send_document(call.message.chat.id, doc)
			#удаляем инлайновую клаву
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Книги на любой вкус",
				reply_markup=None)
			#Создаём уведомление
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
				text='Приятного чтения!')
	except Exception as e:
		print(repr(e))

bot.polling(none_stop=True)