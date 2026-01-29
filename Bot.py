
import requests
import json
import calendar
import time
import datetime
# import openpyxl
import pandas
answer = False
answerId = None
newsletter = False
contact = False
will = []
dont_will = []
wait = []
hitId = None
check = False
checkId = None
toall = False
toall_id = None
tousers_id = None
toadmins_id = None
tousers = False
toadmins = False
month = {1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня", 7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"}
reason = []


def numbers():
    cal = calendar.Calendar(firstweekday=0)
    now = datetime.datetime.now()
    
    month_days = cal.monthdatescalendar(now.year, now.month)
    
    for week in month_days:
        if any(day.day == now.day and day.month == now.month for day in week):
            return [day.day for day in week]

current_week = numbers()

def months(number):
    numbers()
    global answer_text
    answer_text = ""
    
    current_month = datetime.datetime.now().month
    
    if number in current_week:
        answer_text = str(number) + " " + month[current_month]
    else:
        if number < current_week[0]:
            answer_text = str(number) + " " + month[current_month]
        else:
            if current_month != 12:
                answer_text = str(number) + " " + month[current_month + 1]
            else:
                answer_text = str(number) + " " + month[1]
numbers()
months(current_week[0])
menu_token = "https://api.telegram.org/bot8356095124:AAGoWwGoIlyk9qvTAlcCi-RTTPJFv8T8TK8/setMyCommands"
menu = {
    "commands": [
        {"command": "myclasses", "description": "Предстоящие занятия"},
        {"command": "photo", "description": "Мои фотографии"},
        {"command": "pastevents", "description": "Фото с мероприятий"},
        {"command": "upcomingevents", "description": "Предстоящие мероприятия"},
        {"command": "contact", "description": "Связь с администратором"}
        # {"command": "trial", "description": "Записаться на пробное занятие"}
    ]
}
lastDay = 0
requests.post(menu_token, json=menu)
group1 = ["Wednesday", "Friday"]
group2 = ["Saturday"]
group3 = ["Saturday"]
group4 = ["Sunday"]
group5 = ["Sunday"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
TOKEN = "https://api.telegram.org/bot8356095124:AAGoWwGoIlyk9qvTAlcCi-RTTPJFv8T8TK8/SendMessage"
CHAT_ID = "8126089922"
SEND_DOCUMENT = "https://api.telegram.org/bot8356095124:AAGoWwGoIlyk9qvTAlcCi-RTTPJFv8T8TK8/sendDocument"
FORWARDMESSAGE = "https://api.telegram.org/bot8356095124:AAGoWwGoIlyk9qvTAlcCi-RTTPJFv8T8TK8/copyMessage"
DELETE_TOKEN = "https://api.telegram.org/bot8356095124:AAGoWwGoIlyk9qvTAlcCi-RTTPJFv8T8TK8/deleteMessage"
ADMIN_ID = "201479005"
GET_UPDATE_URL = "https://api.telegram.org/bot8356095124:AAGoWwGoIlyk9qvTAlcCi-RTTPJFv8T8TK8/getUpdates"
addUE = False
addUEId = None
inline_kb = {
    "inline_keyboard": [
        [
            {"text": "Я буду на занятии", "callback_data": "True"},
            {"text": "Я не буду на занятии", "callback_data": "False"}
        ]
    ]
}
isSended = False
stat_send_days = [2,4,5,6]
last_update_id = 0
surname = False
while True:
    try:
        respone = requests.get(GET_UPDATE_URL, params={"offset": last_update_id + 1}).json()
        updates = respone.get("result", [])

        for update in updates:
            last_update_id = update['update_id']
            try:
                text1 = update['message'].get("text", "")
            except KeyError:
                text1 = ""
            if text1 == "/contact":
                contact = True
                contact_id = update['message']['from'].get("id", "")
                requests.post(TOKEN, json={"chat_id": contact_id, "text": "Опишите Вашу проблему одним сообщением"})
                contact_name = update['message']['from'].get("username", "")
            elif not text1.startswith("/") and contact:
                message_id = update['message']['message_id']
                if update['message']['from']['id'] == contact_id:
                    requests.post(TOKEN, json={"chat_id": CHAT_ID, "text": f"Сообщений от {update['message']['from']['first_name']}, username: {update['message']['from']['username']}"})
                    requests.post(FORWARDMESSAGE, json={"from_chat_id": update['message']['from']['id'], "message_id": message_id, "chat_id": CHAT_ID})
                    requests.post(TOKEN, json={"chat_id": contact_id, "text": "Спасибо за обращение. Мы свяжемся с Вами в ближайшее время"})
                    contact = False
            
            
            if "callback_query" in update:
                c_id = str(update['callback_query']['from']['id'])
                choice = update['callback_query']['data'] 
                if choice in ["True", "False"]:
                    with open("info.json", "r+", encoding="utf8") as f:
                        data = json.load(f)
                        if c_id in data:
                            data[c_id]['status'] = choice 
                            f.seek(0)
                            json.dump(data, f, indent=4, ensure_ascii=False)
                            f.truncate()
                            requests.post(DELETE_TOKEN, json={"chat_id": c_id, "message_id": update['callback_query']['message']['message_id']})    
                            if choice == "False":
                                requests.post(TOKEN, json={"chat_id":c_id, "text": "Почему Вы не сможете прийти"})
                                answer = True
                                answerId = c_id
                            else:
                                requests.post(TOKEN, json={"chat_id": c_id, "text": "Спасибо за ответ"})
                    continue
                elif choice in ["g1", "g2", "g3", "g4", "g5"
                                
                                ]:
                    with open("info.json", "r+", encoding="utf8") as fill:
                        data = json.load(fill)
                        data[c_id]['trial'] = True
                        fill.seek(0)
                        json.dump(data, fill, indent=4, ensure_ascii=False)
                        fill.truncate()
                        requests.post(DELETE_TOKEN, json={"chat_id": c_id, "message_id": update['callback_query']['message']['message_id']})
                        requests.post(TOKEN, json={"chat_id": CHAT_ID, "text": f"Пользователь {update['callback_query']['from']['first_name']} с юзернеймом {update['callback_query']['from']['username']} хочет записаться на пробное занятие в группу номер {choice[1]}"})
                elif choice == "null":
                    requests.post(DELETE_TOKEN, json={"chat_id": c_id, "message_id": update['callback_query']['message']['message_id']})

            if "message" not in update:
                continue
            
            chat_id = str(update['message']['chat']['id'])

            with open("info.json", "r+", encoding="utf8") as file:
                try:
                    data = json.load(file)
                except:
                    data = {}
                if not text1.isdigit() and answer and chat_id == answerId and text1[0] != "/":
                    with open("answers.json", "r+") as fill:
                        info = json.load(fill)
                        info['o'].append({"surname": data[str(chat_id)]['surname'], "answer": text1})
                        fill.seek(0)
                        json.dump(info, fill, indent=4, ensure_ascii=False)
                        fill.truncate()
                        answer = False
                        requests.post(TOKEN, json={"chat_id": chat_id, "text": "Спасибо за ответ"})

                if text1 == "/toall":
                    if data[str(update['message']['from']['id'])]['admin'] == "True":
                        toall = True
                        toall_id = update['message']['from']['id']
                        requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": "Введите Ваше сообщение которое Вы хотите отправить всем"})
                
                if text1 == "/tousers":
                    if data[str(update['message']['from']['id'])]['admin'] == "True":
                        tousers = True
                        tousers_id = update['message']['from']['id']
                        requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": "Здравствуйте введите сообщение для пользователей"})

                if text1 != "/tousers" and tousers and data[str(update['message']['from']['id'])]['admin'] == "True" and update['message']['from']['id'] == tousers_id:
                    messageId = update['message']['message_id']
                    for i in data:
                        if data[i]['admin'] == "False":
                            date = {
                                "chat_id": i,
                                "from_chat_id": tousers_id,
                                "message_id": messageId
                            }
                            requests.post(FORWARDMESSAGE, data=date)
                    requests.post(TOKEN, json={"chat_id": tousers_id, "text": "рассылка окончена"}).json()
                    tousers = False
                if text1 != "/toall" and toall and data[str(update['message']['from']['id'])]['admin'] == "True" and update['message']['from']['id'] == toall_id:
                    messageId = update['message']['message_id']
                    for i in data:
                        date = {
                            "chat_id": i,
                            "from_chat_id": toall_id,
                            "message_id": messageId
                        }
                        requests.post(FORWARDMESSAGE, data=date)
                    requests.post(TOKEN, json={"chat_id": toall_id, "text": "Рассылка окончена"})
                    toall = False
                
                if text1 == "/toadmins" and data[str(update['message']['from']['id'])]['admin'] == "True":
                    toadmins = True
                    toadmins_id = update['message']['from']['id']
                    requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": "Введите Ваше сообщение для администраторов"})
                
                if text1 != "/toadmins" and toadmins and update['message']['from']['id'] == toadmins_id:
                    messageId = update['message']['message_id']
                    for i in data:
                        if data[i]['admin'] == "True":
                            date = {
                                "chat_id": i,
                                "from_chat_id": toadmins_id,
                                "message_id": messageId
                            }
                            requests.post(FORWARDMESSAGE, data=date)
                    requests.post(TOKEN, json={"chat_id": toadmins_id, "text": "Рассылка окончена"})
                    toadmins = False
                
                if text1 == "/help":
                    if data[str(update['message']['from']['id'])]['admin'] == "False":
                        requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": f"""Здравствуйте {update['message']['from']['first_name']}, вот Ваши команды: 
    /contact - связь с администратором,
    /myclasses - занятия на неделе,
    /photo - мои фотографии"""})
                    else:
                        requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": f"""Здравствуйте {update['message']['from']['first_name']}, вот Ваши команды:
    /toall - сообщение всем,
    /tousers - только пользователям,
    /toadmins - только администраторам,
    /contact - связь с техподдержкой,
    /myclasses - занятия на неделе,
    /photo - мои фотографии,
    /addupcomingevents - добавить предстоящие мероприятия,
    /upcomingevents - посмотреть предстоящие мероприятия,
    /check - посмотреть состояние учеников
    /trial - бета - функция записи на пробное занятие"""})
                
                

                if text1 == "/myclasses":
                    if str(update['message']['from']['id']) in data:
                        numbers()
                        if data[str(update['message']['from']['id'])]['group'] == 1:
                            datetime.datetime.now().weekday + 1
                            if today <= 2:
                                numbers()
                                months(current_week[2])
                                text2 = f"У Вас будет занятие {answer_text} 16:30-20:00 и "
                                numbers()
                                months(current_week[4])
                                text2 = text2 + f"{answer_text} 16:30-20:00"

                                requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": text2})
                            elif today <= 5:
                                requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": f"У Вас будет занятие {current_week[4]} {month[datetime.datetime.now().month]} 16:30 - 20:00"})
                            else:
                                requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": "У Вас на этой неделе больше не осталось занятий"})
                        elif data[str(update['message']['from']['id'])]['group'] == 2:
                            if today <= 6:
                                requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": f"У Вас занятие {current_week[5]} {month[datetime.datetime.now().month]} 11:00 - 15.00"})
                            else:
                                requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": "У Вас на этой неделе больше не осталось занятий"})
                        elif data[str(update['message']['from']['id'])]['group'] == 3:
                            if today <= 6:
                                requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": f"У Вас занятие {current_week[5]} {month[datetime.datetime.now().month]} 15.30 - 19:30"})
                            else:
                                requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": "У Вас на этой неделе больше не осталось занятий"})
                        elif data[str(update['message']['from']['id'])]['group'] == 4:
                            requests.post(TOKEN, json={"text": f"У Вас занятие {current_week[6]} {month[datetime.datetime.now().month]} 11:00 - 15:00", "chat_id": update['message']['from']['id'] })
                        else:
                            requests.post(TOKEN, json={"text": f"У Вас занятие {current_week[6]} {month[datetime.datetime.now().month]} 15:30 - 19:30", "chat_id": update['message']['from']['id'] })

                if text1 == "/pastevents":
                    requests.post(TOKEN, json={"chat_id": chat_id, "text": "Показы в которых мы участвовали: https://школакутюрье.рф/events"})

                if text1 == "/trial":
                    if data[str(update['message']['from']['id'])]['trial'] != True:
                        if str(update['message']['from']['id']) in data and data[str(update['message']['from']['id'])]['surname'] != None:
                            numbers()
                            today = datetime.datetime.now().weekday + 1
                            months(current_week[0])
                            g1 = 1000
                            # Поставьте 0 если хотите сделать так чтобы в первую группу можно было записаться
                            if data[str(update['message']['from']['id'])]['group'] == 1:
                                requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": "Извините но мы не поддерживаем пробные занятие в первой группе"})
                            # Удалите чтобы не Вылезало сообщение "Извините но мы не поддерживаем пробные занятие в первой группе"
                            g2 = 0
                            g3,g4,g5 = 0, 0, 0
                            for i in data:
                                if today <= 5:
                                    if data[i]['group'] == 1 and data[i]['status'] == "True":
                                        g1 += 1
                                elif today == 6:
                                    if data[i]['group'] == 2:
                                        g2 += 1
                                    elif data[i]['group'] == 3:
                                        g3 += 1
                                else:
                                    if data[i]['group'] == 4:
                                        g4 += 1
                                    elif data[i]['group'] == 5:
                                        g5 += 1
                            needed = min([g1, g2, g3, g4, g5])
                            if needed >= 10:
                                requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": "Извините все места заняты"})
                            else:
                                if g1 == needed:
                                    btn = {"inline_keyboard": [[
                                        {"text": f"Да", "callback_data": "g1"},
                                        {"text": "Нет", "callback_data": "null"}
                                    ]]}
                                    txt1 = {
                                        "chat_id": update['message']['from']['id'],
                                        "text": "Вы хотите записаться в группу 1?",
                                        "reply_markup": json.dumps(btn)

                                    }
                                elif g2 == needed:
                                    btn = {"inline_keyboard": [[
                                        {"text": f"Да", "callback_data": "g2"},
                                        {"text": "Нет", "callback_data": "null"}
                                    ]]}
                                    txt1 = {
                                        "chat_id": update['message']['from']['id'],
                                        "text": "Вы хотите записаться в группу 2?",
                                        "reply_markup": json.dumps(btn)

                                    }
                                elif g3 == needed:
                                    btn = {"inline_keyboard": [[
                                        {"text": f"Да", "callback_data": "g3"},
                                        {"text": "Нет", "callback_data": "null"}
                                    ]]}
                                    txt1 = {
                                        "chat_id": update['message']['from']['id'],
                                        "text": "Вы хотите записаться в группу 3?",
                                        "reply_markup": json.dumps(btn)

                                    }
                                elif g4 == needed:
                                    btn = {"inline_keyboard": [[
                                        {"text": f"Да", "callback_data": "g4"},
                                        {"text": "Нет", "callback_data": "null"}
                                    ]]}
                                    txt1 = {
                                        "chat_id": update['message']['from']['id'],
                                        "text": "Вы хотите записаться в группу 4?",
                                        "reply_markup": json.dumps(btn)

                                    }
                                else:
                                    btn = {"inline_keyboard": [[
                                        {"text": f"Да", "callback_data": "g5"},
                                        {"text": "Нет", "callback_data": "null"}
                                    ]]}
                                    txt1 = {
                                        "chat_id": update['message']['from']['id'],
                                        "text": "Вы хотите записаться в группу 5?",
                                        "reply_markup": json.dumps(btn)

                                    }
                                requests.post(TOKEN, json=txt1)
                        else:
                            requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": "Авторизуйтесь в боте пожалуйста"})
                    else:
                        requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": "Вы уже записывались на пробное занятие"})
                if text1 == "/upcomingevents":
                    with open("UE.json", "r") as fi:
                        data1 = json.load(fi)
                    if "upcomingevents" in data1 and len(data1['upcomingevents']) >= 1:
                        for j in range(len(data1['upcomingevents'])):
                            date = {"chat_id": chat_id,
                                    "from_chat_id": data1['upcomingevents'][j]['from_chat_id'],
                                    "message_id": data1['upcomingevents'][j]['message_id']
                                    }
                            requests.post(FORWARDMESSAGE, date)
                    else:
                        requests.post(TOKEN, json={"chat_id": chat_id, "text": "Пока что нету предстоящих мероприятий"})
                if text1 == "/addupcomingevents":
                    if data[str(chat_id)]['admin'] == "True":
                        addUEId = chat_id
                        addUE = True
                        requests.post(TOKEN, json={"chat_id": chat_id, "text": "Пришлите предстоящие мероприятие"})
                if not text1.startswith("/") and chat_id == addUEId and addUE:
                    with open("UE.json", "r+") as filling:
                        dat = json.load(filling)
                        dat['upcomingevents'].append({"from_chat_id": chat_id, "message_id": update['message']['message_id']})
                        filling.seek(0)
                        json.dump(dat, filling, ensure_ascii=False, indent=4)
                        filling.truncate()
                    requests.post(TOKEN, json={"chat_id": addUEId, "text": "Мероприятие успешно добавленно"})
                    addUE = False
                if text1 == "/photo":
                    if str(update['message']['from']['id']) in data:
                        if requests.get(f"https://disk.yandex.ru/d/Xl41T86IOxHYfg/{data[str(update['message']['from']['id'])]['surname']}").status_code <= 299 and requests.get(f"https://disk.yandex.ru/d/Xl41T86IOxHYfg/{data[str(update['message']['from']['id'])]['surname']}").status_code > 199:
                            requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": f"Здравствуйте, вот Ваша ссылка: https://disk.yandex.ru/d/Xl41T86IOxHYfg/{data[str(update['message']['from']['id'])]['surname']}"})
                        else:
                            requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": "Здравствуйте, у Вас нету папки на данный момент"})
                if text1 == "/check" and data[str(chat_id)]['admin'] == "True":
                    requests.post(TOKEN, json={"chat_id": chat_id, "text":"Введите дату которую хотите просмотреть"})
                    check = True
                    checkId = chat_id
                if check and chat_id == checkId and not text1.startswith("/") and int(float(text1)) in current_week:
                    check = False
                    checkId = None
                    df = pandas.DataFrame()
                    df.to_excel("status.xlsx", index=False)
                    usernames = []
                    surnames = []
                    statuses = []
                    groups = []
                    reasons = []
                    reason = []
                    for i in data:
                        r = False
                        if data[i]['lastDay'] in [int(float(text1)), int(float(text1)) - 1, int(float(text1)) - 2]:
                            usernames.append(data[i]['name'])
                            surnames.append(data[i]['surname'])
                            if data[i]['status'] == "True":
                                statuses.append("Будет")
                            elif data[i]['status'] == "sended":
                                statuses.append("Не ответил")
                            else:
                                statuses.append("Не будет")
                                with open("answers.json", "r") as d:
                                    content = json.load(d)['o']
                                    for n in range(len(content)):
                                        if content[n]['surname'] == data[i]['surname']:
                                            reason = content[n]['answer']
                                            r = True
                                    if reason != []:
                                        reasons.append(reason)
                            groups.append(data[i]['group'])
                            if not r:
                                reasons.append(" ")
                    if usernames:
                        dota = {"Юзер": usernames,
                                "Фамилия": surnames,
                                "Статус": statuses,
                                "Группа": groups,
                                "Причина": reasons}
                        df = pandas.DataFrame(dota)
                        df.to_excel("status.xlsx", engine="openpyxl", index=False)
                        with open("./status.xlsx", "rb") as do:
                            requests.post(
                                SEND_DOCUMENT, 
                                data={"chat_id": chat_id, "caption": "Вот статистика"}, 
                                files={"document": do}  
                            )
                    else:
                        requests.post(TOKEN, json={"chat_id": chat_id, "text": "На этот день нет учеников"})
                if text1 == "/secret":
                    requests.post(FORWARDMESSAGE, json={"chat_id": chat_id, "from_chat_id": "8126089922", "message_id": 1762}).json()
                if chat_id not in data:
                    text = update['message'].get("text", "")
                
                    if text.isdigit() and int(text) <= 5:
                        data[chat_id] = {
                            "group": int(text), 
                            "admin": "False", 
                            "status": "wait",
                            "surname": None, 
                            "name": update['message']['from'].get("username"),
                            "trial": False,                                   
                            "lastDay": 0
                            }       

                        file.seek(0) 
                        json.dump(data, file, indent=4, ensure_ascii=False)
                        file.truncate()
                        requests.post(TOKEN, json={"chat_id": chat_id, "text": "Группа сохранена!"})
                        requests.post(TOKEN, json={"chat_id": chat_id, "text": "Введите вашу фамилию"})
                        surname = True
                        hitId = update['message']['from']['id']
                    else:
                        requests.post(TOKEN, json={"chat_id": chat_id, "text": """Вас приветствует Школа Кутюрье! ✨
    Напишите номер группы (только цифру) в которую записан ребёнок или хотите записаться на пробное занятие:
    1 - среда+пятница 16.30-20.00
    2 - суббота 11.00-15.00
    3 - суббота 15.30-19.30
    4 - воскресенье 11.00-15.00
    5 - воскресенье 15.30-19.30"""})

            if not text1.isdigit() and not text1.startswith("/"):
                if surname:
                    if update['message']['from']['id'] == hitId:
                        with open("info.json", "r+") as file:
                            data = json.load(file)
                            data[str(update['message']['from']['id'])]['surname'] = text1
                            file.seek(0)
                            json.dump(data, file, ensure_ascii=False, indent=4)
                            surname = False
                            requests.post(TOKEN, json={"chat_id": update['message']['from']['id'], "text": "Фамилия сохранена"})

        today = datetime.datetime.now().weekday() + 1 
        now = datetime.datetime.now()

        with open("info.json", "r+", encoding="utf8") as fill:
            data = json.load(fill)
            try:
                months(current_week[today + 1])
            except Exception:
                months(current_week[today] + 1)
            for i in data:
                txt = {
                    "chat_id": i,
                    "text": f"Вы будете на занятии {answer_text}?",
                    "reply_markup": json.dumps(inline_kb)
                }
                if data[i]['lastDay'] in [int(datetime.datetime.now().day), int(datetime.datetime.now().day) + 1] or data[i]['surname'] == None or data[i]['admin'] == "True":
                    continue
                else:
                    if datetime.datetime.now().hour > 10 and datetime.datetime.now().hour < 22:
                        if data[i]['group'] == 1 and today in [1,2,3]:
                            requests.post(TOKEN, data=txt)
                            data[i]['status'] = "sended"
                            data[i]['lastDay'] = datetime.datetime.now().day
                            fill.seek(0)
                            json.dump(data, fill, indent=4, ensure_ascii=False)
                            fill.truncate()

                        elif (data[i]['group'] == 2 or data[i]['group'] == 3) and today in [4,5]:
                            requests.post(TOKEN, data=txt)
                            data[i]['status'] = "sended"
                            data[i]['lastDay'] = datetime.datetime.now().day
                            fill.seek(0)
                            json.dump(data, fill, indent=4, ensure_ascii=False)
                            fill.truncate()
                        elif (data[i]['group'] == 4 or data[i]['group'] == 5) and today in [5, 6]:
                            requests.post(TOKEN, data=txt)
                            data[i]['status'] = "sended"
                            data[i]['lastDay'] = datetime.datetime.now().day
                            fill.seek(0)
                            json.dump(data, fill, indent=4, ensure_ascii=False)
                            fill.truncate()
                
        if lastDay != today:
            if datetime.datetime.now().hour >= 10:
                df = pandas.DataFrame()
                df.to_excel("status.xlsx", index=False)
                usernames = []
                surnames = []
                statuses = []
                groups = []
                reasons = []
                for i in data:
                    r = False
                    if data[i]['lastDay'] in current_week:
                        usernames.append(data[i]['name'])
                        surnames.append(data[i]['surname'])
                        if data[i]['status'] == "True":
                            statuses.append("Будет")
                        elif data[i]['status'] == "sended":
                            statuses.append("Не ответил")
                        else:
                            statuses.append("Не будет")
                            with open("answers.json", "r") as d:
                                content = json.load(d)['o']
                                for n in range(len(content)):
                                    if content[n]['surname'] == data[i]['surname']:
                                        reason = content[n]['answer']
                                        r = True
                                if reason != []:
                                    reasons.append(reason)
                        groups.append(data[i]['group'])
                        if not r:
                            reasons.append(" ")
                dota = {"Юзер": usernames,
                        "Фамилия": surnames,
                        "Статус": statuses,
                        "Группа": groups,
                        "Причина": reasons}
                df = pandas.DataFrame(dota)
                df.to_excel("status.xlsx", engine="openpyxl", index=False)
                with open("./status.xlsx", "rb") as do:
                    requests.post(
                        SEND_DOCUMENT, 
                        data={"chat_id": CHAT_ID, "caption": "Вот статистика"}, 
                        files={"document": do}  
                    )
                lastDay = today

        time.sleep(1)
    except Exception as e:
        print(e)
        #asdasdasdasdad asdadasda