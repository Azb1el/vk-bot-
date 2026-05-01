import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import requests
import config as cfg

vk_session = vk_api.VkApi(token=cfg.VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def send_msg(id, msg, keyboard=None):
    vk.messages.send(user_id=id, message=msg, random_id=random.randint(1, 2147483647), keyboard=keyboard)

def get_about():
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
    local_jokes = ["-Доктор, я жить буду?\n - А смысл?",
                   "Колобок повесился . . .",
                   "Купил мужик шляпу, а она ему как раз.",
                   "Повар спрашивает повара: \n - Какова твоя профессия? Ты милиционер? \n - Нееет! - отвечает повар, - моя главная профессия - пооовар! А твоя, наверное, врач? \n - Нееет! Я пооовар! \n",
                   "Немецкая пунктуальность \n   -Дорогой, ты записал нашу годовщину в твой ежедневник с точностью до минуты, но забыл про неё душой.\n     -Франциска, не драматизируй. Согласно графику, эмоциональные упрёки у нас запланированы на 20:15. Сейчас только 20:13. \n "
                   ]
    return random.choice(local_jokes)

def get_math():
    type_eq = random.randint(1, 3)
    problem = ""
    answer = None

    if type_eq == 1:
        a = random.randint(1, 10)
        answer = random.randint(1, 10)
        b = a * answer
        problem = f"Решите уравнение: {a}x = {b}"

    elif type_eq == 2:
        a = random.randint(1, 5)
        answer = random.randint(1, 10)
        b = random.randint(1, 20)
        c = a * answer + b
        problem = f"Решите уравнение: {a}x + {b} = {c}"

    else:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        answer = a * b
        problem = f"Решите уравнение: x / {a} = {b}"

    return problem, answer

def get_about_extended():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_openlink_button('VK разработчика', 'https://vk.com/andreyselyunin')
    keyboard.add_line()
    keyboard.add_openlink_button('Telegram', 'https://t.me/Azbiill')
    keyboard.add_line()
    keyboard.add_openlink_button('GitHub', 'https://github.com/Azb1el')

    about_text = ("Информация о создателе бота\n"
                  "Разработчик: Селюнин Андрей Васильевич\n"
                  "Дата создания: 24 апреля 2026\n")

    return about_text, keyboard.get_keyboard()

def get_help_extended():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_callback_button('/about', color=VkKeyboardColor.PRIMARY, payload={'command': 'about_info'})
    keyboard.add_line()
    keyboard.add_callback_button('/joke', color=VkKeyboardColor.POSITIVE, payload={'command': 'joke_info'})
    keyboard.add_line()
    keyboard.add_callback_button('/math', color=VkKeyboardColor.NEGATIVE, payload={'command': 'math_info'})

    help_text = ("Справка по командам бота\n"
                 "Выберите команду для подробной информации:")

    return help_text, keyboard.get_keyboard()

def get_command_info_extended():
    about_info = "/about - Информация о создателе бота"
    joke_info = "/joke - Получить случайную шутку"
    math_info = "/math - Получить случайный математический пример"

    info = {
        'about_info': about_info,
        'joke_info': joke_info,
        'math_info': math_info
    }
    return info

def get_joke_extended():
    joke_text = get_joke()
    keyboard = VkKeyboard(inline=True)
    keyboard.add_callback_button('Ещё анекдот', color=VkKeyboardColor.POSITIVE, payload={'command': 'another_joke'})
    return joke_text, keyboard.get_keyboard()

def get_math_extended():
    problem, correct_answer = get_math()

    wrong_answers = []
    while len(wrong_answers) < 3:
        wrong = correct_answer + random.randint(-5, 5)
        if wrong != correct_answer and wrong > 0 and wrong not in wrong_answers:
            wrong_answers.append(wrong)

    options = wrong_answers + [correct_answer]
    random.shuffle(options)

    keyboard = VkKeyboard(inline=True)
    keyboard.add_callback_button(
        str(options[0]),
        color=VkKeyboardColor.PRIMARY,
        payload={'command': 'math_answer', 'answer': options[0], 'correct': correct_answer}
    )
    keyboard.add_callback_button(
        str(options[1]),
        color=VkKeyboardColor.PRIMARY,
        payload={'command': 'math_answer', 'answer': options[1], 'correct': correct_answer}
    )
    keyboard.add_line()
    keyboard.add_callback_button(
        str(options[2]),
        color=VkKeyboardColor.PRIMARY,
        payload={'command': 'math_answer', 'answer': options[2], 'correct': correct_answer}
    )
    keyboard.add_callback_button(
        str(options[3]),
        color=VkKeyboardColor.PRIMARY,
        payload={'command': 'math_answer', 'answer': options[3], 'correct': correct_answer}
    )

    return problem, keyboard.get_keyboard()

def check_math_answer_extended(user_answer, correct_answer):
    if user_answer == correct_answer:
        return "Правильно! Отличная работа!"
    else:
        return f"Неправильно. Правильный ответ: {correct_answer}"

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
        if event.text:
            print(event.text)

        if hasattr(event, 'payload') and event.payload:
            payload = event.payload
            command = payload.get('command')

            if command in ['about_info', 'joke_info', 'math_info']:
                info_dict = get_command_info_extended()
                send_msg(event.user_id, info_dict[command])

            elif command == 'another_joke':
                joke_text, keyboard = get_joke_extended()
                send_msg(event.user_id, joke_text, keyboard)

            elif command == 'math_answer':
                user_answer = payload.get('answer')
                correct_answer = payload.get('correct')
                result_msg = check_math_answer_extended(user_answer, correct_answer)
                send_msg(event.user_id, result_msg)

        elif event.text.lower() == "/about":
            about_text, keyboard = get_about_extended()
            send_msg(event.user_id, about_text, keyboard)

        elif event.text.lower() == "/help":
            help_text, keyboard = get_help_extended()
            send_msg(event.user_id, help_text, keyboard)

        elif event.text.lower() == "/joke":
            joke_text, keyboard = get_joke_extended()
            send_msg(event.user_id, joke_text, keyboard)

        elif event.text.lower() == "/math":
            math_text, keyboard = get_math_extended()
            send_msg(event.user_id, math_text, keyboard)

        elif event.text.lower() in ["привет", "здравствуй", "хай", "здарова", "hello", "прив", "ку"]:
            greetings = ["Здравствуй! Рад тебя видеть!",
                         "Приветствую! Чем могу помочь?",
                         "Хай! Как настроение?"]
            send_msg(event.user_id, random.choice(greetings))

        elif "как дела" in event.text.lower() or "как жизнь" in event.text.lower() or "как ты" in event.text.lower():
            answers = [
                "Отлично! А у тебя как?",
                "Всё работает в штатном режиме! А ты как?",
                "Лучше всех! Спасибо, что спросил",
            ]
            send_msg(event.user_id, random.choice(answers))

        elif event.text.lower() in ["пока", "до свидания", "бай", "увидимся", "прощай"]:
            goodbyes = [
                "Пока! Возвращайся!",
                "До свидания! Хорошего дня!",
                "Буду ждать тебя! Приходи ещё!",
                "Удачи! Если что - я здесь!"
            ]
            send_msg(event.user_id, random.choice(goodbyes))