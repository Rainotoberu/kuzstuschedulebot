import requests
import json
import datetime

emoji_dict = {1: "1️⃣", 2:"2️⃣", 3:"3️⃣", 4:"4️⃣", 5:"5️⃣", 6:"6️⃣"}
weekday_dict = {0:"Понедельник",1:"Вторник",2:"Среда",3:"Четверг",4:"Пятница",5:"Суббота",6:"Воскресенье"}
lesson_dict = {1:"09:00-10:30", 2:"10:50-12:20", 3:"13:20-14:50", 4:"15:10-16:40", 5:"17:00-18:30", 6:"18:50-20:20"}

def get_group_schedule(group_name):
    group_url = "https://portal.kuzstu.ru/api/group?group={}".format(group_name)
    group_id = json.loads(requests.get(group_url).text)[0]['dept_id']
    url = "https://portal.kuzstu.ru/api/student_schedule?group_id={}".format(group_id)
    site = requests.get(url).text
    site = json.loads(site)
    return site

def gen_lessons_list(group_name):
    try:
        site = get_group_schedule(group_name)
    except:
        print("!ERROR!")
        pass
    daylist = []
    test_list = []
    last_i = int(site[0]['day_number'])
    for i in site:
        if int(i['day_number']) == last_i:
            test_list.append(pars_schedule(i, None))
        else:
            daylist.append(test_list)
            test_list = []
            test_list.append(pars_schedule(i, None))
            if last_i >= 5:
                last_i = 1
            else:
                last_i += 1
    return daylist

def pars_schedule(i, full_teacher_name):
    a_list = []
    a_list.append(i['education_group_name'])
    a_list.append(i['lesson_number'])
    a_list.append(i['type'])
    a_list.append(i['subject'])
    try:
        a_list.append(i['teacher_name'])
    except:
        a_list.append(full_teacher_name)
    a_list.append(i['subgroup'])
    a_list.append(i['place'])
    a_list.append(i['date_lesson'])
    try:
        a_list.append(i['teacher_id'])
    except:
        a_list.append(None)
    #print(a_list)
    #print(i['teacher_id'])
    return a_list


def print_datelessons(group_name,date):
    daylist = gen_lessons_list(group_name)
    for i in daylist:
        for j in i:
            if j[-2] == date:
                return (i)

def print_weeklessons(group_name):
    a = []
    today = datetime.datetime.now()
    start = today - datetime.timedelta(days=today.weekday())
    end = start.strftime('%Y-%m-%d')
    daylist = gen_lessons_list(group_name)
    for q in range(0,6):
        for i in daylist:
            b = []
            for j in i:
                #print(j[-2])
                if j[-2] == end:
                    a.append(i)
                    start = start + datetime.timedelta(days=1)
                    end = start.strftime('%Y-%m-%d')
                    break
    return a

def make_week_list_great(group_name):
    try:
        today = datetime.datetime.now()
        start = today - datetime.timedelta(days=today.weekday())
        end = start + datetime.timedelta(days=4)
        list = print_weeklessons(group_name)
        #print(list)
        great_str = ""
        great_list = []
        separator = "-------------------------------------"
        a = []
        b = []
        for j in list:
            great_list = []
            for k in j:
                if int(k[5]) != 0:
                    great_str = ("{} <b>{}</b>\n{}\n<i>{}, ауд.{} {} п/г</i>\n<b>{}</b>\n{}\n".format(emoji_dict.get(int(k[1])), lesson_dict.get(int(k[1])),k[3], k[2], k[6], k[5],k[4], separator))
                else:
                    great_str = ("{} <b>{}</b>\n{}\n<i>{}, ауд.{}</i>\n<b>{}</b>\n{}\n".format(emoji_dict.get(int(k[1])), lesson_dict.get(int(k[1])),k[3], k[2], k[6],k[4], separator))
                great_list.append(great_str)
            a.append(great_list)
        
        b.append("📅 <b>{} - {} {}:</b>\n\n".format(start.strftime("%d-%m-%Y"), end.strftime("%d-%m-%Y"), list[0][0][0]))
        for i in a:
            b.append("🗓 {} <b>{}</b>\n{}\n\n".format(start.strftime("%d-%m-%Y"),weekday_dict.get(int(datetime.datetime.weekday(start))),"".join(i)))
            start = start + datetime.timedelta(days=1)
        return("".join(b))
    except Exception as ex:
        a = "Неверная группа"
        return a

