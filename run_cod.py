from bot import bot
from create_tables import engine, create_tables

if __name__ == '__main__':
    create_tables(engine)
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка при работе бота: {e}")