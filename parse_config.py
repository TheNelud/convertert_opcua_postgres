import xml.etree.ElementTree as ET

class ParserXML():
    def __init__(self) :
        self.tree = ET.parse("J:\job\opcua_postgres\opcua_35\config.xml")
        self.root = self.tree.getroot()
        self.external_result = {}
        
    #Парсинг XML конфигурации конвертера
    def parser(self):
        for self.external_elements in self.root:
            self.inside_result = {}
            self.external_result[self.external_elements.tag] = self.inside_result
            for element in self.external_elements:
                self.inside_result[element.tag] = element.text
        return self.external_result

# if __name__ == '__main__':
#     print(ParserXML().parser())