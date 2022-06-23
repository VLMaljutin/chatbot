# Сделал небольшую замену эмоций, так как некоторые смайлики, находящиеся в разных группах
# считывались одинаково
a = 5
list_happy = ["😀", "😃", "😄", "😁", "😆", "😀", "😊", "🤩", "🥳"]
list_sad = ["😒", "😔", "😞", "😟", "😤", "☹", "😩", "😡", "😓"]
list_anger = ["👿", "😭", "🤬", "💩", "👺", "💀", "😠", "🤯", "🤨"]


def main():
    prev = ""
    while True:
        message = input("Клиент: ")
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
            prev = ""


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


main()
