from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.types import ParseMode, BotCommand, InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
import config
import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
import logging
import os
#Добавить условия для except

path = os.path.dirname(os.path.abspath(__file__)) + "//"
os.chdir(path)

bot = Bot(token="5814136143:AAGkvr2qyx6F0nYrbARQL4-s9PAINKiuTyc")
dp = Dispatcher(bot, storage=MemoryStorage())
grouplist = {}
teacherlist = {}


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/today", description="Расписание на сегодня"),
        BotCommand(command="/tomorrow", description="Расписание на завтра"),
        BotCommand(command="/date", description="Расписание на дату"),
        BotCommand(command="/teacher_today", description="Расписание пр. на сегодня"),
        BotCommand(command="/teacher_tomorrow", description="Расписание пр. на завтра"),
        BotCommand(command="/teacher_date", description="Расписание пр. на дату"),
        BotCommand(command="/about", description="Основная информация о боте")
    ]
    await bot.set_my_commands(commands)

logging.basicConfig(level=logging.INFO)

#-----------------------------------------------------------------------------------------
class ChangeData(StatesGroup):
    waiting_for_group_name = State()
    waiting_for_teacher_surname = State()
    waiting_for_teacher_group = State()
    waiting_for_place = State()
#-----------------------------------------------------------------------------------------

@dp.message_handler(commands="group", state="*")
async def ask_group(message: types.Message, state: FSMContext):
    await message.answer("🗒Введите группу:")
    await state.set_state(ChangeData.waiting_for_group_name.state)

