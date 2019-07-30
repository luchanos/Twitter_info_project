import json
import re


def sentiment_dict_maker(filepath):
    """
    :param filepath: путь к файлу sentiments
    :return: возвращает словарь эмоциональной окраски
    """
    word_dict = dict()
    """Читает маркеры эмоциональной окраски из файла и записывает их в БД"""
    line = True
    with open(filepath) as filetoread:
        while line != '':
            line = filetoread.readline()
            if line != '':
                sentiment = re.split('\t', line)
                sentiment[1] = int(sentiment[1])
                word_dict.update({sentiment[0]: sentiment[1]})
    return word_dict


def sentiment_counter(s, word_dict):
    """
    :param s: строка с текстом твитта
    :param word_dict: словарь эмоциональной окраски
    :return:    Считает количество вхождений подстроки в словарь
    """
    res = 0
    s = s.split()
    for x in s:
        if x in word_dict:
            res += word_dict[x]
    return res


def tweets_inserter_sql(cursor, line_to_json, sentiment):
    """ Функция для записи json в таблицу twitts
    :param cursor: курсор подключения к БД
    :param line_to_json: json с данными
    :param sentiment: значение эмоциональной окраски
    :return:
    """
    country_code = None
    if line_to_json['place']:
        country_code = line_to_json['place']['country_code']
    cursor.execute("""insert or ignore into twitts (tweet_id, created_at, user_id, tweet_text, country_code, sentiment) 
            values (?,?,?,?,?,?)""", [line_to_json['id'],
                                      line_to_json['created_at'],
                                      line_to_json['user']['id'],
                                      line_to_json['text'],
                                      country_code,
                                      sentiment])


def users_inserter_sql(cursor, line_to_json):
    """
    Функция для записи json в таблицу twitts
    :param cursor:  курсор подключения к БД
    :param line_to_json: json с данными
    :return:
    """
    cursor.execute("""insert or ignore into users (user_id, url, username, lang, location) 
            values (?,?,?,?,?)""", [line_to_json['user']['id'],
                                    line_to_json['user']['url'],
                                    line_to_json['user']['name'],
                                    line_to_json['user']['lang'],
                                    line_to_json['user']['location']])


def tweets_inserter(filepath, cursor, word_dict):
    """ Читает строки из файла с твитами и вызывает метод записи в БД
    :param filepath: путь к файлу
    :param cursor: курсор подключения к БД
    :param word_dict: словарь эмоциональной окраски
    :return:
    """
    line = True
    with open(filepath) as filetoread:
        while line != '':
            line = filetoread.readline()
            if line != '':
                line_to_json = json.loads(line)
            if 'delete' not in line_to_json.keys():
                sentiment = sentiment_counter(line_to_json['text'], word_dict)
                tweets_inserter_sql(cursor, line_to_json, sentiment)
                users_inserter_sql(cursor, line_to_json)
