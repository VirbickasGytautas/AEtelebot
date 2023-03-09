import telebot
from telebot import types
import datetime
from datetime import datetime, timedelta
import time
import pandas as pd
import logging
import schedule
from threading import Thread
import glob
from pathlib import Path

#Логгирование
logging.basicConfig(level=logging.DEBUG, filename="log\log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")
#TODO Настроить логгирование

bot = telebot.TeleBot("5941676589:AAExTrhG3aZCkG13obkHyzPE-Z8F5NTxq_A") #API телеграмм бота
today = datetime.today().strftime('%Y.%m.%d %H:%M:%S')

#Файлы csv
DSP_file_00 = r'\\pk-55\CSV\tmpID.csv' #статистика с ДСП
DSP_file_01 = r'\\pk-55\ID_QR_enter\РАБОЧАЯ\CSV\tmpID.csv' #статистика с ДСП, другое ПО
#TODO Добавить объединение файлов csv

file_tune_41 = r'\\pk-41\stend\epsgranta_ipmstend_new\.arch' #статистика настройки БУ РМ41

#PSI_01 =
#PSI_02 =
#PSI_03 =
#PSI_04 =
#PSI_05 =
#PSI_06 =

#TODO Добавить статистику со стендов ПСИ
#TODO Добавить статистику со стендов настройки блока управления

#Белый список
list = [440032806,415077278,376187604,905566669,-815383918,1759649548]

#376187604 - Илья Билокур		|	#415077278 - dev
#1759649548 - Андрей Зозуля		|	#905566669 - Дмитрий Ульянов
#440032806 - Руслан Рустамович	|	#415077278, -81538391 - AE STA группа

#Авторизация через белый список
@bot.message_handler(commands=['start'])
def check_user(message):
	userID = message.chat.id
	userName = message.chat.first_name
	print(userName, userID)
	if userID in list:
		print('Авторизация', userID, userName)
		send_welcome(message)
	else:
		chatid = 415077278
		userID = message.chat.id
		userName = message.chat.first_name
		bot.forward_message(chatid, message.chat.id, message.message_id, userID, userName)
		stic = open('stic/ar.webp', 'rb')
		bot.send_message(message.chat.id, 'Доступ ограничен')
		bot.send_sticker(message.chat.id, stic)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		but1 = types.KeyboardButton("Помощь")
		markup.add(but1)
		bot.reply_to(message, "Здравствуй, {0.first_name}\nДля авторизации обратитесь к разработчику"
					 .format(message.from_user), reply_markup=markup)
		bot.send_message(chatid, userID, userName)
		return

@bot.message_handler(commands=['full'])
def fullreport(message):
	doc = open(DSP_file_01)
	bot.send_document(message.chat.id, doc)

#Рассылка в группу
groupID = -81538391
#TODO Добавить рассылку в группу

#Приветственное сообщение в группе
@bot.message_handler(commands=['post'])
def command(message):
    if message.text.split(" ", 1)[0] == "/post":
        bot.send_message(groupID, message.text.split(" ", 1)[1])
@bot.message_handler(content_types=['new_chat_members'])
def handler_new_member(message):
    user_name = message.new_chat_members[0].first_name
    bot.send_message(message.chat.id, f"Добро пожаловать!, {user_name}! \nДля начала взаимодействия с ботом, напишите /start")

#Начало использования
def send_welcome(message):
	stic = open('stic/welcome.webp', 'rb')
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	but1 = types.KeyboardButton("Статистика УУР")
	but2 = types.KeyboardButton("Статистика БиД")
	but3 = types.KeyboardButton("Отчеты по качеству")
	but4 = types.KeyboardButton("Помощь")
	markup.add(but1, but2, but3, but4)
	bot.reply_to(message, "{0.first_name}, Добро пожаловать!\nБот в режиме разработки, многие функции недоступны"
				 .format(message.from_user), parse_mode='html', reply_markup=markup)
	bot.send_sticker(message.chat.id, stic)

#Обработка команды help
@bot.message_handler(commands=['help'])
def help(message):
	cid2 = message.chat.id
	stic = open('stic/help.webp', 'rb')
	bot.send_sticker(message.chat.id, stic)
	help_message = bot.send_message(cid2, 'Пожалуйста, опишите вашу проблему:')
	bot.register_next_step_handler(help_message, message_to_help)

def message_to_help(message):
	chatid = 415077278
	help_message = bot.send_message(message.chat.id, 'Ваше сообщение отправлено разработчику')
	bot.forward_message(chatid, message.chat.id, message.message_id)

#Команда остановки
@bot.message_handler(commands=['stp'])
def stop_command(message):
	userID = message.chat.id
	userName = message.chat.first_name
	print(userName, userID)
	if userID == 415077278:
		print("Бот остановлен", userID, userName)
		bot.send_message(415077278,'Бот будет остановлен')
		bot.stop_polling()
	else:
		bot.send_message('Доступ ограничен')

