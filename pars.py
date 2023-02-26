from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.types import ParseMode, BotCommand, InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
import kuzstuapi
import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
import logging
import os
import config
#Добавить условия для except

path = os.path.dirname(os.path.abspath(__file__)) + "//"
os.chdir(path)

bot = Bot(token="6046839961:AAGXl_r-RpnHrG8qRgVOiO8tq8IP9fpJE0Y")
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

grouplist = {}
teacherlist = {}
statelist = {}

cancel_keyboard = types.InlineKeyboardMarkup()
cancel_button = types.InlineKeyboardButton(text="Отменить", callback_data="cancel")
cancel_keyboard.add(cancel_button)

GroupKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
Group_Buttons = [
    types.KeyboardButton(text="📗Сегодня📗"),
    types.KeyboardButton(text="📘Завтра📘"),
    types.KeyboardButton(text="⚙️Сменить группу⚙️"),
    types.KeyboardButton(text="⚙️Доп. Возможности⚙️"),
    types.KeyboardButton(text="🎓Студент🎓")
]
GroupKeyboard.row(Group_Buttons[0], Group_Buttons[1])
GroupKeyboard.row(Group_Buttons[2], Group_Buttons[3])
GroupKeyboard.add(Group_Buttons[4])

TeacherKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
Teacher_Buttons = [
    types.KeyboardButton(text="📗Сегодня📗"),
    types.KeyboardButton(text="📘Завтра📘"),
    types.KeyboardButton(text="⚙️Сменить преподавателя⚙️"),
    types.KeyboardButton(text="⚙️Доп. Возможности⚙️"),
    types.KeyboardButton(text="✏️Преподаватель✏️")
]
TeacherKeyboard.row(Teacher_Buttons[0], Teacher_Buttons[1])
TeacherKeyboard.row(Teacher_Buttons[2], Teacher_Buttons[3])
TeacherKeyboard.add(Teacher_Buttons[4])

AdditionalKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
AdditionalKeys = [
    types.KeyboardButton(text="📕На неделю📕"),
    types.KeyboardButton(text="🚪По кабинету🚪"),
    types.KeyboardButton(text="◀️Назад◀️")
]
AdditionalKeyboard.row(AdditionalKeys[0], AdditionalKeys[1])
AdditionalKeyboard.add(AdditionalKeys[2])

def return_log(message):
    print(datetime.datetime.now(), message.from_user.first_name, message.from_user.last_name, message.text)

#-----------------------------------------------------------------------------------------
class ChangeData(StatesGroup):
    waiting_for_group_name = State()
    waiting_for_teacher_surname = State()
    waiting_for_teacher_group = State()
    waiting_for_place = State()
#-----------------------------------------------------------------------------------------

@dp.message_handler(commands="group", state="*")
async def ask_group(message: types.Message, state: FSMContext):
    await message.answer("🗒Введите группу:", reply_markup=cancel_keyboard)
    await state.set_state(ChangeData.waiting_for_group_name.state)