@dp.callback_query_handler(text="student")
async def ask_groupe(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("🗒Введите группу:")
    await state.set_state(ChangeData.waiting_for_group_name.state)

@dp.message_handler(state=ChangeData.waiting_for_group_name)
async def change_group(message: types.Message, state: FSMContext):
    await state.update_data(group_name = message.text.lower())
    group_name = await state.get_data()
    group_name = group_name.get("group_name")
    try:
        sch = config.get_group_schedule(group_name)
        group_name = sch[0].get("education_group_name")
        a = []
        a.append(group_name)
        grouplist[message.from_id] = a
        await message.answer("✅Группа успешно изменена на {}".format(group_name))
        await state.finish()
    except Exception as ex:
        print(ex)
        await message.reply("Такой группы нет, повторите попытку😔")
        return

@dp.message_handler(commands="cancel", state=ChangeData.waiting_for_group_name)
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Смена группы отменена")


#-----------------------------------------------------------------------------------------


@dp.message_handler(commands="teacher", state="*")
async def ask_teacher_surname(message: types.Message, state: FSMContext):
    await message.answer("🗒Введите группу, в которой преподаёт преподаватель:")
    await state.set_state(ChangeData.waiting_for_teacher_group.state)

@dp.callback_query_handler(text="teacher")
async def ask_groupe(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("🗒Введите группу, в которой преподаёт преподаватель:")
    await state.set_state(ChangeData.waiting_for_teacher_group.state)

@dp.message_handler(state=ChangeData.waiting_for_teacher_group)
async def change_teacher_group(message: types.Message, state: FSMContext):
    await state.update_data(teacher_group = message.text.lower())
    try:
        teacher_group_name = await state.get_data()
        teacher_group_name = teacher_group_name.get("teacher_group")
        sch = config.get_group_schedule(teacher_group_name)
        teacher_group = sch[0].get("education_group_name")
        print(sch)
        a = []
        a.append(teacher_group)
        teacherlist[message.from_id] = a
        await message.answer("Определённая группа: {}\n🗒Введите фамилию преподавателя:".format(teacher_group))
        await state.set_state(ChangeData.waiting_for_teacher_surname.state)
    except Exception as ex:
        print(ex, "teacher ex")
        await message.answer("Такой группы нет, повторите попытку😔")
        return

@dp.message_handler(state=ChangeData.waiting_for_teacher_surname)
async def change_teacher_surname(message: types.Message, state: FSMContext):
    await state.update_data(teacher_surname = message.text.lower())
    group_name = teacherlist.get(message.from_id)[0]
    teacher_surname = await state.get_data()
    teacher_surname = teacher_surname.get("teacher_surname")
    try:
        sch = config.get_teacher_schedule(teacher_surname ,group_name)
        a = teacherlist.get(message.from_id)
        a.append(teacher_surname)
        teacherlist[message.from_id] = a
        await message.answer("✅Преподаватель успешно изменён на {}".format(str(teacher_surname).capitalize()))
        await state.finish()
    except Exception as ex:
        print(ex)
        await message.answer("Такого преподавателя нет, повторите попытку😔")
        return

@dp.message_handler(commands="cancel", state=ChangeData.waiting_for_teacher_surname)
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Смена преподавателя отменена")


#-----------------------------------------------------------------------------------------


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await set_commands(bot)
    buttons = [
        types.InlineKeyboardButton(text="Студент", callback_data="student"),
        types.InlineKeyboardButton(text="Преподаватель", callback_data="teacher")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    photo = InputFile("16752191029290.png")
    await message.answer_photo(photo=photo,caption="👋 Привет, {}!\n\n❓Чьё расписание ты хочешь получить?".format(message.from_user.username), reply_markup=keyboard)

@dp.message_handler(commands=['about'])
async def process_start_command(message: types.Message):
    await message.answer("💠Бот ~Ева~ Валл\-И позволяет удобно находить расписание *группы* или *преподавателя*\n\n📅Бот разрабатывается *на протяжении недели*\n👨‍🔧Командой из *одного человека*\n🐍На языке программирования *Python*",parse_mode=ParseMode.MARKDOWN_V2)


@dp.message_handler(commands=['Сегодня', "today"])
async def send_today_schedule(message: types.Message):
    schedule = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    #schedule = text(emojize(schedule))
    try:
        await message.reply(config.make_list_great(grouplist.get(message.from_id)[0],str(datetime.datetime.now().strftime('%Y-%m-%d'))), parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте группу\n/group")

@dp.message_handler(commands=['Завтра', "tomorrow"])
async def send_tomorrow_schedule(message: types.Message):
    schedule = config.make_day_greater(date=datetime.datetime.now())
    try:
        await message.reply(config.make_list_great(grouplist.get(message.from_id)[0],(schedule)),parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте группу\n/group")

@dp.message_handler(commands=['Дата', "date"])
async def send_bydate_schedule(message: types.Message):
    try:
        await message.reply(config.make_list_great(grouplist.get(message.from_id)[0],str(datetime.datetime.strptime(str(message.get_args()), "%d.%m").replace(year=datetime.datetime.now().year).strftime("%Y-%m-%d"))),parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте группу\n/group")


#-----------------------------------------------------------------------------------------

@dp.message_handler(commands=['teacher_today'])
async def send_teacher_today_schedule(message: types.Message):
    try:
        await message.reply(config.make_teacherlist_great(teacherlist.get(message.from_id)[1],str(datetime.datetime.now().strftime('%Y-%m-%d')), teacherlist.get(message.from_id)[0]), parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте учителя\n/set_teacher *Фамилия*")
    
@dp.message_handler(commands=['teacher_tomorrow'])
async def send_teacher_tomorrow_schedule(message: types.Message):
    schedule = config.make_day_greater(date=datetime.datetime.now())
    try:
        await message.reply(config.make_teacherlist_great(teacherlist.get(message.from_id)[1],schedule, teacherlist.get(message.from_id)[0]), parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте учителя\n/set_teacher *Фамилия*")

@dp.message_handler(commands=['teacher_date'])
async def send_teacher_date_schedule(message: types.Message):
    try:
        await message.reply(config.make_teacherlist_great(teacherlist.get(message.from_id)[1],str(datetime.datetime.strptime(str(message.get_args()), "%d.%m").replace(year=datetime.datetime.now().year).strftime("%Y-%m-%d")), teacherlist.get(message.from_id)[0]), parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте учителя\n/set_teacher *Фамилия*")
#-----------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------


@dp.message_handler(commands=["place"])
async def send_place_today_schedule(message: types.Message):
    try:
        await message.reply(config.make_placelist_great(message.get_args(),str(datetime.datetime.now().strftime('%Y-%m-%d'))), parse_mode=ParseMode.HTML)
    except Exception as ex:
        print(ex)
        await message.reply("Введите номер кабинета через пробел")


#-----------------------------------------------------------------------------------------


if __name__ == '__main__':
    executor.start_polling(dp)