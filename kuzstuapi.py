import requests
import json
import datetime

emoji_dict = {1: "1️⃣", 2:"2️⃣", 3:"3️⃣", 4:"4️⃣", 5:"5️⃣", 6:"6️⃣"}
weekday_dict = {0:"Понедельник",1:"Вторник",2:"Среда",3:"Четверг",4:"Пятница",5:"Суббота",6:"Воскресенье"}
lesson_dict = {1:"09:00-10:30", 2:"10:50-12:20", 3:"13:20-14:50", 4:"15:10-16:40", 5:"17:00-18:30", 6:"18:50-20:20"}

def get_group_schedule(_group_name):
    try:
        group_id = requests.get("https://portal.kuzstu.ru/api/group?group={}".format(_group_name)).text
        group_id = json.loads(group_id)
        group_name = group_id[0]['name']
        group_id = group_id[0]["dept_id"]
        site = requests.get("https://portal.kuzstu.ru/api/student_schedule?group_id={}".format(group_id)).text
        site = json.loads(site)
    except Exception as ex:
        print("get_group_schedule’",ex)
        site = "Неверная группа"
        group_name = _group_name
    return (site, group_name)

def reform_group_schedule(_group_name, date):
    schedule = get_group_schedule(_group_name)
    group_name = schedule[1]
    schedule = schedule[0]
    schedule = pars_group_schedule(schedule)
    for i in schedule:
        for j in i:
            if date in j:
                return make_group_schedule_nice(i)
            else:
                continue
    return "🌥Пар нет, отдыхаем"

def make_group_schedule_nice(schedule):
    separator = "-------------------------------------"
    weekday = weekday_dict.get(datetime.datetime.strptime(schedule[0][-1], "%Y-%m-%d").weekday())
    schedule_str = "📅*{}* {} на {}:\n\n".format(weekday,schedule[0][1], schedule[0][-1])
    for i in schedule:
        if int(i[6]) != 0:
            schedule_str += f"*{emoji_dict.get(int(i[4]))} {lesson_dict.get(int(i[4]))}*\n{i[9]}\n_{i[10]}, ауд.{i[5]} {i[6]} п/г_\n*{i[8]}*\n{separator}\n"
        else:
            schedule_str += f"*{emoji_dict.get(int(i[4]))} {lesson_dict.get(int(i[4]))}*\n{i[9]}\n_{i[10]}, ауд.{i[5]}_\n*{i[8]}*\n{separator}\n"
    return schedule_str

# {0'id': '5728015', 1'education_group_name': 'ИСт-222', 2'education_group_id': '6460', 3'day_number': '2', 
# 4'lesson_number': '4', 5'place': '5505', 6'subgroup': '0', 7'teacher_id': '101041', 8'teacher_name': 'Клавецка Т.Я.', 
# 9'subject': 'Астрономия', 10'type': 'л.', 11'date_lesson': '2023-02-28'}

def pars_group_schedule(schedule):
    day_list = []
    schedule_list = []
    datelesson = schedule[0]["date_lesson"]
    for i in schedule:
        if i["date_lesson"] == datelesson:
            day_list.append(list(i.values()))
        else:
            schedule_list.append(day_list)
            day_list = []
            day_list.append(list(i.values()))
            datelesson = i["date_lesson"]
    return schedule_list

#print(get_group_schedule("ист-222"))
#print(reform_group_schedule("ист-222", "2023-02-27"))