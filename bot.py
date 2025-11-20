import random
import telebot
from telebot import types

from config import TG_BOT_TOKEN
from create_tables import Session, User, Level, CommonWord, UserWord
from ai_hf import AI_HF

bot = telebot.TeleBot(TG_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    """Handle /start command and initialize user profile and level selection."""
    session = Session()
    user_id = message.chat.id
    is_user = session.query(User).filter(User.id == user_id).all()
    if not is_user:
        info_user = User(id = user_id)
        session.add(info_user)
    buttom_A1 = types.KeyboardButton('A1')
    buttom_A2 = types.KeyboardButton('A2')
    buttom_B1 = types.KeyboardButton('B1')
    buttom_B2 = types.KeyboardButton('B2')
    buttom_C1 = types.KeyboardButton('C1')
    buttom_C2 = types.KeyboardButton('C2')
    level_keyboard = types.ReplyKeyboardMarkup()
    for i in [buttom_A1, buttom_A2, buttom_B1, buttom_B2, buttom_C1, buttom_C2]:
        level_keyboard.add(i)
    welcome_message = (
    "👋 Привет! Я бот для изучения английских слов.\n\n"
    "Помогу тебе учить новые слова, проверять знания и сохранять свой словарь.\n"
    "Начнём!"
)
    bot.send_message(message.chat.id, welcome_message)
    bot.send_message(message.chat.id, 'Выбери уровень английского языка для практики ⬇️', reply_markup=level_keyboard)
    session.commit()
    session.close()


@bot.message_handler(func=lambda i: i.text in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])
def second_step(message):
    """Save the user's chosen CEFR level and display main menu."""
    session = Session()
    menu = types.ReplyKeyboardMarkup()
    buttom_main_menu = types.KeyboardButton('Главное меню')
    menu.add(buttom_main_menu)
    user_id = message.chat.id
    user_level = session.query(Level).filter(Level.name == message.text).one()
    session.query(User).filter(User.id == user_id).update({'level_id': f'{user_level.id}'})
    session.commit()
    bot.send_message(message.chat.id, f'Отлично! Твой уровень - {message.text}! Ты сможешь его поменять в любой момент!', reply_markup=menu)
    session.commit()
    session.close()


@bot.message_handler(func=lambda i: i.text == 'Главное меню')
def main_menu(message):
    """Display the main menu with available bot actions."""
    session = Session()
    menu = types.ReplyKeyboardMarkup()
    buttom_learn_re = types.KeyboardButton('Учить слова (рус->eng)')
    buttom_learn_er = types.KeyboardButton('Учить слова (eng->рус)')
    buttom_add = types.KeyboardButton('Добавить слово')
    buttom_show = types.KeyboardButton('Мой словарь')
    buttom_remove = types.KeyboardButton('Удалить слово')
    buttom_level = types.KeyboardButton('Поменять уровень')
    buttom_estimate = types.KeyboardButton('Оценить мой уровень')
    for i in [buttom_add, buttom_show, buttom_remove, buttom_learn_re, buttom_learn_er, buttom_level, buttom_estimate]:
        menu.add(i)
    bot.send_message(message.chat.id, f'Ты в главном меню! Выбери действие ⬇️', reply_markup=menu)
    session.commit()
    session.close()


