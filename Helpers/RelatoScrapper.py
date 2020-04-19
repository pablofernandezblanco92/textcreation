from bs4 import BeautifulSoup
import requests


class RelatoScrapper:

    def __init__(self, url):
        self.__url = url
        self.__soup = None
        self.__raw_html = None
        self.__paragraphs = None

    def obtain_html(self):
        self.__raw_html = requests.get(self.__url).content
        self.__soup = BeautifulSoup(self.__raw_html, 'html.parser')

    def is_valid(self):
        # Check if we have found something. Otherwise just jump to the next "relato"
        return not self.__soup.find(id="relato") is None

    def obtain_paragraphs(self):
        # Find "relato" container
        div_relato = self.__soup.find(id="relato")

        # Get all items paragraphs
        self.__paragraphs = div_relato.find_all("p")
        return self.__paragraphs

    def transform_paragraphs_to_plain_text(self):
        paragraphs_text = []
        for paragraph in self.__paragraphs:
            # Convert the html to plain text
            paragraphs_text.append(paragraph.getText())

        return paragraphs_text