def make_list_great(group_name,date):
    try:
        if group_name != int:
            list = print_datelessons(group_name, date)
            great_str = ""
            great_list = []
            separator = "-------------------------------------"
            for i in list:
                if int(i[5]) != 0:
                    great_str = ("{} <b>{}</b>\n{}\n<i>{}, ауд.{} {} п/г</i>\n<b>{}</b>\n{}\n".format(emoji_dict.get(int(i[1])), lesson_dict.get(int(i[1])),i[3], i[2], i[6], i[5],i[4], separator))
                else:
                    great_str = ("{} <b>{}</b>\n{}\n<i>{}, ауд.{}</i>\n<b>{}</b>\n{}\n".format(emoji_dict.get(int(i[1])), lesson_dict.get(int(i[1])),i[3], i[2], i[6], i[4], separator))
                great_list.append(great_str)
                weekday = weekday_dict.get(datetime.datetime.strptime(i[-2], "%Y-%m-%d").weekday())
            a = ("📅{} {} {}:\n\n".format("<b>{}</b>".format(weekday),date, group_name), "\n".join(great_list))
            a = "".join(a)
            return a
        else:
            raise Exception("integer group")
    except Exception as ex:
        a = "Недоступная дата"
        return a

def get_group_name(group_name):
    url="https://portal.kuzstu.ru/api/group?group={}".format(str(group_name))
    site = requests.get(url).text
    site = json.loads(site)
    full_group_name = site[0]["name"]
    return full_group_name

#-------------------------------------------------------------

def get_teacher_schedule(teacher_name, group_name):
    teacher_id = list(get_teacher_id(teacher_name, group_name))
    url = "https://portal.kuzstu.ru/api/teacher_schedule?teacher_id={}".format(teacher_id[0])
    site = requests.get(url).text
    site = json.loads(site)
    return [site, teacher_id[1]]

def get_teacher_id(teacher_name, group_name):
    daylist = gen_lessons_list(group_name)
    for i in daylist:
        for j in i:
            if j[4].split()[0].lower() == teacher_name.lower():
                return [j[-1], j[4]]
                break   

def gen_teacher_list(teacher_namee, group_name):
    try:
        schedule = get_teacher_schedule(teacher_namee, group_name)
        site = schedule[0]
        full_teacher_name = schedule[1]
    except:
        print("!ERROR!")
        pass
    daylist = []
    test_list = []
    last_i = int(site[0]['day_number'])
    for i in site:
        if int(i['day_number']) == last_i:
            test_list.append(pars_schedule(i, full_teacher_name))
        else:
            daylist.append(test_list)
            test_list = []
            test_list.append(pars_schedule(i, full_teacher_name))
            if last_i >= 5:
                last_i = 1
            else:
                last_i += 1
    return daylist

def print_dateteacher(teacher_name,date, group_name):
    daylist = gen_teacher_list(teacher_name, group_name)
    a = []
    for i in daylist:
        for j in i:
            if j[-2] == date:
                a.append(j)
    return a

def print_weekteacher(teacher_name,group_name):
    a = []
    today = datetime.datetime.now()
    start = today - datetime.timedelta(days=today.weekday())
    end = start.strftime('%Y-%m-%d')
    daylist = gen_teacher_list(teacher_name, group_name)
    for q in range(0,6):
        for i in daylist:
            b = []
            for j in i:
                #print(j[-2])
                if j[-2] == end:
                    a.append(i)
                    start = start + datetime.timedelta(days=1)
                    end = start.strftime('%Y-%m-%d')
                    break
    return a

def make_teacherlist_great(teacher_name,date, group_name):
    try:
            list = print_dateteacher(teacher_name, date, group_name)
            full_teacher_name = list[0][4]
            great_str = ""
            great_list = []
            separator = "-------------------------------------"
            for i in list:
                if int(i[5]) != 0:
                    great_str = ("{} <b>{}</b>\n{}\n<i>{}, ауд.{} {} п/г</i>\n<b>{}</b>\n{}\n".format(emoji_dict.get(int(i[1])), lesson_dict.get(int(i[1])),i[3], i[2], i[6], i[5],i[0], separator))
                else:
                    great_str = ("{} <b>{}</b>\n{}\n<i>{}, ауд.{}</i>\n<b>{}</b>\n{}\n".format(emoji_dict.get(int(i[1])), lesson_dict.get(int(i[1])),i[3], i[2], i[6], i[0], separator))
                great_list.append(great_str)
            great_list = sorted(great_list, key=lambda lesson_number: int(lesson_number[0][0]))
            a = ("📅{} {}:\n".format(date, full_teacher_name), "\n".join(great_list))
            a = "".join(a)
            return a
    except Exception as ex:
        a = "Фамилия преподавателя указана неверно, либо преподаватель не преподаёт у данной группы"
        return a