@bot.message_handler(func=lambda i: i.text == 'Учить слова (рус->eng)')
def learn_words_re(message):
    """Start a learning round: Russian → English direction."""
    session = Session()
    user_id = message.chat.id
    user_level = session.query(Level).join(User.level).filter(User.id == user_id).first()
    common_words = session.query(CommonWord).join(Level).filter(Level.id == user_level.id).all()
    user_words = session.query(UserWord).filter(UserWord.id_user == user_id).all()
    words = []
    for word in common_words:
        _dict = {'eng': '', 'rus': '', 'exmp': ''}
        _dict['eng'] = word.english_word
        _dict['rus'] = word.russian_word
        _dict['exmp'] = word.example
        words.append(_dict)
    for word in user_words:
        _dict = {'eng': '', 'rus': '', 'exmp': ''}
        _dict['eng'] = word.english_word
        _dict['rus'] = word.russian_word
        _dict['exmp'] = word.example
        words.append(_dict)
    random.shuffle(words)
    first_word = words[0]
    second_word = words[1]
    third_word = words[2]
    fourth_word = words[3]
    menu = types.ReplyKeyboardMarkup()
    buttom_first_word = types.KeyboardButton(first_word['eng'])
    buttom_second_word = types.KeyboardButton(second_word['eng'])
    buttom_third_word = types.KeyboardButton(third_word['eng'])
    buttom_fourth_word = types.KeyboardButton(fourth_word['eng'])
    buttom_show_translate = types.KeyboardButton('Показать перевод')
    buttom_main_menu = types.KeyboardButton('Главное меню')
    words_buttoms = [buttom_first_word, buttom_second_word, buttom_third_word, buttom_fourth_word]
    random.shuffle(words_buttoms)
    menu.add(*words_buttoms)
    menu.add(buttom_show_translate)
    menu.add(buttom_main_menu)
    user_msg = bot.send_message(message.chat.id, f'Слово: {first_word['rus']}\nВыбери перевод', reply_markup=menu)
    bot.register_next_step_handler(user_msg, LearnWords.right_or_not_re, first_word['rus'], first_word['eng'], first_word['exmp'])
    session.commit()
    session.close()


@bot.message_handler(func=lambda i: i.text == 'Учить слова (eng->рус)')
def learn_words_er(message):
    """Start a learning round: English → Russian direction."""
    session = Session()
    user_id = message.chat.id
    user_level = session.query(Level).join(User.level).filter(User.id == user_id).first()
    common_words = session.query(CommonWord).join(Level).filter(Level.id == user_level.id).all()
    user_words = session.query(UserWord).filter(UserWord.id_user == user_id).all()
    words = []
    for word in common_words:
        _dict = {'eng': '', 'rus': '', 'exmp': ''}
        _dict['eng'] = word.english_word
        _dict['rus'] = word.russian_word
        _dict['exmp'] = word.example
        words.append(_dict)
    for word in user_words:
        _dict = {'eng': '', 'rus': '', 'exmp': ''}
        _dict['eng'] = word.english_word
        _dict['rus'] = word.russian_word
        _dict['exmp'] = word.example
        words.append(_dict)
    random.shuffle(words)
    first_word = words[0]
    second_word = words[1]
    third_word = words[2]
    fourth_word = words[3]
    menu = types.ReplyKeyboardMarkup()
    buttom_first_word = types.KeyboardButton(first_word['rus'])
    buttom_second_word = types.KeyboardButton(second_word['rus'])
    buttom_third_word = types.KeyboardButton(third_word['rus'])
    buttom_fourth_word = types.KeyboardButton(fourth_word['rus'])
    buttom_show_translate = types.KeyboardButton('Показать перевод')
    buttom_main_menu = types.KeyboardButton('Главное меню')
    words_buttoms = [buttom_first_word, buttom_second_word, buttom_third_word, buttom_fourth_word]
    random.shuffle(words_buttoms)
    menu.add(*words_buttoms)
    menu.add(buttom_show_translate)
    menu.add(buttom_main_menu)
    user_msg = bot.send_message(message.chat.id, f'Слово: {first_word['eng']}\nВыбери перевод', reply_markup=menu)
    bot.register_next_step_handler(user_msg, LearnWords.right_or_not_er, first_word['eng'], first_word['rus'], first_word['exmp'])
    session.commit()
    session.close()


