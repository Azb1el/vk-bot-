import  vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import requests
import config  as cfg

vk_session = vk_api.VkApi(token=cfg.VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def send_msg(id ,msg):
    vk.messages.send(user_id=id,message=msg,random_id=random.randint(1, 2147483647))

def get_about ():
    return ("Информация о создателе бота \n"
            "Разработчик:Селюнин Андрей Васильевич \n"
            "Дата создания:24 апреля 2026 \n"

            )
def get_help():
    return ("/about - Информация о создателе бота \n"
            "/help - Справка по командам бота \n "
            "/joke - Получить случайную шутку \n"
            "/math - Получить случайный математический пример \n")

def get_joke():
    local_jokes =["-Доктор, я жить буду?\n - А смысл?",
                  "Колобок повесился . . .",
                  "Купил мужик шляпу, а она ему как раз.",
                  "Повар спрашивает повара: \n - Какова твоя профессия? Ты милиционер? \n - Нееет! - отвечает повар, - моя главная профессия - пооовар! А твоя, наверное, врач? \n - Нееет! Я пооовар! \n",
                  "Немецкая пунктуальность \n   -Дорогой, ты записал нашу годовщину в твой ежедневник с точностью до минуты, но забыл про неё душой.\n     -Франциска, не драматизируй. Согласно графику, эмоциональные упрёки у нас запланированы на 20:15. Сейчас только 20:13. \n "
                  ]
    return random.choice(local_jokes)


def get_math():
    type_eq = random.randint(1, 3)
    problem = ""
    solution = ""

    if type_eq == 1:
        # a * x
        a = random.randint(1, 10)
        answer = random.randint(1, 10)
        b = a * answer
        problem = f"Решите уравнение: {a}x = {b}"
        solution = f"Ответ: x = {answer}"

    elif type_eq == 2:
        # a * x + b
        a = random.randint(1, 5)
        answer = random.randint(1, 10)
        b = random.randint(1, 20)
        c = a * answer + b
        problem = f"Решите уравнение: {a}x + {b} = {c}"
        solution = f"Ответ: x = {answer}"

    else:
        # x / a
        a = random.randint(1, 10)
        answer = random.randint(1, 10)
        b = answer
        c = a * b
        problem = f"Решите уравнение: x / {a} = {b}"
        solution = f"Ответ: x = {c}"

    return f"{problem}\n\n {solution}"

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print(event.text)
        if event.text == "Привет":
            send_msg(event.user_id,"Привет как дела ")
        elif event.text =="/about":
            send_msg(event.user_id, get_about())
        elif event.text =="/help":
            send_msg(event.user_id, get_help())
        elif event.text =="/joke":
            send_msg(event.user_id, get_joke())
        elif event.text == "/math":
            send_msg(event.user_id, get_math())
        elif "как дела" in event.text or "как жизнь" in event.text or "как ты" in event.text:
            answers = [
                "Отлично! А у тебя как?",
                "Всё работает в штатном режиме! А ты как?",
                "Лучше всех! Спасибо, что спросил",
            ]
            send_msg(event.user_id, random.choice(answers))

        elif event.text in ["привет", "здравствуй", "хай", "здарова", "hello", "прив", "ку"]:
            greetings = ["Здравствуй! Рад тебя видеть!",
                    "Приветствую! Чем могу помочь?",
                    "Хай! Как настроение?"]
            send_msg(event.user_id, random.choice(greetings))

        elif event.text in ["пока", "до свидания", "бай", "увидимся", "прощай"]:
            goodbyes = [
                "Пока!"," Возвращайся!",
                "До свидания!"," Хорошего дня!",
                "Буду ждать тебя!"," Приходи ещё!",
                "Удачи! Если что - я здесь!"
            ]
            send_msg(event.user_id, random.choice(goodbyes))




