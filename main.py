import psycopg2
from datetime import datetime, timedelta
import time
from random import randint

con = psycopg2.connect(
    database="chatbot",
    user="postgres",
    password="1234",
    host="127.0.0.1",
    port="5432"
)
list_happy = ["😀", "😃", "😄", "😁", "😆", "😀", "😊", "🤩", "🥳"]
list_sad = ["😒", "😔", "😞", "😟", "😤", "☹", "😩", "😡", "😓"]
list_anger = ["👿", "😭", "🤬", "💩", "👺", "💀", "😠", "🤯", "🤨"]
list_messages = []
list_time = []
list_id = []


def main():
    id_client = login()
    prev = ""
    start = datetime.now()
    while True:
        tic = time.perf_counter()
        message = input("Клиент: ")
        list_messages.append(message)
        list_time.append(datetime.now())
        toc = time.perf_counter()
        if toc - tic < 60:
            if message in list_happy:
                happy(prev)
                prev = message
            elif message in list_sad:
                sad(prev)
                prev = message
            elif message in list_anger:
                anger(prev)
                prev = message
            elif message == "end":
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


def happy(prev):
    if prev == "":
        print("Привет, я рад что у тебя хорошее настроение")
    elif prev in list_happy:
        print("Хорошо,что продолжаешь быть в хорошем настроении")
    elif prev in list_sad:
        print("Хорошо, что ты теперь не грустишь")
    elif prev in list_anger:
        print("Хорошо, что ты перестал злиться")


def sad(prev):
    if prev == "":
        print("Привет, почему ты грустный?")
    elif prev in list_happy:
        print("Почему ты стал грустным?")
    elif prev in list_sad:
        print("Почему ты продолжаешь быть грустным?")
    elif prev in list_anger:
        print("Видимо, тебе немного полегчало, но ты всё равно грустишь(")


def anger(prev):
    if prev == "":
        print("Привет, почему ты злой?")
    elif prev in list_happy:
        print("Я вижу, что твоё настроение значительно ухудшилось(((")
    elif prev in list_sad:
        print("Тебе стало ещё хуже(")
    elif prev in list_anger:
        print("Почему ты всё ещё злишься?")


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


def login():
    while True:
        id_client = int(input("Введите ваш id (если вы пользуетесь ботом впервые, введите 0) : "))
        if id_client != 0:
            cur.execute("SELECT idclient from table_message")
            rows = cur.fetchall()
            for row in rows:
                list_id.append(row[0])
            for i in list_id:
                print(i)
                if id_client == i:
                    print("Пользуйтесь ботом")
                    return id_client
                else:
                    print("Вы ввели неправильный id")
        elif id_client == 0:
            id_client = randint(0, 100000)
            print(f"Ваш id {id_client}")
            return id_client


cur = con.cursor()
main()
cur.close()