@bot.message_handler(commands=['ask'])
def Ask(message):
	pythoncom.CoInitializeEx(0)
	office = win32com.client.Dispatch("Excel.Application")
	wb = office.Workbooks.Open(r"C:\Users\g.virbitskas\PycharmProjects\AEtelebot\экспорт.xlsx")
	print('Открыт файл')
	count = wb.Sheets.Count
	try:
		for i in range(count):
			ws = wb.Worksheets[i]
			ws.Unprotect()
			pivotCount = ws.PivotTables().Count
			for j in range(1, pivotCount + 1):
				ws.PivotTables(j).PivotCache().Refresh()
				print('Обновлено')
	except:
		print('Ошибка обработки файла')

#Обработка нажатий меню
@bot.message_handler(func=lambda message: True)
def menu(message):
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
		but2 = types.InlineKeyboardButton("Динамика дефектов на УУР", callback_data='Отчет2')
		but3 = types.InlineKeyboardButton("ТОП дефектов на УУР", callback_data='Отчет3')
		but4 = types.InlineKeyboardButton("Гарантия за весь период", callback_data='Отчет4')
		inMurkup.add(but1, but2, but3, but4)
		bot.send_message(message.chat.id, "Текущие отчеты по качеству:", reply_markup=inMurkup)
	elif message.text == "Статистика БиД":
		stic = open('stic/dev.webp', 'rb')
		bot.send_sticker(message.chat.id, stic)

	elif message.text == "Помощь":
		help(message)
	else:
		bot.send_message(message.chat.id, "Я не знаю что и ответить")

#Объявление переменной содержащее конец периода
def stepSD(message):
	cid = message.chat.id
	global uSD
	uSD = message.text
	uED = str
	print(uSD)
	bot.send_message(cid, "Сохранил!")
	msgED = bot.send_message(cid,'Введите дату *КОНЦА* периода в формате гггг.мм.дд Ч:М:С\n'
								 '(Пример 2023.01.02 07:00:00):', parse_mode= 'Markdown')
	bot.register_next_step_handler(msgED, stepED)

#Объявление переменной содержащее начало периода
def period(message):
	cid = message.chat.id
	msgSD = bot.send_message(cid, 'Введите дату *НАЧАЛА* периода в формате гггг.мм.дд Ч:М:С\n'
								  '(Пример 2023.02.17 07:00:00):', parse_mode= 'Markdown')
	bot.register_next_step_handler(msgSD, stepSD)

#Переход на обработку результата
def stepED(message):
	cid = message.chat.id
	global uED
	uED = message.text
	uSD = str
	print(uED)
	bot.send_message(cid, "Сохранил!")
	msgRD = bot.send_message(cid, "Подождите около минуты")
	resultRD(message)

#Обработка csv за произвольный период
def resultRD(message):
	try:
		start_time = time.time()
		stic = open('stic/error.webp', 'rb')
		cid = message.chat.id
		print('С', uSD, 'По', uED)
		df = pd.read_csv(DSP_file_00, index_col=0, sep=';', names=['1', '2', '3', '4', '5'], on_bad_lines='skip')
		df['4'] = pd.to_datetime(df['4'], format='%d.%m.%Y %H:%M:%S')

		fullnewdf = (df['4'] >= uSD) & (df['4'] <= uED)
		fullnewdf = df.loc[fullnewdf]
		fullnewdf = len(fullnewdf.index)
		total = (df['4'] > '2023.01.01 00:00:00') & (df['4'] <= today)
		total = len(total.index)
		#TODO Обработка CSV по парт-номерам
		#TODO Обработка нескольких CSV

		print('Запрос от:', str(message.chat.first_name), 'ID:',str(message.chat.id))
		print('Сегодня:', today)
		print('Количество произведенных за выбранный период: ',fullnewdf)
		print('За 2023 год:', total )
		bot.send_message(cid,f'Количество произведенных за выбранный период: \nС {uSD} по {uED}')
		bot.send_message(cid, fullnewdf)
		# Опрос пользователя о необходимости отправки полного отчета
		inMurkup = types.InlineKeyboardMarkup(row_width=1)
		but1 = types.InlineKeyboardButton("Да", callback_data='Да')
		but2 = types.InlineKeyboardButton("Нет", callback_data='Нет')
		inMurkup.add(but1, but2)
		bot.send_message(message.chat.id, "Получить подробный отчет за 2023 год?", reply_markup=inMurkup)
		return today
	except:
		print('Ошибка ввода данных')
		bot.send_message(cid, 'Ошибка ввода данных')
		bot.send_message(cid, 'Возможно вы ввели некорректно даты периодов, попробуйте снова')
		bot.send_sticker(cid, stic)

