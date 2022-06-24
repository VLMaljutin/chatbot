import psycopg2
import time
from datetime import datetime, timedelta
from random import randint

# Подключение к базе данных
con = psycopg2.connect(
    database="chatbot",
    user="postgres",
    password="1234",
    host="127.0.0.1",
    port="5432"
)

# Списки с эмоциями
list_happy = ["😀", "😃", "😄", "😁", "😆", "😉", "😊", "🤩", "🥳"]
list_sad = ["😒", "😔", "😞", "😟", "😤", "☹", "😩", "😡", "😓"]
list_anger = ["👿", "😭", "🤬", "💩", "👺", "💀", "😠", "🤯", "🤨"]

# Списки, которые будут использоваться в добавлении записей в бд
list_messages = []
list_time = []
list_id = []


# Главная функция
def main():
    print("Доброго времени суток, Вас Приветствует EmojiChatBot")
    id_client = login()
    prev = ""  # Предыдущее сообщение
    start = datetime.now()  # Старт сессии
    while True:
        tic = time.perf_counter()
        message = input("Клиент: ")
        list_messages.append(message)
        list_time.append(datetime.now())
        toc = time.perf_counter()
        if toc - tic < 60:
            if message in list_happy:
                happy(prev, message)
                prev = message
            elif message in list_sad:
                sad(prev, message)
                prev = message
            elif message in list_anger:
                anger(prev, message)
                prev = message
            elif message == "end":
                end = datetime.now()
                sql_request(start, end, id_client, list_messages, list_time)
                print("До Свидания!!!")
                return False
            else:
                print("Я тебя не понимаю")
                end = datetime.now()
                sql_request(start, end, id_client, list_messages, list_time)
                start = datetime.now()
                prev = ""
                list_messages.clear()
                list_time.clear()
        else:
            print("Сообщений не было больше минуты, сессия завершена")
            end = start + timedelta(minutes=1)
            sql_request(start, end, id_client, list_messages, list_time)
            start = datetime.now()
            prev = ""
            list_messages.clear()
            list_time.clear()


# Если эмоция из группы "Радость"
def happy(prev, message):
    if prev == "":
        return {
            list_happy[0]: lambda: print("Привет, я рад, что ты улыбаешься"),
            list_happy[1]: lambda: print("Привет, я рад, что ты в хорошем настроении"),
            list_happy[2]: lambda: print("Привет, я рад, что ты в хорошем расположении духа"),
            list_happy[3]: lambda: print("Привет, я рад, что ты смеёшься"),
            list_happy[4]: lambda: print("Привет, я рад видеть твою улыбку"),
            list_happy[5]: lambda: print("Привет, интересно, с кем ты заигрываешь?"),
            list_happy[6]: lambda: print("Привет, вижу ты сияешь"),
            list_happy[7]: lambda: print("Привет, ты сегодня прямо звезда!!!"),
            list_happy[8]: lambda: print("Привет, что празднуем?")
        }.get(message, lambda: print('Я не знаю такой эмоции('))()
    elif prev in list_happy:
        print("Хорошо,что продолжаешь быть в хорошем настроении")
    elif prev in list_sad:
        print("Хорошо, что ты теперь не грустишь")
    elif prev in list_anger:
        print("Хорошо, что ты перестал злиться")


# Если эмоция из группы "Грусть"
def sad(prev, message):
    if prev == "":
        return {
            list_sad[0]: lambda: print("Привет, почему ты грустный?"),
            list_sad[1]: lambda: print("Привет, почему ты грустишь?"),
            list_sad[2]: lambda: print("Привет, кто тебя обидел?"),
            list_sad[3]: lambda: print("Привет, не грусти, пожалуйста"),
            list_sad[4]: lambda: print("Привет, выпусти пар"),
            list_sad[5]: lambda: print("Привет, не тоскуй"),
            list_sad[6]: lambda: print("Привет, не плачь, пожалуйста"),
            list_sad[7]: lambda: print("Привет, ты весь красный!!!"),
            list_sad[8]: lambda: print("Привет, вижу на твоём лице уныние(")
        }.get(message, lambda: print("Я не знаю такой эмоции("))()
    elif prev in list_happy:
        print("Почему ты стал грустным?")
    elif prev in list_sad:
        print("Почему ты продолжаешь быть грустным?")
    elif prev in list_anger:
        print("Видимо, тебе немного полегчало, но ты всё равно грустишь(")


# Если эмоция из группы "Злость"
def anger(prev, message):
    if prev == "":
        return {
            list_anger[0]: lambda: print("Привет, почему ты такой злой!!!"),
            list_anger[1]: lambda: print("Привет, почему ты рыдаешь???"),
            list_anger[2]: lambda: print("Привет, не ругайся, тут же дети!!!"),
            list_anger[3]: lambda: print("Привет, кажется, у тебя проблемы с животом"),
            list_anger[4]: lambda: print("Привет, мне кажется, этим пугают детей"),
            list_anger[5]: lambda: print("Привет, о нет..."),
            list_anger[6]: lambda: print("Привет, почему ты злишься?"),
            list_anger[7]: lambda: print("Привет, твоя голова скоро лопнет"),
            list_anger[8]: lambda: print("Привет, ты какой-то хмурый")
        }.get(message, lambda: print("Я не знаю такой эмоции("))()
    elif prev in list_happy:
        print("Я вижу, что твоё настроение значительно ухудшилось(((")
    elif prev in list_sad:
        print("Тебе стало ещё хуже(")
    elif prev in list_anger:
        print("Почему ты всё ещё злишься?")


# Добавление записей в бд
def sql_request(start_session, end_session, id_client, messages, times):
    sql_session = ("""INSERT INTO table_session(startsession, endsession) 
                    VALUES(%s,%s) RETURNING Id""")
    cur.execute(sql_session, (start_session, end_session))
    session_id = cur.fetchone()[0]
    sql_messages = ("""INSERT INTO table_message(timemessage, idsession, message, idclient)
                        VALUES(%s,%s,%s,%s) RETURNING Id""")
    i = 0
    while i < len(messages):
        cur.execute(sql_messages, (times[i], session_id, messages[i], id_client))
        i = i + 1
    con.commit()


# Своего рода регистрация (выдача id клиенту)
def login():
    while True:
        id_client = int(
            input("Введите ваш id (если вы пользуетесь ботом впервые или не помните свой id, введите 0) : "))
        if id_client != 0:
            cur.execute("SELECT idclient from table_message")
            rows = cur.fetchall()
            for row in rows:
                list_id.append(row[0])
            for i in list_id:
                if id_client == i:
                    print("Пользуйтесь ботом, для того чтобы закончить общение введите end")
                    return id_client
                else:
                    print("Вы ввели неправильный id")
        elif id_client == 0:
            id_client = randint(0, 100000)
            j = 0
            while j < len(list_id):
                if id_client == list_id[j]:
                    id_client = randint(0, 100000)
                    j = 0
            print(f"Ваш id {id_client}")
            print("Пользуйтесь ботом, для того чтобы закончить общение введите end")
            return id_client


cur = con.cursor()
main()
cur.close()