@bot.message_handler(func=lambda i: i.text == 'Добавить слово')
def add_words(message):
    """Begin the process of adding a new custom word to the user's dictionary."""
    session = Session()
    user_id = message.chat.id
    user_level = session.query(Level).join(User.level).filter(User.id == user_id).first()
    menu = types.ReplyKeyboardRemove()
    user_msg = bot.send_message(message.chat.id, f'Напиши слово на английском языке, которое хочешь добавить в словарь: ', reply_markup=menu)
    bot.register_next_step_handler(user_msg, Add_words.add_eng, user_level)
    session.commit()
    session.close()


@bot.message_handler(func=lambda i: i.text == 'Мой словарь')
def show_words(message):
    """Show all user-added vocabulary entries."""
    session = Session()
    user_id = message.chat.id
    words = session.query(UserWord).filter(UserWord.id_user == user_id).all()
    answer = '📚 Твой словарь: \n'
    if not words:
        bot.send_message(message.chat.id, 'Твой словарь пуст... \n 🕒 Самое время его заполнить!')
    else:
        for word in words:
            answer += f'{word.english_word} ➡️ {word.russian_word} \nПример: {word.example}\nУникальный идентификатор слова: {word.id}\n\n'
        bot.send_message(message.chat.id, answer)
    session.commit()
    session.close()

@bot.message_handler(func=lambda i: i.text == 'Удалить слово')
def remove_words(message):
    """Start the flow for deleting a user-added vocabulary entry."""
    menu = types.ReplyKeyboardMarkup()
    buttom_main_menu = types.KeyboardButton('Главное меню')
    menu.add(buttom_main_menu)
    session = Session()
    user_msg = bot.send_message(message.chat.id, f'Введи уникальный идентификатор слова (посмотреть его можно через кнопку "Мой словарь" в главном меню)', reply_markup=menu)
    bot.register_next_step_handler(user_msg, Remove.find_word)
    session.commit()
    session.close()


@bot.message_handler(func=lambda i: i.text == 'Следующее слово (рус->eng)')
def next_word_re(message):
    """Load a new learning word for Russian → English mode."""
    session = Session()
    learn_words_re(message)
    session.commit()
    session.close()



@bot.message_handler(func=lambda i: i.text == 'Следующее слово (eng->рус)')
def next_word_er(message):
    """Load a new learning word for English → Russian mode."""
    session = Session()
    learn_words_er(message)
    session.commit()
    session.close()
    

@bot.message_handler(func=lambda i: i.text == 'Поменять уровень')
def change_level(message):
    """Allow user to select a new CEFR level."""
    session = Session()
    menu = types.ReplyKeyboardMarkup()
    buttom_A1 = types.KeyboardButton('A1')
    buttom_A2 = types.KeyboardButton('A2')
    buttom_B1 = types.KeyboardButton('B1')
    buttom_B2 = types.KeyboardButton('B2')
    buttom_C1 = types.KeyboardButton('C1')
    buttom_C2 = types.KeyboardButton('C2')
    for i in [buttom_A1, buttom_A2, buttom_B1, buttom_B2, buttom_C1, buttom_C2]:
        menu.add(i)
    bot.send_message(message.chat.id, 'Выбери новый уровень английского языка ⬇️', reply_markup=menu)
    session.commit()
    session.close()


@bot.message_handler(func=lambda i: i.text == 'Оценить мой уровень')
def estimate(message):
    """Process user dictionary and estimate English level via AI."""
    session = Session()
    user_id = message.chat.id
    words = session.query(UserWord).filter(UserWord.id_user == user_id).all()
    bot.send_message(message.chat.id, 'Твой словарь обработает нейросеть и исходя из сложности слов и переводов вычислит твой текущий уровень английского языка!\nОценка не заменит профессиональное тестирование, но поможет определить приблизительный уровень языка!')
    answer = 'Словарь: \n'
    if not words:
        bot.send_message(message.chat.id, 'Твой словарь пуст... \n 🕒 Самое время его заполнить!')
    else:
        for word in words:
            answer += f'{word.english_word} ➡️ {word.russian_word}\n'
    user_ai_level = AI_HF.estimate_level(answer)
    link_test_level = 'https://e24.kz/free-online-english-level-test'
    bot.send_message(message.chat.id, f'Твой уровень английского, согласно вычислениям нейросети: {user_ai_level}.\n\nНейросеть может допускать ошибки, для более точной оценки рекомендуем пройти тест на сайте {link_test_level}')
    session.commit()
    session.close()






