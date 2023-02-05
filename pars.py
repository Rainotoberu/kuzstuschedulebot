from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ParseMode
import config
import datetime

#Добавить условия для except

bot = Bot(token="5814136143:AAGkvr2qyx6F0nYrbARQL4-s9PAINKiuTyc")
dp = Dispatcher(bot)
userlist = {}

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Ку")

@dp.message_handler(commands=['set_group'])
async def echo_message(message: types.Message):
    try:
        a = []
        a.append(message.text.split()[1])
        userlist[message.from_id] = a
        await message.answer("Группа была изменена на {}".format(userlist.get(message.from_id)[0]))
    except:
        await message.answer("Группа не указана")

@dp.message_handler(commands=['Сегодня', "today"])
async def send_today_schedule(message: types.Message):
    schedule = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    #schedule = text(emojize(schedule))
    try:
        await message.reply(config.make_list_great(userlist.get(message.from_id)[0],str(datetime.datetime.now().strftime('%Y-%m-%d'))), parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте группу\n/set_group *Название*")

@dp.message_handler(commands=['Завтра', "tomorrow"])
async def send_tomorrow_schedule(message: types.Message):
    schedule = config.make_day_greater(date=datetime.datetime.now())
    try:
        await message.reply(config.make_list_great(userlist.get(message.from_id)[0],(schedule)),parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте группу\n/set_group *Название*")

@dp.message_handler(commands=['Дата', "date"])
async def send_bydate_schedule(message: types.Message):
    try:
        await message.reply(config.make_list_great(userlist.get(message.from_id)[0],str(datetime.datetime.strptime(str(message.get_args()), "%d.%m").replace(year=datetime.datetime.now().year).strftime("%Y-%m-%d"))),parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте группу\n/set_group *Название*")

@dp.message_handler(commands=["set_teacher"])
async def set_teacher_name(message: types.Message):
    try:
        if type(userlist.get(message.from_id)[0]) == str:
            a = userlist.get(message.from_id)
            try:
                a[1] = message.text.split()[1]
            except:
                a.append(message.text.split()[1])
            userlist[message.from_id] = a 
            await message.reply("Преподаватель был изменён на {}".format(userlist[message.from_id][1]))
    except IndexError:
        await message.reply("Напишите фамилию преподавателя через пробел")
    except:
        await message.reply("Сначала добавьте группу, в которой преподаёт преподаватель\n/set_group *Название*")

@dp.message_handler(commands=['teacher_today'])
async def send_teacher_today_schedule(message: types.Message):
    try:
        await message.reply(config.make_teacherlist_great(userlist.get(message.from_id)[1],str(datetime.datetime.now().strftime('%Y-%m-%d')), userlist.get(message.from_id)[0]), parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте учителя\n/set_teacher *Фамилия*")
    
@dp.message_handler(commands=['teacher_tomorrow'])
async def send_teacher_tomorrow_schedule(message: types.Message):
    schedule = config.make_day_greater(date=datetime.datetime.now())
    try:
        await message.reply(config.make_teacherlist_great(userlist.get(message.from_id)[1],schedule, userlist.get(message.from_id)[0]), parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте учителя\n/set_teacher *Фамилия*")

@dp.message_handler(commands=['teacher_date'])
async def send_teacher_date_schedule(message: types.Message):
    try:
        await message.reply(config.make_teacherlist_great(userlist.get(message.from_id)[1],str(datetime.datetime.strptime(str(message.get_args()), "%d.%m").replace(year=datetime.datetime.now().year).strftime("%Y-%m-%d")), userlist.get(message.from_id)[0]), parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте учителя\n/set_teacher *Фамилия*")

@dp.message_handler(commands=["place"])
async def send_place_today_schedule(message: types.Message):
    try:
        await message.reply(config.make_placelist_great(message.get_args(),str(datetime.datetime.now().strftime('%Y-%m-%d'))), parse_mode=ParseMode.HTML)
    except Exception as ex:
        print(ex)
        await message.reply("Введите номер кабинета через пробел")

if __name__ == '__main__':
    executor.start_polling(dp)