import csv
import telebot
from telebot import types
import datetime
from datetime import datetime
import time
import io
import pandas as pd

start_time = time.time()
bot = telebot.TeleBot("5941676589:AAExTrhG3aZCkG13obkHyzPE-Z8F5NTxq_A") #API телеграмм бота

@bot.message_handler(commands=['start'])
def send_welcome(message):
	stic = open('stic/welcome.webp', 'rb') #стикер

	#Меню, клавиатура
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	but1 = types.KeyboardButton("Статистика УУР")
	but2 = types.KeyboardButton("Отчеты по качеству")
	markup.add(but1, but2)

	bot.reply_to(message, "Здравствуй, {0.first_name}\nБот в режиме разработки, многие функции недоступны, "
						  "но пофиг пшл нх птчк".format(message.from_user),parse_mode='html',reply_markup=markup)
	bot.send_sticker(message.chat.id,stic)

#Ответ бота на определенные команды
@bot.message_handler(func=lambda message: True)
def menu(message):
	if message.chat.type == 'private':
		if message.text == "Статистика УУР":
			cid = message.chat.id
			msgSD = bot.send_message(cid,'Введите дату начала периода в формате дд.мм.гггг Ч:М:С (Пример 24.01.2022 07:00:00):')
			bot.register_next_step_handler(msgSD, stepSD)

		elif message.text == "Отчеты по качеству":
			#инлайновая клавиатура
			inMurkup = types.InlineKeyboardMarkup(row_width=1)
			but1 = types.InlineKeyboardButton("ДЕФЕКТЫ НА ПРОИЗВОДСТВЕ ЭУР 2022 год", callback_data='Отчет1')
			but2 = types.InlineKeyboardButton("Умная кнопка 2", callback_data='Отчет2')
			but3 = types.InlineKeyboardButton("Умная кнопка 3", callback_data='Отчет3')
			but4 = types.InlineKeyboardButton("Умная кнопка 4", callback_data='Отчет4')
			inMurkup.add(but1, but2, but3, but4)
			bot.send_message(message.chat.id, "ВОТ СПИСОК УМНЫХ НЕ РАБОЧИХ КНОПОК", reply_markup=inMurkup)
		else:
			bot.send_message(message.chat.id, "Я не знаю что и ответить")
def stepSD(message):
	cid = message.chat.id
	global uSD
	uSD = message.text
	uED = str
	print(uSD)
	bot.send_message(cid, "Сохранил!")
	msgED = bot.send_message(cid,'Введите дату конца периода в формате дд.мм.гггг Ч:М:С (Пример 24.01.2022 07:00:00):')
	bot.register_next_step_handler(msgED, stepED)

def stepED(message):
	cid = message.chat.id
	global uED
	uED = message.text
	uSD = str
	print(uED)
	bot.send_message(cid, "Сохранил!")
	msgRD = bot.send_message(cid, "Подождите около минуты")
	resultRD(message)

def resultRD(message):
	cid = message.chat.id
	print(uSD,uED)
	file = 'tmpID.csv'
	dateparse = lambda x: pd.datetime.strptime(x, "%d.%m.%Y %H:%M:%S")
	dateparse = str
	today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	df = pd.read_csv(file, index_col=0, sep=';', names=['1', '2', '3', '4', '5'], on_bad_lines='skip', parse_dates=[4], date_parser=dateparse)
	df['4'] = pd.to_datetime(df['4'])
	newdf = (df['4'] > uSD) & (df['4'] <= uED)
	newdf = df.loc[newdf]
	newdf = len(newdf.index)
	total = (df['4'] > '11.01.2023 00:00:00') & (df['4'] <= datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
	total = len(total.index)

	print('Сегодня:', today)
	print('Количество произведенных за выбранный период: ',newdf)
	print('За 2023 год:', total )
	print("Операция выполнена за %s секунд" % (time.time() - start_time))

	bot.send_message(cid, text = "Сегодня:")
	bot.send_message(cid,today)
	bot.send_message(cid,"Количество произведенных за выбранный период: ")
	bot.send_message(cid, newdf)

#обработка callback
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'Отчет1':
				doc = open('report/Файл1.pdf', 'rb')
				bot.send_document(call.message.chat.id, doc)
			elif call.data == 'Отчет2':
				doc = open('report/Файл2.pdf','rb')
				bot.send_document(call.message.chat.id, doc)
			elif call.data == 'Отчет3':
				doc = open('report/Файл3.pdf', 'rb')
				bot.send_document(call.message.chat.id, doc)
			elif call.data == 'Отчет4':
				doc = open('report/Файл4.pdf', 'rb')
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