class Add_words:

    @staticmethod
    def add_eng(message, user_level):
        """Process and validate the English word before saving and requesting translation.

        Args:
            message: Telegram message object containing user input.
            user_level: User's CEFR level for generating example sentences.
        """

        session = Session()
        english_correct_word = AI_HF.corect_word(message.text)
        example = AI_HF.example(english_correct_word, user_level)
        user_id = message.chat.id
        if not example:
            example = None
        word = UserWord(english_word=english_correct_word, example=example, id_user=user_id)
        session.add(word)
        session.commit()
        id_userword = session.query(UserWord).filter(UserWord.id_user == user_id).filter(UserWord.english_word == english_correct_word).order_by(UserWord.id.desc()).first()
        user_msg_2 = bot.send_message(message.chat.id, f'Напиши перевод слова {english_correct_word}, который хочешь добавить в словарь: ')
        bot.register_next_step_handler(user_msg_2, Add_words.add_rus, id_userword.id, english_correct_word)
        session.commit()
        session.close()


        

    @staticmethod
    def add_rus(message, id_userword, english_correct_word):
        """Save the Russian translation for a previously added English word.

        Args:
            message: Telegram message with Russian translation.
            id_userword (int): ID of the word entry being updated.
            english_correct_word (str): The validated English word.
        """

        session = Session()
        menu = types.ReplyKeyboardMarkup()
        buttom_main_menu = types.KeyboardButton('Главное меню')
        menu.add(buttom_main_menu)
        user_id = message.chat.id
        russian_correct_word = AI_HF.corect_word(message.text)
        session.query(UserWord).filter(UserWord.id == id_userword).update({'russian_word': russian_correct_word})
        session.commit()
        bot.send_message(message.chat.id, f'Пара {english_correct_word} ➡️ {russian_correct_word} успешно добавлена в словарь! 🔥', reply_markup=menu)
        session.commit()
        session.close()


class Remove:

    @staticmethod
    def delete(message, word_id, english_word, russian_word):
        """Delete a vocabulary entry if the user confirms the action.

        Args:
            message: User confirmation message.
            word_id (int): ID of the word to delete.
            english_word (str): English part of the pair.
            russian_word (str): Russian part of the pair.
        """

        session = Session()
        menu = types.ReplyKeyboardMarkup()
        buttom_main_menu = types.KeyboardButton('Главное меню')
        menu.add(buttom_main_menu)
        if message.text == 'Да':
            session.query(UserWord).filter(UserWord.id == word_id).delete()
            bot.send_message(message.chat.id, f'Пара:\n{english_word} ➡️ {russian_word}\nуспешно удалена 🗑️', reply_markup=menu)
        else:
            bot.send_message(message.chat.id, f'Удаление отменено!', reply_markup=menu)
        session.commit()
        session.close()


    @staticmethod
    def find_word(message):
        """Find a user word by ID and ask for deletion confirmation.

        Args:
            message: Telegram message containing entered ID.
        """

        session = Session()
        if message.text.isdigit():
            user_id = message.chat.id
            menu = types.ReplyKeyboardMarkup()
            buttom_y = types.KeyboardButton('Да')
            buttom_n = types.KeyboardButton('Нет')
            menu.add(buttom_y)
            menu.add(buttom_n)
            info_word = session.query(UserWord).filter(UserWord.id_user == user_id).filter(UserWord.id == int(message.text)).first()
            if info_word:
                answer = 'В словаре найдена карточка: \n'
                answer += f'{info_word.english_word} ➡️ {info_word.russian_word} \nПример:\n{info_word.example}\n\n'
                answer += 'Подтверждаешь удаление? (отменить это действие нельзя)'
                user_choose = bot.send_message(message.chat.id, answer, reply_markup=menu)
                bot.register_next_step_handler(user_choose, Remove.delete, info_word.id, info_word.english_word, info_word.russian_word)
            else:
                bot.send_message(message.chat.id, f'Карточка с идентификатором "{message.text}" не найдена!')
        elif message.text == 'Главное меню':
            main_menu(message)
        else:
            bot.send_message(message.chat.id, f'Карточка с идентификатором "{message.text}" не найдена!')
        session.commit()
        session.close()


