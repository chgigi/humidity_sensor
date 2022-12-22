import psycopg2
from psycopg2 import Error


class DataBase:
    def __init__(self, user, password, address, port, name, logger):
        self._user = user
        self._password = password
        self._address = address
        self._port = port
        self._name = name
        self._logger = logger
        self._connection = None
        self._cursor = None
        self.creation()

    def creation(self):
        self.connect()
        self._cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
        if not self._cursor.fetchall():
            self._cursor.execute("CREATE TABLE method (id serial, local boolean, host varchar, port integer);")
            self._cursor.execute("CREATE TABLE room (id serial, type varchar, name varchar, data method);")
            self._connection.commit()

    def connect(self):
        try:
            self._connection = psycopg2.connect(user=self._user,
                                                password=self._password,
                                                host=self._address,
                                                port=self._port,
                                                database=self._name)
            self._cursor = self._connection.cursor()
        except (Exception, Error) as error:
            self._logger.error(f"Unable to connect to the DataBase: {error[0]} : {error[1]}")
            return False
        return True

    def close(self):
        if self._cursor:
            self._cursor.close()
        if (self._connection):
            self._connection.close()


    def add_room(self, name, type, method):
        # TBD
        return True
