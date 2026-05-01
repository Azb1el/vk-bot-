import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import config as cfg
import json

vk_session = vk_api.VkApi(token=cfg.VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

math_answers = {}


def send_msg(id, msg, keyboard=None):
    vk.messages.send(user_id=id, message=msg, random_id=random.randint(1, 2147483647), keyboard=keyboard)


def get_joke():
    local_jokes = ["-Доктор, я жить буду?\n - А смысл?",
                   "Колобок повесился . . .",
                   "Купил мужик шляпу, а она ему как раз.",
                   "Повар спрашивает повара: \n - Какова твоя профессия? Ты милиционер? \n - Нееет! - отвечает повар, - моя главная профессия - пооовар! А твоя, наверное, врач? \n - Нееет! Я пооовар! \n",
                   "Немецкая пунктуальность \n   -Дорогой, ты записал нашу годовщину в твой ежедневник с точностью до минуты, но забыл про неё душой.\n     -Франциска, не драматизируй. Согласно графику, эмоциональные упрёки у нас запланированы на 20:15. Сейчас только 20:13. \n "
                   ]
    return random.choice(local_jokes)


def get_about_extended():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_openlink_button('VK разработчика', 'https://vk.com/andreyselyunin')
    keyboard.add_line()
    keyboard.add_openlink_button('Telegram', 'https://t.me/Azbiill')
    keyboard.add_line()
    keyboard.add_openlink_button('GitHub', 'https://github.com/Azb1el')

    about_text = ("Информация о создателе бота\n\n"
                  "Разработчик: Селюнин Андрей Васильевич\n"
                  "Дата создания: 24 апреля 2026\n")

    return about_text, keyboard.get_keyboard()


def get_help_extended():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button('Подробнее об /about', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Подробнее о /joke', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Подробнее о /math', color=VkKeyboardColor.NEGATIVE)

    help_text = ("Справка по командам бота\n\n"
                 "Выберите команду для получения подробной информации:")

    return help_text, keyboard.get_keyboard()


def get_command_info(command):
    if command == "about":
        return ("Команда /about\n\n"
                "Показывает информацию о разработчике бота:\n"
                "- Имя разработчика\n"
                "- Дату создания\n"
                "- Ссылки на контакты (VK, Telegram, GitHub)\n\n")
    elif command == "joke":
        return ("Команда /joke\n\n"
                "Отправляет случайную шутку из коллекции бота.\n"
                "После получения шутки появляется кнопка для получения ещё одной.\n\n")
    elif command == "math":
        return ("Команда /math\n\n"
                "Предлагает решить случайный математический пример.\n"
                "Типы примеров:\n"
                "- Простые уравнения\n"
                "- Уравнения с неизвестным\n"
                "- Уравнения на деление\n\n"
                "Выберите правильный ответ из 4 вариантов.")


def get_joke_extended():
    joke_text = get_joke()
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button('Ещё шутку', color=VkKeyboardColor.POSITIVE)
    return joke_text, keyboard.get_keyboard()


def get_math_extended(user_id):
    global math_answers

    type_eq = random.randint(1, 3)
    problem = ""
    correct_answer = None

    if type_eq == 1:
        a = random.randint(1, 10)
        correct_answer = random.randint(1, 10)
        b = a * correct_answer
        problem = f"Решите уравнение: {a}x = {b}"

    elif type_eq == 2:
        a = random.randint(1, 5)
        correct_answer = random.randint(1, 10)
        b = random.randint(1, 20)
        c = a * correct_answer + b
        problem = f"Решите уравнение: {a}x + {b} = {c}"

    else:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        correct_answer = a * b
        problem = f"Решите уравнение: x / {a} = {b}"

    wrong_answers = []
    while len(wrong_answers) < 3:
        wrong = correct_answer + random.randint(-5, 5)
        if wrong != correct_answer and wrong > 0 and wrong not in wrong_answers:
            wrong_answers.append(wrong)

    options = wrong_answers + [correct_answer]
    random.shuffle(options)

    math_answers[user_id] = correct_answer

    keyboard = VkKeyboard(inline=True)
    keyboard.add_button(str(options[0]), color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(str(options[1]), color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(str(options[2]), color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(str(options[3]), color=VkKeyboardColor.PRIMARY)

    return problem, keyboard.get_keyboard()


def check_math_answer_extended(user_id, user_answer, correct_answer):
    if user_answer == correct_answer:
        return "Правильно! Отличная работа!"
    else:
        return f"Неправильно. Правильный ответ: {correct_answer}"


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.from_me:
            continue

        if event.text:
            text = event.text.lower()
            print(f"Получено сообщение: {text}")

            if text == "/about":
                about_text, keyboard = get_about_extended()
                send_msg(event.user_id, about_text, keyboard)

            elif text == "/help":
                help_text, keyboard = get_help_extended()
                send_msg(event.user_id, help_text, keyboard)

            # Обработка нажатий на кнопки из /help
            elif text == "подробнее об /about":
                about_info = get_command_info("about")
                send_msg(event.user_id, about_info)

            elif text == "подробнее о /joke":
                joke_info = get_command_info("joke")
                send_msg(event.user_id, joke_info)

            elif text == "подробнее о /math":
                math_info = get_command_info("math")
                send_msg(event.user_id, math_info)

            elif text == "/joke" or text == "ещё шутку":
                joke_text, keyboard = get_joke_extended()
                send_msg(event.user_id, joke_text, keyboard)

            elif text == "/math":
                math_text, keyboard = get_math_extended(event.user_id)
                send_msg(event.user_id, math_text, keyboard)

            elif text.isdigit() and event.user_id in math_answers:
                user_answer = int(text)
                correct_answer = math_answers[event.user_id]
                result = check_math_answer_extended(event.user_id, user_answer, correct_answer)
                send_msg(event.user_id, result)
                del math_answers[event.user_id]

            elif text in ["привет", "здравствуй", "хай", "здарова", "hello", "прив", "ку"]:
                greetings = ["Здравствуй! Рад тебя видеть!",
                             "Приветствую! Чем могу помочь?",
                             "Хай! Как настроение?"]
                send_msg(event.user_id, random.choice(greetings))

            elif "как дела" in text or "как жизнь" in text or "как ты" in text:
                answers = [
                    "Отлично! А у тебя как?",
                    "Всё работает в штатном режиме! А ты как?",
                    "Лучше всех! Спасибо, что спросил",
                ]
                send_msg(event.user_id, random.choice(answers))

            elif text in ["пока", "до свидания", "бай", "увидимся", "прощай"]:
                goodbyes = [
                    "Пока! Возвращайся!",
                    "До свидания! Хорошего дня!",
                    "Буду ждать тебя! Приходи ещё!",
                    "Удачи! Если что - я здесь!"
                ]
                send_msg(event.user_id, random.choice(goodbyes))