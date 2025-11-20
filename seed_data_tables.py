
import time
from create_tables import Session, Level, CommonWord, create_tables
from ai_hf import AI_HF

session = Session()


def adding_level(level_name):
    """Insert multiple CEFR levels into the database.

    Args:
        level_name (list[str]): List of CEFR level names.
    """

    for n in level_name:
        level = Level(name=n)
        session.add(level)
    session.commit()


adding_level(['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])


def adding_common_word(russian_word, english_word, level_name):
    """Insert a common vocabulary word with example sentence into the database.

    Args:
        russian_word (str): Translation in Russian.
        english_word (str): English word to store.
        level_name (str): CEFR level assigned to the word.
    """

    level= session.query(Level).filter(Level.name == level_name).one()
    level_id = level.id
    example = AI_HF.example(english_word, level_name)
    if not example:
        example = None
    word = CommonWord(russian_word=russian_word, english_word=english_word, example=example, id_level=level_id)
    session.add(word)
    session.commit()


#A1
adding_common_word('небо', 'sky', 'A1')
time.sleep(1)
adding_common_word('мост', 'bridge', 'A1')
time.sleep(1)
adding_common_word('музыка', 'music', 'A1')
time.sleep(1)
adding_common_word('собака', 'dog', 'A1')
time.sleep(1)
adding_common_word('вода', 'water', 'A1')
time.sleep(1)

#A2
adding_common_word('зарядка', 'charger', 'A2')
time.sleep(1)
adding_common_word('аэропорт', 'airport', 'A2')
time.sleep(1)
adding_common_word('привычный путь', 'routine', 'A2')
time.sleep(1)
adding_common_word('путешествие', 'journey', 'A2')
time.sleep(1)
adding_common_word('выбор', 'choice', 'A2')
time.sleep(1)

#B1
adding_common_word('уверенность', 'confidence', 'B1')
time.sleep(1)
adding_common_word('терпение', 'patience', 'B1')
time.sleep(1)
adding_common_word('вдохновение', 'inspiration', 'B1')
time.sleep(1)
adding_common_word('попытка', 'attempt', 'B1')
time.sleep(1)
adding_common_word('поддержка', 'support', 'B1')
time.sleep(1)

#B2
adding_common_word('атмосфера', 'atmosphere', 'B2')
time.sleep(1)
adding_common_word('алгоритм', 'algorithm', 'B2')
time.sleep(1)
adding_common_word('орбита', 'orbit', 'B2')
time.sleep(1)
adding_common_word('измерение', 'measurement', 'B2')
time.sleep(1)
adding_common_word('гипотеза', 'hypothesis', 'B2')
time.sleep(1)

#C1
adding_common_word('восприятие реальности', 'perception', 'C1')
time.sleep(1)
adding_common_word('неопределённость', 'uncertainty', 'C1')
time.sleep(1)
adding_common_word('сознательность', 'mindfulness', 'C1')
time.sleep(1)
adding_common_word('убедительность', 'persuasiveness', 'C1')
time.sleep(1)
adding_common_word('противоречивость', 'ambivalence', 'C1')
time.sleep(1)

#C2
adding_common_word('сингулярность', 'singularity', 'C2')
time.sleep(1)
adding_common_word('неизбежность', 'inevitability', 'C2')
time.sleep(1)
adding_common_word('взаимосвязанность', 'interconnectedness', 'C2')
time.sleep(1)
adding_common_word('саморефлексия', 'introspection', 'C2')
time.sleep(1)
adding_common_word('непредсказуемость', 'unpredictability', 'C2')


session.close()