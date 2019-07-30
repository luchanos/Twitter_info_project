from retry import retry
import os
from constants import FILEPATH, FILEPATH_AF, db, sql, log_conf, logpath
from db_tweet_tools import *
from sqlite_contextman import *
import configparser
from prettylogger import PrettyLogger
import argparse

ppath = os.getcwd()  # проверяем с какой директорией работает питон
FILEPATH_AF = '{}{}'.format(ppath, FILEPATH_AF)
FILEPATH = '{}{}'.format(ppath, FILEPATH)
db = '{}{}'.format(ppath, db)
log_conf = '{}{}'.format(ppath, log_conf)
logpath = '{}{}'.format(ppath, logpath)

""" Производим создание и настройку парсера"""
parser = argparse.ArgumentParser(description='Twitter_info_project')
parser.add_argument('-r', '--retry_attempts', type=int, default=3, help='Retry attempts to perform script')
parser.add_argument('-d', '--delay', type=int, default=5, help='Delaying period between attempts')
args = parser.parse_args()

# создание и настройка логгера
conf = configparser.RawConfigParser()
conf.read(log_conf)
mainLogger = PrettyLogger(name='tweet_script_logger', logpath=logpath, conf=conf)


def main(retry_attempts, delay):
    """ Главный метод программы. Декорирован retry на случай неудачных коннекшенов к БД
    :param retry_attempts: количество попыток
    :param delay: задержка между попытками
    :return:
    """

    @retry(tries=retry_attempts, delay=delay)
    def main_func():
        word_dict = sentiment_dict_maker(FILEPATH_AF)  # получаем словарь с эмоциональной окраской
        with Sqlite_Contextman(db) as conn:
            cursor = conn.cursor()
            for req in sql:
                Sqlite_Contextman.db_querrier(cursor, req)
            tweets_inserter(FILEPATH, cursor, word_dict)
            conn.commit()
            conn.close()

    main_func()


if __name__ == '__main__':
    try:
        main(args.retry_attempts, args.delay)
        mainLogger.logger.info(msg='Work complete, my Lord!')
    except Exception as err:
        mainLogger.logger.error(msg="Error!!! {}".format(err))