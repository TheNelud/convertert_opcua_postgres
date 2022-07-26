from datetime import datetime
import psycopg2
from parse_config import ParserXML
import logger_info


class Postgres():
    # Инициализируем конфиг из XML
    def __init__(self):
        self.pXML = ParserXML().parser()
        self.logger = logger_info.LogginMyApp().get_logger(__name__)

    # Создаем подключение к базе
    def connection(self):
        try:
            self.connect = psycopg2.connect(database=self.pXML['database']['db_name'],
                                    user=self.pXML['database']['db_user'],
                                    password=self.pXML["database"]['db_password'],
                                    host=self.pXML["database"]['db_host'],
                                    port=self.pXML["database"]['db_port'])
            self.logger.info("Подключено к базе данных ")
            return self.connect


        except psycopg2.OperationalError as e:
            self.logger.info("Подключение к базе данных прошло c ошибкой: " + str(e))
            # print("The error " + e + "occurred")

    # Запрос на вывод всех тегов из базы данных для сравнения с сервером OPC
    def selectTags(self):
        self.sqlSelect = 'SELECT ' + str(self.pXML['database']['tb_column_tag']) + ", " + str(self.pXML['database']['tb_column_id_tag']) + ' FROM ' + str(self.pXML['database']['tb_name']) + ' WHERE ' + str(self.pXML['database']['tb_column_tag']) + ' IS NOT NULL'
        self.connection = self.connection()
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.sqlSelect)
        _selectTags = [self.i for self.i in self.cursor.fetchall()]
        self.connection.close()
        return _selectTags

    # Запрос записи в базу, тегов с их значениями
    def insertTagsValues(self, listValue, toWhichTable):
        self.connection = self.connection()
        for self.key, self.value in listValue.items():
            self.tempstamp = datetime.now()
            self.sqlInsert = "INSERT INTO " + str(toWhichTable) + " (" + str(
                self.pXML['database']['tb_isert_id_tag']) + ", " + str(
                self.pXML['database']['tb_isert_value']) + ", " + str(
                self.pXML['database']['tb_isert_timestamp']) + ") VALUES (\'" + str(self.key) + "\', \'" + str(
                self.value) + "\', '" + str(self.tempstamp) + "\')"
            self.cursor = self.connection.cursor()
            self.cursor.execute(self.sqlInsert)
            self.connection.commit()
        self.connection.close()

    def insertIfNotConnectOpc(self, toWhichTable):
        self.connection = self.connection()
        selectTags = Postgres().selectTags()
        for tag in selectTags:
            tempstamp = datetime.now()
            sqlInsert = "INSERT INTO " + str(toWhichTable) + " (" + str(
                self.pXML['database']['tb_isert_id_tag']) + ", " + str(
                self.pXML['database']['tb_isert_value']) + ", " + str(
                self.pXML['database']['tb_isert_timestamp']) + ") VALUES (\'" + str(tag[1]) + "\', \'" + str(
                0) + "\', '" + str(tempstamp) + "\')"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sqlInsert)
            self.connection.commit()
        self.connection.close()


# if __name__ == "__main__":
#     Postgres().insertIfNotConnectOpc(ParserXML().parser()['rate_5_min']['cl_table'])
    # Postgres().insert()
