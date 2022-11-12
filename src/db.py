import psycopg2
from psycopg2 import Error


class DataBase:
    def __init__(self, user, password, address, port, name):
        self._user = user
        self._password = password
        self._address = address
        self._port = port
        self._name = name
        self._connection = None
        self._cursor = None

    def connect(self):
        try:
            self._connection = psycopg2.connect(user=self._user,
                                                password=self._password,
                                                host=self._address,
                                                port=self._port,
                                                database=self._name)
            self._cursor = self._connection.cursor()
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def close(self):
        if self._cursor:
            self._cursor.close()
        if (self._connection):
            self._connection.close()