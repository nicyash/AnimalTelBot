from config import questions, count
import telebot
import json



class DataBase:
    # def __init__(self):
    #     self.user = {}
    #     self.questions_count = len(questions)

    def get_user(self, chat_id):
        with open('users_test_one.json', encoding='utf-8') as json_file:
            data = json.load(json_file)
            for i in data:
                if int(i) == chat_id:
                    return data.get(str(chat_id))

        user_profil = {
            "chat_id": chat_id,  # id пользователя
            "is_passing": False,  # проходит тест?
            "is_passed": False,   # уже прошел
            "question_index": 0,  # индекс вопроса
            "answers": [],  # список ответов
            "points": 0,  # количество баллов
        }
        with open('users_test_one.json', encoding='utf-8') as file:
            data = json.load(file)
            data.update({chat_id: user_profil})
            with open('users_test_one.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            print(data.get(chat_id))
            return data.get(chat_id)

    def set_user(self, chat_id, update):
        with open('users_test_one.json', encoding='utf-8') as file:
            data = json.load(file)
            data.pop(str(chat_id))
            data[str(chat_id)] = update
            with open('users_test_one.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)


db = DataBase()


def get_question_message(user):
    keyboard = telebot.types.InlineKeyboardMarkup()  # создаем клавиатуру
    if user["question_index"] == len(questions):    # если прошел тест выводим сообщения с результатами
        points = sum(user["answers"])

        if 0 <= points <= 16:
            smile = "Сова"
        elif 16 < points <= 32:
            smile = "Волк"
        elif 32 < points <= 48:
            smile = "Лев"
        else:
            smile = "Кит"

        text = (f"Ваше тотемное животно {smile} \n"
                f"Определено в телеграм боте @nicyashBot")
        user["points"] = smile
        user["is_passed"] = True
        user["is_passing"] = False
        db.set_user(user["chat_id"], user)

        keyboard.row(telebot.types.InlineKeyboardButton(f"Пройти тест снова", callback_data=f"?replay"))
        keyboard.row(telebot.types.InlineKeyboardButton(f"Поделиться", callback_data=f"?repost"))
        keyboard.row(telebot.types.InlineKeyboardButton(f"Связаться с сотрудником зоопарка для уточнения про "
                                                        f"программу опекунства.", callback_data=f"?cont"))

        return {
            "text": text,
            "keyboard": keyboard,
            "animal": smile,
        }

    for answer_index, answer in enumerate(questions[user["question_index"]].get('answers')):  # создаем нопки
        keyboard.row(telebot.types.InlineKeyboardButton(f"{chr(answer_index + 97)}) {answer}",
                                                        callback_data=f"?ans&{answer_index}"))

    text = f"{questions[user["question_index"]].get('question')}"  # формируем текст вопроса
    # возвращаем кортеж с вопросом и клавиатурой
    return {
        "text": text,
        "keyboard": keyboard,
        "animal": None,
    }


def get_answered_message(user, ans_index):
    text = f"{questions[user["question_index"]].get('question')}\n"

    for answer_index, answer in enumerate(questions[user["question_index"]].get('answers')):
        text += f"{chr(answer_index + 97)}) {answer}"

        if answer_index == ans_index:
            text += " ✅"

        text += "\n"

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton("Далее", callback_data="?next"))


    return {
        "text": text,
        "keyboard": keyboard
    }