#Обработка csv за сегодня
def callback_today(message):
	start_time = time.time()
	cid = message.chat.id
	today2 = datetime.today().strftime('%Y.%m.%d %H:%M:%S')
	yesterday = datetime.today() - timedelta(days=1)
	yesterday = yesterday.strftime('%Y.%m.%d')
	print(today2, yesterday)
	df = pd.read_csv(DSP_file_00, index_col=0, sep=';', names=['1', '2', '3', '4', '5'], on_bad_lines='skip')
	df['4'] = pd.to_datetime(df['4'], format='%d.%m.%Y %H:%M:%S')
	newdf = (df['4'] >= datetime.today().strftime('%Y.%m.%d')) & (df['4'] <= today2)
	newdf = df.loc[newdf]
	newdf = len(newdf.index)
	total = (df['4'] > '2023.01.01 00:00:00') & (df['4'] <= today)
	total = len(total.index)

	#----------КОСТЫЛЬ ДЛЯ 2х ФАЙЛОВ CSV----------------
	df2 = pd.read_csv(DSP_file_01, index_col=0, sep=';', names=['1', '2', '3', '4', '5'], on_bad_lines='skip')
	df2['4'] = pd.to_datetime(df2['4'], format='%d.%m.%Y %H:%M:%S')
	newdf2 = (df2['4'] >= datetime.today().strftime('%Y.%m.%d')) & (df2['4'] <= today2)
	newdf2 = df2.loc[newdf2]
	newdf2 = len(newdf2.index)
	newdf3 = newdf2 + newdf

	#logging.debug('Запрос от:', str(message.chat.first_name), str(message.chat.id))
	print('Запрос от:', str(message.chat.first_name), 'ID:',str(message.chat.id))
	print('Сегодня:', today2)
	print('Количество произведенных: ',newdf3)
	print('За 2023 год:', total)
	print("Операция выполнена за %s секунд" % (time.time() - start_time))

	bot.send_message(cid, f'Сегодня: {today2}')
	bot.send_message(cid, "Количество произведенных: ")
	bot.send_message(cid, newdf3)
	return today2

#Обработка csv за вчерашний день
def callback_yesterday(message):
	start_time = time.time()
	cid = message.chat.id
	today2 = datetime.today()
	today2 = today2.strftime('%Y.%m.%d')
	afteryesterday = datetime.today() - timedelta(days=1)
	afteryesterday= afteryesterday.strftime('%Y.%m.%d')
	print(today2, afteryesterday)
	df = pd.read_csv(DSP_file_00, index_col=0, sep=';', names=['1', '2', '3', '4', '5'], on_bad_lines='skip')
	df['4'] = pd.to_datetime(df['4'], format='%d.%m.%Y %H:%M:%S')
	newdf = (df['4'] >= afteryesterday) & (df['4'] <= today2)
	newdf = df.loc[newdf]
	newdf = len(newdf.index)
	total = (df['4'] > '2023.01.01 00:00:00') & (df['4'] <= today)
	total = len(total.index)

	print('Запрос от:', str(message.chat.first_name), 'ID:',str(message.chat.id))
	print('Сегодня:', today)
	print('Количество произведенных за вчерашний день: ',newdf)
	print('За 2023 год:', total)
	print("Операция выполнена за %s секунд" % (time.time() - start_time))

	bot.send_message(cid, f'Сегодня: {today}')
	bot.send_message(cid, f'Количество произведенных за вчерашний день:')
	bot.send_message(cid, newdf)
	return today

#обработка callback
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'Отчет1':
				img = open('report/Дефекты за 2022 год.jpg', 'rb')
				bot.send_photo(call.message.chat.id, img)
			elif call.data == 'Отчет2':
				img = open('report/Динамика.jpg','rb')
				bot.send_photo(call.message.chat.id, img)
			elif call.data == 'Отчет3':
				img = open('report/Топ.jpg','rb')
				bot.send_document(call.message.chat.id, img)
			elif call.data == 'Отчет4':
				img = open('report/Гарантия.jpg', 'rb')
				bot.send_document(call.message.chat.id, img)
			#TODO Сделать обработку полного отчета и отсылать картинку с диаграммой статистики
			elif call.data == 'Да':
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
									  text="Подождите ~20 секунд",
									  reply_markup=None)
				try:
					img = open('image.png', 'rb')
					bot.send_photo(call.message.chat.id, img)
				except:
					bot.send_message(call.message.chat.id, 'Ошибка отправки отчета')
			elif call.data == 'Нет':
				bot.send_message(call.message.chat.id, 'Отмена отправки отчета')
			elif call.data == 'Сегодня':
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
									  text="Подождите...",
									  reply_markup=None)
				format(callback_today(call.message))
			elif call.data == 'Период':
				format(period(call.message))
			elif call.data == 'Вчера':
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
									  text="Подождите...",
									  reply_markup=None)
				format(callback_yesterday(call.message))
			#удаляем инлайновую клаву
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Результат:",
				reply_markup=None)
			#Создаём уведомление
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
				text='Выполнено!')
	except Exception as e:
		print(repr(e))

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(e)
        time.sleep(15)
#bot.polling(none_stop=True)