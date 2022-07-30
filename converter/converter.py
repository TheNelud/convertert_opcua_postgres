from opcua import Client
from parse_config import ParserXML
from logger_info import LogginMyApp
from postgres import Postgres
import schedule, time


class OpcUAClient():
    def __init__(self):
        self.pXML = ParserXML().parser()
        self.logger = LogginMyApp().get_logger(__name__)
        self.selectTags = Postgres().selectTags()
        # self.selectTagsAlpha = Postgres().selectDataAlpha()

        self.listValue = {}
        self.counter = 0

    # Подлючение клиентом OPC UA к серверу
    def connectClient(self):
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

    # Берет названия тегов из базы, ищет на сервере OPC считывая их значение и отправляет обратно в базу
    def processPostrgres(self, client, toWhichTable):
        for self.tagsElement in self.selectTags:  # ['GD06.UF01UD01.KS01.GCA.CTGA_AVO1.Socket_PLC.Value', '232']
            self.node = client.get_node('ns=1;s=' + str(self.tagsElement[0]))
            try:
                self.listValue[self.tagsElement[1]] = self.node.get_value()
            except Exception as e:
                self.listValue[self.tagsElement[1]] = 0
                self.counter += 1
        if self.counter > 0:
            self.logger.warning("Пустые значения")
        self.logger.info("Данные собраны с сервера opc")
        Postgres().insertTagsValues(self.listValue, toWhichTable)
        self.logger.info("Данные отправлены в базу")

    # def processAlpha(self, client):
    #     # TODO: Отправление из базы данных на сервер Alpha
    #     for self.tagsElementAplha in self.selectTagsAlpha:
    #         self.node = client.get_node('ns=1;s=' + str(self.tagsElementAplha[0]))
    #         self.node.set_value(self.tagsElementAplha[1])
    #         self.node.get_data_value()
    #     client.close_session()


    def main(self):
        # настройка по расписанию postgres -> opc -> postgres
        schedule.every(5).minutes.at(':00').do(OpcUAClient().processPostrgres, client=OpcUAClient().connectClient(),toWhichTable=ParserXML().parser()['rate_5_min']['cl_table'])
        schedule.every().hour.at(':00').do(OpcUAClient().processPostrgres, client=OpcUAClient().connectClient(),toWhichTable=ParserXML().parser()['rate_1_hour']['cl_table'])
        schedule.every().day.at("10:00:00").do(OpcUAClient().processPostrgres, client=OpcUAClient().connectClient(),toWhichTable=ParserXML().parser()['rate_1_day']['cl_table'])

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':

    # OpcUAClient().processPostrgres(OpcUAClient().connectClient(), ParserXML().parser()['rate_5_min']['cl_table'])
    OpcUAClient().main()
