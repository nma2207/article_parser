#coding: utf-8

import requests
from bs4 import BeautifulSoup

class ArticleParser:
    '''
    Класс, который будет извлекать текст статьи
    '''
    MAX_LINE_LENGTH = 80

    def get_article(self, link, filename):
    '''Метод, вызываемый для работы алгоритма
    
    Arguments:
        link {str} -- ссылка на сайт
    
    Keyword Arguments:
        filename {str} -- куда сохранять
    '''

        html = self.__get_text(link)
        if not html:
            print('Link {0} is not available'.format(link))
            return
        
        sections = self.__extract_sections(html)

        sections = self.__divide_by_length(sections)

        self.__save_to_file(sections, filename)

    def __get_text(self, link):
        '''
        Получает html-кода из сайта.
        Возвращает None, если страница недоступна
        '''

        response = requests.get(link)

        if response.status_code != 200:
            return None
        else:
            return response.text

    def __extract_sections(self, text):
        '''
        Парсит html-код на абзацы
        
        Returns:
            абзацы
        '''

        soup = BeautifulSoup(text, "html.parser")

        title = soup.find("title")
        sections = [title.text]

        sections_html = soup.find(
            "div", {"itemprop": "articleBody"}).findAll("p")
        for section in sections_html:
            section_text = ""
            for content in section.contents:
                try:
                    content_text = "[{0}] {1}".format(content.get("href"), content.text)
                except:
                    content_text = str(content)
                section_text += content_text
            sections.append(section_text)
        return sections

    
    def __divide_by_length(self, sections):
        '''
        Делает абзацы такими, чтобы длина строки не превышала 
        максимально допустимой
        
        Returns:
            Красивые абзацы
        '''

        result = []
        for section in sections:
            new_section = ""
            split_section = section.split(" ")
            line = ""
            for word in split_section:
                if len(line) + len(word) < self.MAX_LINE_LENGTH:
                    line += (word + " ")
                else:
                    new_section += (line + "\n")
                    line = word + " "
            new_section += line
            result.append(new_section)
        return result
    
    def __save_to_file(self, sections, filename):
        '''
        Сохраняет абзацы в файл
        '''

        with open(filename, "w") as file:
            for section in sections:
                file.write(section)
                file.write("\n\n")
        


    
