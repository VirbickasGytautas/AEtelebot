import telebot
from telebot import types
import datetime
from datetime import datetime, timedelta
import time
import pandas as pd

start_time = time.time()
bot = telebot.TeleBot("5941676589:AAExTrhG3aZCkG13obkHyzPE-Z8F5NTxq_A") #API телеграмм бота
today = datetime.today().strftime('%Y.%m.%d %H:%M:%S')
file = r'\\pk-55\CSV\tmpID.csv' #статистика с ДСП

#Белый список
list('Белый список')
[415077278,565955,5955564]

#bot.send_message(message.chat.id, 'Доступ ограничен')

@bot.message_handler(commands=['start'])
def send_welcome(message):
	userID = message.chat.id
	userName = message.chat.first_name
	print('id пользователя:', userID)
	print('Имя пользователя: ', userName)
	stic = open('stic/welcome.webp', 'rb') #стикер

	#Меню, клавиатура
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	but1 = types.KeyboardButton("Статистика УУР")
	but2 = types.KeyboardButton("Отчеты по качеству")
	markup.add(but1, but2)
	bot.reply_to(message, "Здравствуй, {0.first_name}\nБот в режиме разработки, многие функции недоступны"
				 .format(message.from_user),parse_mode='html',reply_markup=markup)
	bot.send_sticker(message.chat.id,stic)

#Ответ бота на определенные команды
@bot.message_handler(func=lambda message: True)
def menu(message):
	if message.chat.type == 'private':
		if message.text == "Статистика УУР":
			cid = message.chat.id
			inMurkup = types.InlineKeyboardMarkup(row_width=1)
			but10 = types.InlineKeyboardButton("Сегодня", callback_data='Сегодня')
			but11 = types.InlineKeyboardButton("Вчера", callback_data='Вчера')
			but12 = types.InlineKeyboardButton("Произвольный период", callback_data='Период')
			inMurkup.add(but10, but11, but12)
			bot.send_message(message.chat.id, "Статистика за даты:", reply_markup=inMurkup)

		elif message.text == "Отчеты по качеству":
			#инлайновая клавиатура
			inMurkup = types.InlineKeyboardMarkup(row_width=1)
			but1 = types.InlineKeyboardButton("Дефекты УУР 2022 год", callback_data='Отчет1')
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
	msgED = bot.send_message(cid,'Введите дату конца периода в формате гггг.мм.дд Ч:М:С\n'
								 '(Пример 2023.01.02 07:00:00):')
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
	df = pd.read_csv(file, index_col=0, sep=';', names=['1', '2', '3', '4', '5'], on_bad_lines='skip')
	df['4'] = pd.to_datetime(df['4'], format='%d.%m.%Y %H:%M:%S')

	newdf = (df['4'] >= uSD) & (df['4'] <= uED)
	newdf = df.loc[newdf]
	newdf = len(newdf.index)
	total = (df['4'] > '2023.01.01 00:00:00') & (df['4'] <= today)
	total = len(total.index)

	print('Запрос от:', str(message.chat.first_name), 'ID:',str(message.chat.id))
	print('Сегодня:', today)
	print('Количество произведенных за выбранный период: ',newdf)
	print('За 2023 год:', total )
	print("Операция выполнена за %s секунд" % (time.time() - start_time))

	#bot.send_message(cid, "Сегодня:")
	#bot.send_message(cid,today)
	bot.send_message(cid,f'Количество произведенных за выбранный период: \n'
						 f'С {uSD} по {uED}')
	bot.send_message(cid, newdf)

def period(message):
	cid = message.chat.id
	msgSD = bot.send_message(cid, 'Введите дату начала периода в формате гггг.мм.дд Ч:М:С\n'
								  '(Пример 2023.02.17 07:00:00):')
	bot.register_next_step_handler(msgSD, stepSD)

def callback_today(message):
	cid = message.chat.id
	today2 = datetime.today().strftime('%Y.%m.%d')
	yesterday = datetime.today() - timedelta(days=1)
	yesterday = yesterday.strftime('%Y.%m.%d')
	print(today2, yesterday)
	df = pd.read_csv(file, index_col=0, sep=';', names=['1', '2', '3', '4', '5'], on_bad_lines='skip')
	df['4'] = pd.to_datetime(df['4'], format='%d.%m.%Y %H:%M:%S')
	newdf = (df['4'] >= today2) & (df['4'] <= today)
	newdf = df.loc[newdf]
	newdf = len(newdf.index)
	total = (df['4'] > '2023.01.01 00:00:00') & (df['4'] <= today)
	total = len(total.index)

	print('Запрос от:', str(message.chat.first_name), 'ID:',str(message.chat.id))
	print('Сегодня:', today)
	print('Количество произведенных: ', newdf)
	print('За 2023 год:', total)
	print("Операция выполнена за %s секунд" % (time.time() - start_time))

	bot.send_message(cid, f'Сегодня: {today}')
	bot.send_message(cid, "Количество произведенных: ")
	bot.send_message(cid, newdf)

def callback_yesterday(message):
	cid = message.chat.id
	today2 = datetime.today()
	today2 = today2.strftime('%Y.%m.%d')
	afteryesterday = datetime.today() - timedelta(days=1)
	afteryesterday= afteryesterday.strftime('%Y.%m.%d')
	print(today2, afteryesterday)
	df = pd.read_csv(file, index_col=0, sep=';', names=['1', '2', '3', '4', '5'], on_bad_lines='skip')
	df['4'] = pd.to_datetime(df['4'], format='%d.%m.%Y %H:%M:%S')
	newdf = (df['4'] >= afteryesterday) & (df['4'] <= today2)
	newdf = df.loc[newdf]
	newdf = len(newdf.index)
	total = (df['4'] > '2023.01.01 00:00:00') & (df['4'] <= today)
	total = len(total.index)

	print('Запрос от:', str(message.chat.first_name), 'ID:',str(message.chat.id))
	print('Сегодня:', today)
	print('Количество произведенных за вчерашний день: ', newdf)
	print('За 2023 год:', total)
	print("Операция выполнена за %s секунд" % (time.time() - start_time))

	bot.send_message(cid, f'Сегодня: {today}')
	bot.send_message(cid, f'Количество произведенных за вчерашний день:')
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
			elif call.data == 'Сегодня':
				format(callback_today(call.message))
			elif call.data == 'Период':
				format(period(call.message))
			elif call.data == 'Вчера':
				format(callback_yesterday(call.message))
			#удаляем инлайновую клаву
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Результат:",
				reply_markup=None)
			#Создаём уведомление
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
				text='Выполнено!')
	except Exception as e:
		print(repr(e))

bot.polling(none_stop=True)