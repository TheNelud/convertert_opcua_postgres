
from opcua import Client
from parse_config import ParserXML
from logger_info import LogginMyApp
from postgres import Postgres
import schedule, time
from threading import Timer



class OpcUAClient:
    def __init__(self):
        self.pXML = ParserXML().parser()
        self.logger = LogginMyApp().get_logger(__name__)

        self.listValue = {}
        self.counter = 0
        self.myTime = int(time.strftime("%M"))

    def get_ua_type(self, value):
        if value.__class__.__name__ == 'int':
            return int(value)
        elif value.__class__.__name__ == 'float':
            return float(value)
        elif value.__class__.__name__ == 'bool':
            if value == "True":
                return 1
            else:
                return 0
        elif value.__class__.__name__ == 'str':
            return str(value)
        elif value.__class__.__name__ == 'double':
            return float(value)
        else:
            return None

    # Подлючение клиентом OPC UA к серверу
    def connectClient(self):
        try:
            try:
                self.client = Client(self.pXML['opcserver_master']['opc_host'])
                self.client.connect()
                self.logger.info("Connect master server: " + self.pXML['opcserver_master']['opc_host'])
                return self.client
            except Exception:
                self.client = Client(self.pXML['opcserver_slave']['opc_host'])
                self.client.connect()
                self.logger.warning("Connect slave server: " + self.pXML['opcserver_master']['opc_host'])
                return self.client
        except ConnectionRefusedError:

            time.sleep(60)
            if self.myTime == 0:
                self.logger.warning("No connection to server OPC")

            OpcUAClient().connectClient()


    # Берет названия тегов из базы, ищет на сервере OPC считывая их значение и отправляет обратно в базу
    def processPostrgres(self, client, toWhichTable):
        # try:
        for self.tagsElement in Postgres().selectTags():  # ['GD06.UF01UD01.KS01.GCA.CTGA_AVO1.Socket_PLC.Value', '232']
            self.node = client.get_node('ns=1;s=' + str(self.tagsElement[0]))
            # print(self.node)
            try:
                self.listValue[self.tagsElement[1]] = self.get_ua_type(self.node.get_value())
                print(str(self.node) + " : " + str(self.node.get_value()))
            except Exception as e:
                self.listValue[self.tagsElement[1]] = 0
                self.counter += 1
        if self.counter > 0:
            self.logger.warning("Пустые значения")
        self.logger.info("Данные собраны с сервера opc")
        Postgres().insertTagsValues(self.listValue, toWhichTable)
        self.logger.info("Данные отправлены в базу")
        # except ConnectionRefusedError:
        #     self.logger.warning('Нет связи с сервером OPC')
        #     Postgres().insertIfNotConnectOpc(toWhichTable)
        #     self.logger.info("Данные записанны с нулевыми значениями")


    def everyFiveMinutes(self):
        OpcUAClient().processPostrgres(OpcUAClient().connectClient(), ParserXML().parser()['rate_5_min']['cl_table'])

    def everyOneHour(self):
        OpcUAClient().processPostrgres(OpcUAClient().connectClient(), ParserXML().parser()['rate_1_hour']['cl_table'])
    def everyOneDay(self):
        OpcUAClient().processPostrgres(OpcUAClient().connectClient(), ParserXML().parser()['rate_1_day']['cl_table'])

    def main(self):
        # настройка по расписанию postgres -> opc -> postgres


        while True:
            if self.myTime % 5 == 0 or self.myTime == 0:
                OpcUAClient().processPostrgres(OpcUAClient().connectClient(),
                                               ParserXML().parser()['rate_5_min']['cl_table'])
                schedule.every(5).minutes.at(':00').do(OpcUAClient().everyFiveMinutes)

                break
            else:
                self.myTime = int(time.strftime("%M"))

        schedule.every().hour.at(':45').do(OpcUAClient().everyOneHour)
        schedule.every().day.at("10:00:00").do(OpcUAClient().everyOneDay)

        while True:
            schedule.run_pending()
            time.sleep(1)



if __name__ == '__main__':
    print("Version - 2.2 260922 ")
    OpcUAClient().main()
