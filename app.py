import telebot
from config import TOKEN, info_txt
from telebot import types
from quiz import get_question_message, get_answered_message, DataBase
from mail_send import send_email
from vk_repost import repost_vk

bot = telebot.TeleBot(TOKEN)
db = DataBase()


@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    markup_inline = types.InlineKeyboardMarkup()
    item_quiz = types.InlineKeyboardButton(text='Хочешь узнать своего тотемного животного?', callback_data='?quiz')
    item_url = types.InlineKeyboardButton(text='Сайт Московского Зоопарка', url='https://moscowzoo.ru/animals/')
    item_info = types.InlineKeyboardButton(text='О Московском зоопарке', callback_data='info')
    markup_inline.add(item_quiz).add(item_url).add(item_info)
    bot.send_photo(message.chat.id, open('MZoo_logo.jpg', 'rb'),
                   f'{message.chat.username} Приветствую тебя от имени <b>Московского Зоопарка!</b> \n',
                   parse_mode="HTML", reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: call.data == 'info')
def info(call):
    bot.send_photo(call.message.chat.id, open('MZoo_logo_1864.jpg', 'rb'), f'{call.message.chat.username}'
                                                                           f'{info_txt}', parse_mode="HTML")


@bot.callback_query_handler(func=lambda query: query.data.startswith("?quiz"))
def quiz(query):
    user = db.get_user(query.message.chat.id)

    user["is_passing"] = True

    db.set_user(query.message.chat.id, user)

    post = get_question_message(user)
    if post is not None:  # если есть вопрос, то отправляем в чат
        if post.get("animal"):
            if post.get("animal") == 'Сова':
                bot.send_photo(query.message.chat.id, open('owl.jpg', 'rb'), post["text"],
                               reply_markup=post["keyboard"])
            elif post.get("animal") == 'Волк':
                bot.send_photo(query.message.chat.id, open('wolf.jpg', 'rb'), post["text"],
                               reply_markup=post["keyboard"])
            elif post.get("animal") == 'Лев':
                bot.send_photo(query.message.chat.id, open('lion.jpeg', 'rb'), post["text"],
                               reply_markup=post["keyboard"])
            elif post.get("animal") == 'Кит':
                bot.send_photo(query.message.chat.id, open('whale.jpg', 'rb'), post["text"],
                               reply_markup=post["keyboard"])

        else:
            bot.send_message(query.message.chat.id, post["text"], reply_markup=post["keyboard"])


@bot.callback_query_handler(func=lambda query: query.data.startswith("?ans"))
def ans(query):
    user = db.get_user(query.message.chat.id)
    answer_index = int(query.data.split("&")[1])
    user["answers"].append(answer_index)
    db.set_user(query.message.chat.id, user)

    post = get_answered_message(user, answer_index)
    if post is not None:  # если есть вопрос, то отправляем в чат
        bot.edit_message_text(post["text"], query.message.chat.id, query.message.id, reply_markup=post["keyboard"])


@bot.callback_query_handler(func=lambda query: query.data == "?next")
def next_question(query):
    user = db.get_user(query.message.chat.id)

    user["question_index"] += 1
    db.set_user(query.message.chat.id, user)

    post = get_question_message(user)

    if post is not None:
        if post.get("animal"):
            if post.get("animal") == 'Сова':
                bot.send_photo(query.message.chat.id, open('owl.jpg', 'rb'), post["text"],
                               reply_markup=post["keyboard"])
            elif post.get("animal") == 'Волк':
                bot.send_photo(query.message.chat.id, open('wolf.jpg', 'rb'), post["text"],
                               reply_markup=post["keyboard"])
            elif post.get("animal") == 'Лев':
                bot.send_photo(query.message.chat.id, open('lion.jpeg', 'rb'), post["text"],
                               reply_markup=post["keyboard"])
            elif post.get("animal") == 'Кит':
                bot.send_photo(query.message.chat.id, open('whale.jpg', 'rb'), post["text"],
                               reply_markup=post["keyboard"])

        else:
            bot.edit_message_text(post["text"], query.message.chat.id, query.message.id, reply_markup=post["keyboard"])


@bot.callback_query_handler(func=lambda query: query.data.startswith("?replay"))
def replay(query):
    user = db.get_user(query.message.chat.id)
    user["question_index"] = 0
    user["is_passed"] = False
    user["is_passing"] = True
    user["answers"] = []

    db.set_user(query.message.chat.id, user)

    post = get_question_message(user)
    if post is not None:  # если есть вопрос, то отправляем в чат
        bot.send_message(query.message.chat.id, post["text"], reply_markup=post["keyboard"])


@bot.callback_query_handler(func=lambda query: query.data.startswith("?repost"))
def repost(query):
    user = db.get_user(query.message.chat.id)
    post = get_question_message(user)

    if post is not None:
        repost_vk(post.get("text"))


@bot.callback_query_handler(func=lambda query: query.data.startswith("?cont"))
def cont(query):
    user = db.get_user(query.message.chat.id)
    send_email(query.message.chat.username, user.get("points"))


if __name__ == '__main__':
    bot.polling()
