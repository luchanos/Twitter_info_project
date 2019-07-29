import sqlite3


class Sqlite_Contextman:

    def __init__(self, dbname):
        self.dbname = dbname

    def __enter__(self):
        self.conn = sqlite3.connect(self.dbname)
        return self.conn

    def __exit__(self, exc_val, exc_type, exc_tb):
        self.conn.close()
        if exc_val:
            raise Exception

    @staticmethod
    def db_querrier(cursor, sql):
        """Для запуска произвольного запроса"""
        cursor.execute(sql)