def make_teacherweek_list_great(teacher_name,group_name):
    try:
        today = datetime.datetime.now()
        start = today - datetime.timedelta(days=today.weekday())
        end = start + datetime.timedelta(days=4)
        list = print_weekteacher(teacher_name,group_name)
        #print(list)
        great_str = ""
        great_list = []
        separator = "-------------------------------------"
        a = []
        b = []
        for j in list:
            great_list = []
            for k in j:
                if int(k[5]) != 0:
                    great_str = ("{} <b>{}</b>\n{}\n<i>{}, ауд.{} {} п/г</i>\n<b>{}</b>\n{}\n".format(emoji_dict.get(int(k[1])), lesson_dict.get(int(k[1])),k[3], k[2], k[6], k[5],k[0], separator))
                else:
                    great_str = ("{} <b>{}</b>\n{}\n<i>{}, ауд.{}</i>\n<b>{}</b>\n{}\n".format(emoji_dict.get(int(k[1])), lesson_dict.get(int(k[1])),k[3], k[2], k[6], k[0], separator))
                great_list.append(great_str)
                great_list = sorted(great_list, key=lambda lesson_number: int(lesson_number[0][0]))
            a.append(great_list)
        b.append("📅 <b>{} - {} {}:</b>\n\n".format(start.strftime("%d-%m-%Y"), end.strftime("%d-%m-%Y"), list[0][0][4]))
        for i in a:
            b.append("🗓 {} <b>{}</b>\n{}\n\n".format(start.strftime("%d-%m-%Y"),weekday_dict.get(int(datetime.datetime.weekday(start))),"".join(i)))
            start = start + datetime.timedelta(days=1)
        return("".join(b))
    except Exception as ex:
        a = "Неверная группа"
        return a

#-------------------------------------------------------------

def get_place_schedule(place_id):
    site = requests.get("https://portal.kuzstu.ru/api/classroom_schedule?classroom={}".format(place_id)).text
    site = json.loads(site)
    return site

def gen_place_list(place_id):
    try:
        schedule = get_place_schedule(place_id)
        site = schedule
    except:
        print("!ERROR!")
        pass
    daylist = []
    test_list = []
    last_i = int(site[0]['day_number'])
    for i in site:
        if int(i['day_number']) == last_i:
            test_list.append(pars_schedule(i, None))
        else:
            daylist.append(test_list)
            test_list = []
            test_list.append(pars_schedule(i, None))
            if last_i >= 5:
                last_i = 1
            else:
                last_i += 1
    return daylist

def print_dateplace(place_id, date):
    daylist = gen_place_list(place_id)
    for i in daylist:
        for j in i:
            if j[-2] == date:
                return (i)
                break

def make_placelist_great(place_id, date):
    try:
            list = print_dateplace(place_id, date)
            place_name = list[0][6]
            great_str = ""
            great_list = []
            separator = "-------------------------------------"
            for i in list:
                if int(i[5]) != 0:
                    great_str = ("{} <b>{}</b>\n{}\n<i>{}, ауд.{} {} п/г</i>\n<b>{}</b>\n{}\n".format(emoji_dict.get(int(i[1])), lesson_dict.get(int(i[1])),i[3], i[2], i[6], i[5],i[0], separator))
                else:
                    great_str = ("{} <b>{}</b>\n{}\n<i>{}, ауд.{}</i>\n<b>{}</b>\n{}\n".format(emoji_dict.get(int(i[1])), lesson_dict.get(int(i[1])),i[3], i[2], i[6], i[0], separator))
                great_list.append(great_str)
            great_list = sorted(great_list, key=lambda lesson_number: int(lesson_number[0][0]))
            a = ("📅<b>{} {}:</b>\n\n".format(date, place_name), "\n".join(great_list))
            a = "".join(a)
            return a
    except Exception as ex:
        print(ex)
        a = "Ошибка?"
        return a

#-------------------------------------------------------------

def make_day_greater(date):
    great_date = datetime.datetime.now() + datetime.timedelta(days=1)
    great_date = great_date.strftime('%Y-%m-%d')
    return str(great_date)

#-------------------------------------------------------------

#print(print_weekteacher("Ощепкова", "ист-222")[2])
#print(make_teacherweek_list_great("Ощепкова", "ист-222"))
#print(make_week_list_great("ист-222"))
#print(get_group_name("ист-222"))
#print(get_institutes())
#print(make_placelist_great("5512", "2023-02-02"))
#print(print_dateplace("5512", "2023-02-02"))
#print(make_placelist_great(place_id, date))
#print(get_teacher_schedule("Ощепкова", "ист-222"))
#print(print_dateteacher("Ощепкова Е.А.", "2023-02-01"))
#print(get_teacher_id("Ощепкова", "Ист-222")
#print(make_list_great("ист-222","2023-02-27"))
#print(make_teacherlist_great("Пилин","2023-02-03", "эмт-191"))
#print(print_dateteacher("Ощепкова", "2023-02-01"))
print(make_week_list_great("ТЭб-201"))
#print(daylist)
#print(site)
#site = site.encode().decode("unicode-escape")
#print(json.loads(requests.get("https://portal.kuzstu.ru/api/teachers?teacher=").text))