class LearnWords:

    @staticmethod
    def right_or_not_re(message, right_rus, right_eng, example):
        """Check user answer in Russian → English mode and display feedback.

        Args:
            message: Telegram message with user answer.
            right_rus (str): Correct Russian translation.
            right_eng (str): Correct English word.
            example (str): Example sentence for the word.
        """

        session = Session()
        if message.text != 'Показать перевод' and message.text != 'Главное меню':
            if message.text == right_eng:
                menu = types.ReplyKeyboardMarkup()
                buttom_main_menu = types.KeyboardButton('Главное меню')
                buttom_next_step = types.KeyboardButton('Следующее слово (рус->eng)')
                menu.add(buttom_main_menu)
                menu.add(buttom_next_step)
                bot.send_message(message.chat.id, f'Правильно! ✔️\n{right_rus} ➡️ {right_eng}\nПример использования:\n{example}', reply_markup=menu)
            elif message.text != right_eng:
                user_msg = bot.send_message(message.chat.id, f'Неверно! ❌\nПопробуй заново!')
                bot.register_next_step_handler(user_msg, LearnWords.right_or_not_re, right_rus, right_eng, example)
        elif message.text == 'Показать перевод':
                menu = types.ReplyKeyboardMarkup()
                buttom_main_menu = types.KeyboardButton('Главное меню')
                buttom_next_step = types.KeyboardButton('Следующее слово (рус->eng)')
                menu.add(buttom_main_menu)
                menu.add(buttom_next_step)
                bot.send_message(message.chat.id, f'Перевод:\n{right_rus} ➡️ {right_eng}\nПример использования:\n{example}', reply_markup=menu)
        session.commit()
        session.close()

    @staticmethod
    def right_or_not_er(message, right_eng, right_rus, example):
        """Check user answer in English → Russian mode and display feedback.

        Args:
            message: Telegram message with user answer.
            right_eng (str): Correct English word.
            right_rus (str): Correct Russian translation.
            example (str): Example sentence for the word.
        """

        session = Session()
        if message.text != 'Показать перевод' and message.text != 'Главное меню':
            if message.text == right_rus:
                menu = types.ReplyKeyboardMarkup()
                buttom_main_menu = types.KeyboardButton('Главное меню')
                buttom_next_step = types.KeyboardButton('Следующее слово (eng->рус)')
                menu.add(buttom_main_menu)
                menu.add(buttom_next_step)
                bot.send_message(message.chat.id, f'Правильно! ✔️\n{right_eng} ➡️ {right_rus}\nПример использования:\n{example}', reply_markup=menu)
            elif message.text != right_eng:
                user_msg = bot.send_message(message.chat.id, f'Неверно! ❌\nПопробуй заново!')
                bot.register_next_step_handler(user_msg, LearnWords.right_or_not_er, right_rus, right_eng, example)
        elif message.text == 'Показать перевод':
                menu = types.ReplyKeyboardMarkup()
                buttom_main_menu = types.KeyboardButton('Главное меню')
                buttom_next_step = types.KeyboardButton('Следующее слово (eng->рус)')
                menu.add(buttom_main_menu)
                menu.add(buttom_next_step)
                bot.send_message(message.chat.id, f'Перевод:\n{right_eng} ➡️ {right_rus}\nПример использования:\n{example}', reply_markup=menu)
        session.commit()
        session.close()