@dp.callback_query_handler(text="student")
async def ask_groupe(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("🗒Введите группу:", reply_markup=cancel_keyboard)
    await call.answer()
    await state.set_state(ChangeData.waiting_for_group_name.state)

@dp.callback_query_handler(text="cancel", state=ChangeData)
async def cancel_action(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Изменения отменены")
    await call.answer()
    await state.finish()

@dp.message_handler(state=ChangeData.waiting_for_group_name)
async def change_group(message: types.Message, state: FSMContext):
    await state.update_data(group_name = message.text.lower())
    group_name = await state.get_data()
    group_name = group_name.get("group_name")
    await message.answer("🔎Ищу группу в каталоге...")
    try:
        sch = config.get_group_name(group_name)
        group_name = sch
        a = []
        a.append(group_name)
        grouplist[message.from_id] = a
        await message.answer("✅Группа успешно изменена на {}".format(group_name), reply_markup=GroupKeyboard)
        statelist[message.from_id] = "student"
        await state.finish()
    except Exception as ex:
        print(ex)
        await message.answer("😔Такой группы нет, напишите ещё раз", reply_markup=cancel_keyboard)
        return


#-----------------------------------------------------------------------------------------

@dp.callback_query_handler(text="return")
async def return_to_teacher_group(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("🗒Введите группу, в которой преподаёт преподаватель:", reply_markup=cancel_keyboard)
    await call.answer()
    await state.set_state(ChangeData.waiting_for_teacher_group.state)

@dp.message_handler(commands="teacher", state="*")
async def ask_teacher_surname(message: types.Message, state: FSMContext):
    await message.answer("🗒Введите группу, в которой преподаёт преподаватель:", reply_markup=cancel_keyboard)
    await state.set_state(ChangeData.waiting_for_teacher_group.state)

@dp.callback_query_handler(text="teacher")
async def ask_teacher_surnamee(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("🗒Введите группу, в которой преподаёт преподаватель:", reply_markup=cancel_keyboard)
    await call.answer()
    await state.set_state(ChangeData.waiting_for_teacher_group.state)


@dp.message_handler(state=ChangeData.waiting_for_teacher_group)
async def change_teacher_group(message: types.Message, state: FSMContext):
    await state.update_data(teacher_group = message.text.lower())
    try:
        teacher_group_name = await state.get_data()
        teacher_group_name = teacher_group_name.get("teacher_group")
        sch = config.get_group_name(teacher_group_name)
        teacher_group = sch
        a = []
        a.append(teacher_group)
        teacherlist[message.from_id] = a
        await message.answer("✅Определённая группа: {}\n🗒Введите фамилию преподавателя:".format(teacher_group), reply_markup=cancel_keyboard)
        await state.set_state(ChangeData.waiting_for_teacher_surname.state)
    except Exception as ex:
        print(ex, "teacher ex")
        await message.answer("😔Такой группы нет, напишите ещё раз", reply_markup=cancel_keyboard)
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
        await message.answer("✅Преподаватель успешно изменён на {}".format(str(teacher_surname).capitalize()), reply_markup=TeacherKeyboard)
        statelist[message.from_id] = "teacher"
        await state.finish()
    except Exception as ex:
        print(ex)
        await message.answer("😔Такого преподавателя нет, повторите попытку", reply_markup=cancel_keyboard)
        return


#-----------------------------------------------------------------------------------------

@dp.message_handler(state=ChangeData.waiting_for_place)
async def change_teacher_group(message: types.Message, state: FSMContext):
    await state.update_data(teacher_group = message.text.lower())
    schedule = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    try:
        if statelist[message.from_id] == "student":
            await message.answer(config.make_placelist_great(message.text, schedule), reply_markup=GroupKeyboard, parse_mode=ParseMode.HTML)
        elif statelist[message.from_id] == "teacher":
            await message.answer(config.make_placelist_great(message.text, schedule), reply_markup=TeacherKeyboard, parse_mode=ParseMode.HTML)
        await state.finish()
    except Exception as ex:
        print(ex)
        await message.answer("😔Такой аудитории нет, повторите попытку")
        return

#-----------------------------------------------------------------------------------------


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    statelist[message.from_id] = "student"
    buttons = [
        types.InlineKeyboardButton(text="Студент", callback_data="student"),
        types.InlineKeyboardButton(text="Преподаватель", callback_data="teacher")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    photo = InputFile("16752191029290.png")
    await message.answer("💜*Бот Райа* \- твой надёжный помощник в мире расписания КузГТУ\n💫*Индивидуальный проект по информатике*\n\n👨‍💻Бот разрабатывается на протяжении *недели*", parse_mode=ParseMode.MARKDOWN_V2, reply_markup=types.ReplyKeyboardRemove())
    await message.answer_photo(photo=photo,caption="👋 Привет, {}!\n\n❓Чьё расписание ты хочешь получить?".format(message.from_user.username),reply_markup=keyboard)

@dp.message_handler(commands=['about'])
async def about_bot(message: types.Message):
    await message.answer("💜*Бот Райа* \- твой надёжный помощник в мире расписания КузГТУ\n💫*Индивидуальный проект по информатике*\n\n👨‍💻Бот разрабатывается на протяжении *недели*", parse_mode=ParseMode.MARKDOWN_V2)


@dp.message_handler(text="📗Сегодня📗")
async def send_today_schedule(message: types.Message):
    schedule = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    try:
        if statelist[message.from_id] == "student":
            try:
                await message.reply(kuzstuapi.reform_group_schedule(grouplist.get(message.from_id)[0],schedule), parse_mode=ParseMode.MARKDOWN)
            except:
                await message.reply("Сначала добавьте группу")
        elif statelist[message.from_id] == "teacher":
            try:
                await message.reply(config.make_teacherlist_great(teacherlist.get(message.from_id)[1],schedule, teacherlist.get(message.from_id)[0]), parse_mode=ParseMode.HTML)
            except:
                await message.reply("Сначала добавьте преподавателя")
    except:
        await process_start_command(message=message)

@dp.message_handler(text="📘Завтра📘")
async def send_tomorrow_schedule(message: types.Message):
    schedule = config.make_day_greater(date=datetime.datetime.now())
    try:
        if statelist[message.from_id] == "student":
            try:
                await message.reply(kuzstuapi.reform_group_schedule(grouplist.get(message.from_id)[0],(schedule)),parse_mode=ParseMode.MARKDOWN)
            except:
                await message.reply("Сначала добавьте группу")
        elif statelist[message.from_id] == "teacher":
            try:
                await message.reply(config.make_teacherlist_great(teacherlist.get(message.from_id)[1], schedule, teacherlist.get(message.from_id)[0]), parse_mode=ParseMode.HTML)
            except Exception as ex:
                print(ex)
                await message.reply("Сначала добавьте преподавателя")
    except:
        await process_start_command(message=message)

@dp.message_handler(text="📕На неделю📕")
async def send_today_schedule(message: types.Message):
    try:
        if statelist[message.from_id] == "student":
            try:
                await message.reply(kuzstuapi.reform_week_group_schedule(grouplist.get(message.from_id)[0]), parse_mode=ParseMode.MARKDOWN)
            except:
                await message.reply("Сначала добавьте группу")
        elif statelist[message.from_id] == "teacher":
            try:
                await message.reply(config.make_teacherweek_list_great(teacherlist.get(message.from_id)[1], teacherlist.get(message.from_id)[0]), parse_mode=ParseMode.HTML)
            except:
                await message.reply("Сначала добавьте преподавателя")
    except:
        await process_start_command(message=message)

"""@dp.message_handler(commands=['Дата', "date"])
async def send_bydate_schedule(message: types.Message):
    try:
        await message.reply(config.make_list_great(grouplist.get(message.from_id)[0],str(datetime.datetime.strptime(str(message.get_args()), "%d.%m").replace(year=datetime.datetime.now().year).strftime("%Y-%m-%d"))),parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте группу\n/group")"""


#-----------------------------------------------------------------------------------------

"""@dp.message_handler(commands=['teacher_date'])
async def send_teacher_date_schedule(message: types.Message):
    try:
        await message.reply(config.make_teacherlist_great(teacherlist.get(message.from_id)[1],str(datetime.datetime.strptime(str(message.get_args()), "%d.%m").replace(year=datetime.datetime.now().year).strftime("%Y-%m-%d")), teacherlist.get(message.from_id)[0]), parse_mode=ParseMode.HTML)
    except:
        await message.reply("Сначала добавьте учителя\n/set_teacher *Фамилия*")"""

#-----------------------------------------------------------------------------------------

@dp.message_handler(text="🎓Студент🎓")
async def ChangeStateTo_Teacher(message: types.Message):
    statelist[message.from_id] = "teacher"
    await message.answer("✏️Режим изменён на: Преподаватель✏️", reply_markup=TeacherKeyboard)

@dp.message_handler(text="✏️Преподаватель✏️")
async def ChangeStateTo_Teacher(message: types.Message):
    statelist[message.from_id] = "student"
    await message.answer("🎓Режим изменён на: Студент🎓", reply_markup=GroupKeyboard)

@dp.message_handler(text="⚙️Сменить группу⚙️")
async def ChangeGroupTo(message: types.Message, state: FSMContext):
    await ask_group(message=message, state=state)

@dp.message_handler(text="⚙️Сменить преподавателя⚙️")
async def ChangeTeacherTo(message: types.Message, state: FSMContext):
    await ask_teacher_surname(message=message, state=state)

@dp.message_handler(text="⚙️Доп. Возможности⚙️")
async def Open_AdditionalSettings(message: types.Message, state: FSMContext):
    await message.answer("⚙️Открыто меню доп. возможностей⚙️", reply_markup=AdditionalKeyboard)

@dp.message_handler(text="◀️Назад◀️")
async def Back_toMenu(message: types.Message, state: FSMContext):
    if statelist[message.from_id] == "student":
        await message.answer("⚙️Меню доп. возможностей закрыто⚙️", reply_markup=GroupKeyboard)
    elif statelist[message.from_id] == "teacher":
         await message.answer("⚙️Меню доп. возможностей закрыто⚙️", reply_markup=TeacherKeyboard)
    else:
        process_start_command(message)

@dp.message_handler(text="🚪По кабинету🚪")
async def Wait_ToPlace(message: types.Message, state: FSMContext):
    await message.answer("Введите номер кабинета:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ChangeData.waiting_for_place.state)

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